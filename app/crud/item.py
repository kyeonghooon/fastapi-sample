"""Item DB 접근 계층 (CRUD).

라우터는 이 함수들을 호출하기만 하고, 실제 DB 로직은 여기에 모은다.
"""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


async def create_item(db: AsyncSession, data: ItemCreate) -> Item:
    """상품 1건 생성."""
    item = Item(**data.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def get_item(db: AsyncSession, item_id: int) -> Item | None:
    """id 로 상품 조회. 없으면 None."""
    return await db.get(Item, item_id)


async def list_items(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[Item]:
    """상품 목록 조회 (페이지네이션)."""
    stmt = select(Item).order_by(Item.id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_item(db: AsyncSession, item: Item, data: ItemUpdate) -> Item:
    """전달된 필드만 부분 수정."""
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    await db.commit()
    await db.refresh(item)
    return item


async def delete_item(db: AsyncSession, item: Item) -> None:
    """상품 삭제."""
    await db.delete(item)
    await db.commit()


async def bulk_create_items(db: AsyncSession, items: list[ItemCreate]) -> int:
    """상품 여러 건을 한 번에 생성. 생성된 건수를 반환한다.

    엑셀/CSV 업로드 처리에서 사용한다.
    """
    objects = [Item(**data.model_dump()) for data in items]
    db.add_all(objects)
    await db.commit()
    return len(objects)
