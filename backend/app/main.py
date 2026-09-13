from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="AI Medical Assistant - Bedrock")

app.include_router(router)