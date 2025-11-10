from fastapi import FastAPI

from api.endpoints.session import router as session_router
from api.endpoints.teacher import router as teacher_router

app = FastAPI()

app.include_router(session_router)
app.include_router(teacher_router)
