from pydantic import BaseModel
from datetime import datetime


class DocumentMetadata(BaseModel):
    id: str
    original_filename: str
    stored_filename: str
    file_size: int
    upload_time: datetime
    character_count: int