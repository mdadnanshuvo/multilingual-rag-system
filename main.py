from fastapi import FastAPI

from app.routes.ask import router as ask_router
from app.routes.evaluate import router as eval_router
from app.routes.health import router as health_router
from app.routes.upload import router as upload_router

app = FastAPI()

app.include_router(ask_router, prefix="/ask", tags=["Ask"])
app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(upload_router, prefix="/upload", tags=["Upload"])
app.include_router(eval_router, prefix="/evaluate", tags=["Evaluate"])
