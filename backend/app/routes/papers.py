from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.models.schemas import PaperResponse, AnalysisResponse, ChatRequest, ChatResponse
from app.services.research_assistant import db

router = APIRouter()

@router.post("/upload", response_model=PaperResponse)
async def upload_paper(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        contents = await file.read()
        paper_record = db.process_pdf(file.filename, contents)
        return paper_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[PaperResponse])
async def list_papers():
    return db.get_all_papers()

@router.delete("/{paper_id}")
async def delete_paper(paper_id: str):
    try:
        db.delete_paper(paper_id)
        return {"message": "Deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analyze", response_model=AnalysisResponse)
async def analyze_all_papers():
    try:
        analysis = db.perform_cross_paper_analysis()
        return analysis
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        answer = db.chat_with_papers(request.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
