from fastapi import FastAPI
from app.api.document_routes import router as document_router

app = FastAPI(
    title="AI Document Assistant",
    version="1.0.0",
)

app.include_router(document_router)

@app.get("/")
def root():
    return {"message": "AI Document Assistant API running"}