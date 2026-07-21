from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.document import DocumentMetadata
from app.services.file_service import save_upload_file
from app.services.pdf_service import extract_text

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentMetadata)
async def upload_document(file: UploadFile = File(...)):
    try:
        saved_path, stored_name = save_upload_file(file)

        text = extract_text(saved_path)

        metadata = DocumentMetadata(
            id=str(uuid4()),
            original_filename=file.filename,
            stored_filename=stored_name,
            file_size=saved_path.stat().st_size,
            upload_time=datetime.utcnow(),
            character_count=len(text),
        )

        return metadata

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))