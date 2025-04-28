from pydantic import BaseModel, Field, root_validator
from typing import List, Optional

class AdServingConfig(BaseModel):
    ad_categories: Optional[List[str]] = Field(default=None, description="Preferred ad categories")
    exclude_types: Optional[List[str]] = Field(default=None, description="Ad types to exclude")
    max_ads: int = Field(default=2, description="Maximum number of ads to show")
    debug: bool = Field(default=False, description="Enable debug logging")
    target_paths: Optional[List[str]] = Field(default_factory=lambda: ["/chat/"])
    environment: str = Field(default="production", description="Environment: production or staging")
    api_base_url: Optional[str] = Field(default=None, description="API base URL")
    publisher_id: Optional[str] = Field(default=None, description="Publisher ID")

    @root_validator(pre=True)
    def set_api_base_url(cls, values):
        env = values.get("environment", "production")
        if not values.get("api_base_url"):
            if env == "staging":
                values["api_base_url"] = "https://staging-api.yourplatform.com"
            else:
                values["api_base_url"] = "https://api.yourplatform.com"
        return values 