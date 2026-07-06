"""FastAPI 애플리케이션 진입점."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import files, items
from app.core.config import settings
from app.core.database import create_tables

# 모델을 import 해야 Base.metadata 에 테이블이 등록된다.
from app.models import item as _item  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 시작 시 테이블을 생성한다 (데모 편의용)."""
    await create_tables()
    yield


app = FastAPI(
    title=settings.app_name,
    description="CRUD 및 엑셀/CSV 처리 데모 서버",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(items.router)
app.include_router(files.router)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """서버 상태 확인용 엔드포인트."""
    return {"status": "ok"}
