import httpx
from .config import AdServingConfig
from loguru import logger

async def record_ad_impression(ad_id: int, prompt: str, config: AdServingConfig):
    logger.info(f"Recording ad impression for ad_id={ad_id}")
    payload = {
        "ad_id": ad_id,
        "prompt": prompt,
        "publisher_id": config.publisher_id
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{config.api_base_url}/analytics/impression", json=payload)
        response.raise_for_status()
    logger.info("Ad impression recorded via remote API") 