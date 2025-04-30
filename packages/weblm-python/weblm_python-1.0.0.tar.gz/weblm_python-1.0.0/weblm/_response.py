from typing import Dict, List

from pydantic import BaseModel, HttpUrl


class ConvertResponse(BaseModel):
    markdown: str
    url: HttpUrl
    token_count: int | None = None
    model_name: str | None = None


class ScrapeLinksResponse(BaseModel):
    urls: List[HttpUrl]


class ModelsResponse(BaseModel):
    models: Dict[str, List[str]]
