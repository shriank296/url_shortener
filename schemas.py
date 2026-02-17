from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class UrlCreate(BaseModel):
    original_url: HttpUrl


class UrlResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    short_code: str
    short_url: HttpUrl
    expires_at: datetime
