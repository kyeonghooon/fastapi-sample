"""Item 요청/응답 스키마 (Pydantic).

- Create: 생성 시 입력
- Update: 수정 시 입력 (부분 수정 허용)
- Read: 응답 (DB 모델 → JSON)
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    """생성/수정 공통 필드."""

    name: str = Field(..., min_length=1, max_length=255, description="상품명")
    description: str | None = Field(None, description="상품 설명")
    price: float = Field(0, ge=0, description="가격 (0 이상)")
    quantity: int = Field(0, ge=0, description="수량 (0 이상)")


class ItemCreate(ItemBase):
    """상품 생성 요청 스키마."""


class ItemUpdate(BaseModel):
    """상품 수정 요청 스키마 (전달된 필드만 수정)."""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    price: float | None = Field(None, ge=0)
    quantity: int | None = Field(None, ge=0)


class ItemRead(ItemBase):
    """상품 응답 스키마."""

    id: int
    created_at: datetime

    # ORM 객체(속성 접근)를 그대로 직렬화할 수 있게 한다.
    model_config = ConfigDict(from_attributes=True)
