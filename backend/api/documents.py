from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
import shutil
import uuid
from datetime import date

from database.connection import get_db
from schemas.document import DocumentResponse
from services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}


@router.post("/", response_model=DocumentResponse)
def create_document(
    title: str = Form(...),
    category: str = Form(...),
    expiry_date: Optional[date] = Form(None),
    reminder_days_before: int = Form(30),
    notes: Optional[str] = Form(None),
    user_id: int = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    file_url = None

    if file:
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only PDF, JPG, JPEG, and PNG files are allowed",
            )

        unique_filename = f"{uuid.uuid4()}{ext}"
        file_path = UPLOAD_DIR / unique_filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_url = str(file_path)

    service = DocumentService(db)
    document_data = {
        "title": title,
        "category": category,
        "expiry_date": expiry_date,
        "reminder_days_before": reminder_days_before,
        "file_url": file_url,
        "notes": notes,
        "user_id": user_id,
    }

    return service.create_document(document_data)


@router.get("/{user_id}", response_model=List[DocumentResponse])
def get_documents(user_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_all_documents(user_id)


@router.get("/expired/{user_id}", response_model=List[DocumentResponse])
def get_expired_documents(user_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_expired_documents(user_id)


@router.get("/expiring-soon/{user_id}", response_model=List[DocumentResponse])
def get_expiring_soon_documents(user_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.get_expiring_soon_documents(user_id)


@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    service = DocumentService(db)
    return service.delete_document(document_id)