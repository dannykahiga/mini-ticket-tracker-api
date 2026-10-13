from fastapi import FastAPI

from routers.tickets import router as tickets_router

app = FastAPI(
    title="Mini Ticket Tracker",
    version="1.0.0",
    description="A REST API for managing support tickets.",
)

app.include_router(tickets_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}