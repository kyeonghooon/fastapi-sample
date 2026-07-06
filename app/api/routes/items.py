"""Item CRUD 엔드포인트."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud import item as crud
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(data: ItemCreate, db: AsyncSession = Depends(get_db)) -> ItemRead:
    """상품을 생성한다."""
    item = await crud.create_item(db, data)
    return item


@router.get("", response_model=list[ItemRead])
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
) -> list[ItemRead]:
    """상품 목록을 조회한다."""
    return list(await crud.list_items(db, skip=skip, limit=limit))


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)) -> ItemRead:
    """상품 1건을 조회한다. 없으면 404."""
    item = await crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="해당 상품을 찾을 수 없습니다")
    return item


@router.put("/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: int, data: ItemUpdate, db: AsyncSession = Depends(get_db)
) -> ItemRead:
    """상품을 수정한다. 없으면 404."""
    item = await crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="해당 상품을 찾을 수 없습니다")
    return await crud.update_item(db, item, data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)) -> None:
    """상품을 삭제한다. 없으면 404."""
    item = await crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="해당 상품을 찾을 수 없습니다")
    await crud.delete_item(db, item)
