from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PaperResponse(BaseModel):
    id: str
    filename: str
    summary: Dict[str, Any]

class AnalysisResponse(BaseModel):
    clusters: List[Dict[str, Any]]
    contradictions: str
    research_gaps: str

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
