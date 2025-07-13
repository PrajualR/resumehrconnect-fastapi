from pydantic import BaseModel
from typing import List

class MatchResult(BaseModel):
    filename: str
    similarity: float
    error: str | None = None

class MatchResponse(BaseModel):
    results: List[MatchResult]
