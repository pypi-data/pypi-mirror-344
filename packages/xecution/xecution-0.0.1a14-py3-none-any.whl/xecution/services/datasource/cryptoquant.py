from datetime import datetime, timezone
import logging
from xecution.common.cryptoquant_constants import CryptoQuantConstants
from xecution.models.config import RuntimeConfig
from xecution.models.topic import DataTopic
from xecution.services.connection.restapi import RestAPIClient

class CryptoQuantClient:
    def __init__(self, config: RuntimeConfig,data_map: dict):
        self.config = config
        self.rest_client = RestAPIClient()
        self.data_map = data_map
        self.headers = {
            'Authorization': f'Bearer {self.config.cryptoquant_api_key}',
        }

    async def fetch(self, data_topic: DataTopic):
        url = CryptoQuantConstants.BASE_URL + data_topic.url +f'&limit={self.config.data_count}'

        try:
            raw_data = await self.rest_client.request(
                method='GET',
                url=url,
                headers=self.headers
            )

            # 提取資料主體
            result = raw_data.get('result')
            data = result.get('data')

            # 加入 timestamp 欄位 (ms)
            for item in data:
                dt_str = item.get('datetime') or item.get('date')
                if dt_str:
                    try:
                        item['start_time'] = self.parse_datetime_to_timestamp(dt_str)
                    except ValueError as e:
                        logging.warning(f"日期解析失败({dt_str}): {e}")

            rev = list(reversed(data))
            self.data_map[data_topic] = rev
            return rev

        except Exception as e:
            print(f"[{datetime.now()}] Error fetching {data_topic.url}: {e}")
            return []

    def parse_datetime_to_timestamp(self, dt_str: str) -> int:
        for fmt in (
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d %H:%M:%S',
        ):
            try:
                dt = datetime.strptime(dt_str, fmt)
                dt = dt.replace(tzinfo=timezone.utc)
                return int(dt.timestamp() * 1000)
            except ValueError:
                continue
        try:
            clean = dt_str.rstrip('Z')
            dt = datetime.fromisoformat(clean)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp() * 1000)
        except Exception:
            raise ValueError(f"无法识别的日期格式: {dt_str}")

    async def close(self):
        await self.rest_client.close()