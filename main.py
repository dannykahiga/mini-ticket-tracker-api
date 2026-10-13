from fastapi import FastAPI

app = FastAPI(
    title="Mini Ticket Tracker",
    version="1.0.0",
    description="A REST API for managing support tickets.",
)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}