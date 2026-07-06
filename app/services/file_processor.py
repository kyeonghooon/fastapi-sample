"""엑셀/CSV 파일을 파싱해 Item 데이터로 변환하는 서비스.

지원 형식: .csv, .xlsx (및 .xls)
필수 컬럼: name, price, quantity
선택 컬럼: description

각 행을 검증해 유효한 행은 ItemCreate 로, 잘못된 행은 오류 리포트로 분리한다.
"""

import io
from dataclasses import dataclass, field

import pandas as pd
from pydantic import ValidationError

from app.schemas.item import ItemCreate

REQUIRED_COLUMNS = {"name", "price", "quantity"}
SUPPORTED_EXTENSIONS = (".csv", ".xlsx", ".xls")


class FileProcessingError(Exception):
    """파일 자체를 처리할 수 없을 때 발생 (형식 오류, 필수 컬럼 누락 등)."""


@dataclass
class RowError:
    """행 단위 검증 오류."""

    row: int  # 데이터 행 번호 (1부터, 헤더 제외)
    message: str


@dataclass
class ParseResult:
    """파싱 결과: 유효한 항목 목록 + 오류 목록."""

    items: list[ItemCreate] = field(default_factory=list)
    errors: list[RowError] = field(default_factory=list)


def _read_dataframe(filename: str, content: bytes) -> pd.DataFrame:
    """파일 확장자에 맞춰 DataFrame 으로 읽는다."""
    lower = filename.lower()
    buffer = io.BytesIO(content)
    if lower.endswith(".csv"):
        return pd.read_csv(buffer)
    if lower.endswith((".xlsx", ".xls")):
        return pd.read_excel(buffer)
    raise FileProcessingError(
        f"지원하지 않는 파일 형식입니다. 지원 형식: {', '.join(SUPPORTED_EXTENSIONS)}"
    )


def parse_items_file(filename: str, content: bytes) -> ParseResult:
    """엑셀/CSV 파일 내용을 파싱해 ParseResult 로 반환한다.

    Args:
        filename: 원본 파일명 (확장자 판별용)
        content: 파일 바이트 내용

    Raises:
        FileProcessingError: 형식 미지원 또는 필수 컬럼 누락 등 파일 전체 오류
    """
    try:
        df = _read_dataframe(filename, content)
    except FileProcessingError:
        raise
    except Exception as exc:  # pandas 파싱 실패
        raise FileProcessingError(f"파일을 읽을 수 없습니다: {exc}") from exc

    # 컬럼명 정규화 (앞뒤 공백 제거, 소문자화)
    df.columns = [str(c).strip().lower() for c in df.columns]

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise FileProcessingError(
            f"필수 컬럼이 없습니다: {', '.join(sorted(missing))}. "
            f"필요한 컬럼: {', '.join(sorted(REQUIRED_COLUMNS))}"
        )

    result = ParseResult()
    for idx, row in df.iterrows():
        row_num = int(idx) + 1  # 데이터 기준 행 번호
        try:
            item = ItemCreate(
                name=_clean_str(row.get("name")),
                description=_clean_optional_str(row.get("description")),
                price=row.get("price"),
                quantity=row.get("quantity"),
            )
            result.items.append(item)
        except (ValidationError, ValueError, TypeError) as exc:
            result.errors.append(RowError(row=row_num, message=_summarize_error(exc)))

    return result


def _clean_str(value: object) -> str:
    """필수 문자열 값 정리. NaN/None 이면 빈 문자열로 → 검증에서 걸러짐."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def _clean_optional_str(value: object) -> str | None:
    """선택 문자열 값 정리. 비어있으면 None."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip()
    return text or None


def _summarize_error(exc: Exception) -> str:
    """검증 오류를 사람이 읽기 쉬운 한 줄로 요약."""
    if isinstance(exc, ValidationError):
        parts = []
        for err in exc.errors():
            loc = ".".join(str(x) for x in err["loc"])
            parts.append(f"{loc}: {err['msg']}")
        return "; ".join(parts)
    return str(exc)
