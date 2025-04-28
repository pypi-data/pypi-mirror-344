from fastapi import Response
from typing import List, Dict, Any
from .config import AdServingConfig
import json

async def insert_ads_into_response(response: Response, ads: List[Dict[str, Any]], config: AdServingConfig) -> Response:
    """
    Insert ads into the response body.
    This is a placeholder implementation - you can enhance it based on your needs.
    """
    try:
        # Get the response body
        body = await response.body()
        
        # Parse the response body
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            # If the response is not JSON, return as is
            return response
            
        # Add ads to the response
        if isinstance(data, dict):
            data['ads'] = ads
        elif isinstance(data, list):
            data.append({'ads': ads})
            
        # Update the response body
        response.body = json.dumps(data).encode()
        response.headers['content-length'] = str(len(response.body))
        
        return response
    except Exception as e:
        # If anything goes wrong, return the original response
        return response

async def insert_ads_into_response_old(response: Response, ads: List[dict], config: AdServingConfig) -> Response:
    """Insert ads into the response."""
    try:
        if response.media_type == "application/json":
            data = json.loads(response.body.decode()) if hasattr(response, 'body') else {}
            
            # Add ads to the response
            data["ads"] = [{
                "id": ad["id"],
                "title": ad["title"],
                "description": ad["description"],
                "category": ad["category"],
                "score": ad["score"],
                "ctr": ad["ctr"]
            } for ad in ads]
            
            # Add targeting info if in debug mode
            if config.debug:
                data["targeting_info"] = {
                    "total_ads_found": len(ads),
                    "categories": config.ad_categories,
                    "scores": {ad["title"]: ad["score"] for ad in ads}
                }
            
            response.body = json.dumps(data).encode()
            
        elif response.media_type == "text/plain":
            text = response.body.decode() if hasattr(response, 'body') else ""
            
            # Format ads as text
            ad_text = "\n\n---\nRelevant Ads:\n"
            for ad in ads:
                ad_text += f"\n• {ad['title']}: {ad['description']}"
                if config.debug:
                    ad_text += f" (Score: {ad['score']:.2f}, CTR: {ad['ctr']:.2%})"
            
            response.body = (text + ad_text).encode()
            
    except Exception as e:
        # Log error but don't break the response
        print(f"Error inserting ads into response: {e}")
        
    return response 