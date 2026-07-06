"""엑셀/CSV 파일 업로드 및 처리 엔드포인트."""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud import item as crud
from app.services.file_processor import FileProcessingError, parse_items_file

# files 라우터도 /items 하위에 업로드 엔드포인트를 노출한다.
router = APIRouter(prefix="/items", tags=["files"])


class RowErrorOut(BaseModel):
    """행 단위 오류 응답."""

    row: int
    message: str


class UploadResult(BaseModel):
    """업로드 처리 결과 요약."""

    filename: str
    created: int
    failed: int
    errors: list[RowErrorOut]


@router.post("/upload", response_model=UploadResult)
async def upload_items(
    file: UploadFile = File(..., description="엑셀(.xlsx) 또는 CSV(.csv) 파일"),
    db: AsyncSession = Depends(get_db),
) -> UploadResult:
    """엑셀/CSV 파일을 업로드해 상품을 일괄 등록한다.

    - 유효한 행은 DB에 저장한다.
    - 잘못된 행은 저장하지 않고 오류 리포트로 반환한다.
    """
    content = await file.read()
    filename = file.filename or "uploaded"

    try:
        parsed = parse_items_file(filename, content)
    except FileProcessingError as exc:
        # 파일 전체를 처리할 수 없는 경우 400
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    created = 0
    if parsed.items:
        created = await crud.bulk_create_items(db, parsed.items)

    return UploadResult(
        filename=filename,
        created=created,
        failed=len(parsed.errors),
        errors=[RowErrorOut(row=e.row, message=e.message) for e in parsed.errors],
    )
