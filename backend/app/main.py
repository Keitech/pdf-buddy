from fastapi import FastAPI

app = FastAPI(
    title="PDF Buddy Assistant",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AI Document Assistant API running"
    }