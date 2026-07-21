from pathlib import Path
from uuid import uuid4
import shutil

UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf"}


def validate_file(filename: str):
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}. Only PDF files are allowed."
        )


def save_upload_file(file):
    validate_file(file.filename)

    unique_name = f"{uuid4()}{Path(file.filename).suffix}"

    destination = UPLOAD_DIR / unique_name

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return destination, unique_name