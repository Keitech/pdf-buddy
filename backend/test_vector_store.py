from app.services.vector_service import add_chunks


chunks = [
    "Employees receive 20 vacation days per year.",
    "Employees receive 10 sick days per year.",
    "Employees can work remotely three days per week.",
    "Full-time employees receive health and dental benefits."
]


add_chunks(
    document_id="employee-handbook",
    chunks=chunks
)


print("Chunks stored successfully")