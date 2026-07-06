"""애플리케이션 설정. 환경변수(.env)에서 값을 로드한다."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """환경변수 기반 설정값.

    .env 파일 또는 실제 환경변수에서 값을 읽어온다.
    """

    # 기본값은 로컬 docker-compose 의 db 서비스와 일치
    database_url: str = "mysql+aiomysql://sample:sample@localhost:3306/fastapi_sample"
    app_name: str = "FastAPI Sample"
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
