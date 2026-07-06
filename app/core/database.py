"""데이터베이스 연결 및 세션 관리.

async SQLAlchemy 2.0 스타일. 앱은 MySQL(aiomysql), 테스트는 SQLite(aiosqlite)를
같은 코드로 사용할 수 있다.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """모든 ORM 모델의 베이스 클래스."""


# echo=True 로 하면 실행되는 SQL 을 로그로 볼 수 있다 (디버그용).
engine = create_async_engine(settings.database_url, echo=settings.debug, future=True)

async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """요청마다 DB 세션을 제공하는 FastAPI 의존성.

    요청 처리가 끝나면 세션이 자동으로 닫힌다.
    """
    async with async_session_maker() as session:
        yield session


async def create_tables() -> None:
    """등록된 모델을 기반으로 테이블을 생성한다 (데모 편의용).

    실제 서비스에서는 Alembic 같은 마이그레이션 도구 사용을 권장한다.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
