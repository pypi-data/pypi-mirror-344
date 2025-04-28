from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from .config import AdServingConfig
from .targeting import select_ads
from .utils import insert_ads_into_response
from loguru import logger
from .services.ad_analytics_service import record_ad_impression
import json

class AdServingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, config: AdServingConfig = None):
        super().__init__(app)
        self.config = config or AdServingConfig()
        logger.info(f"AdServingMiddleware initialized with config: {self.config}")

    async def dispatch(self, request: Request, call_next):
        # Only process LLM prompt endpoints
        if request.url.path not in self.config.target_paths:
            logger.info(f"Skipping middleware for path: {request.url.path}")
            return await call_next(request)
            
        logger.info(f"Processing request for path: {request.url.path}")
        
        # Get the request body
        body = await request.body()
        logger.info(f"Request body: {body.decode() if isinstance(body, bytes) else body}")
        
        try:
            # Select ads from remote API
            ads = await select_ads(body, self.config)
            logger.info(f"Selected ads in middleware: {json.dumps(ads, indent=2)}")
            
            # Record impressions for selected ads via remote API
            for ad in ads:
                await record_ad_impression(
                    ad_id=ad["id"],
                    prompt=body.decode() if isinstance(body, bytes) else str(body),
                    config=self.config
                )
            
            # Store ads in request state
            request.state.selected_ads = ads
            logger.info(f"Set request.state.selected_ads to: {json.dumps(ads, indent=2)}")
            
            # Continue with the request
            response = await call_next(request)
            return response
            
        except Exception as e:
            logger.error(f"Error in ad serving middleware: {e}")
            return await call_next(request) 