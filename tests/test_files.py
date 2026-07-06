"""엑셀/CSV 업로드 처리 테스트."""

import io

import pandas as pd
from httpx import AsyncClient


def _make_csv() -> bytes:
    """유효행 2건 + 오류행 2건(이름 없음, 가격 음수)."""
    csv = (
        "name,description,price,quantity\n"
        "사과,국산,1500,10\n"
        "바나나,수입,3000,5\n"
        ",이름없음,500,1\n"
        "포도,가격음수,-100,2\n"
    )
    return csv.encode("utf-8")


def _make_xlsx() -> bytes:
    df = pd.DataFrame(
        [
            {"name": "오렌지", "description": "제주", "price": 2000, "quantity": 7},
            {"name": "수박", "description": "여름", "price": 12000, "quantity": 3},
        ]
    )
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    return buffer.getvalue()


async def test_upload_csv(client: AsyncClient) -> None:
    files = {"file": ("items.csv", _make_csv(), "text/csv")}
    resp = await client.post("/items/upload", files=files)
    assert resp.status_code == 200
    body = resp.json()
    assert body["created"] == 2
    assert body["failed"] == 2
    assert len(body["errors"]) == 2

    # 실제로 DB에 반영됐는지 확인
    resp = await client.get("/items")
    assert len(resp.json()) == 2


async def test_upload_xlsx(client: AsyncClient) -> None:
    files = {
        "file": (
            "items.xlsx",
            _make_xlsx(),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    }
    resp = await client.post("/items/upload", files=files)
    assert resp.status_code == 200
    body = resp.json()
    assert body["created"] == 2
    assert body["failed"] == 0


async def test_upload_missing_required_column_returns_400(client: AsyncClient) -> None:
    csv = b"name,price\n\xec\x82\xac\xea\xb3\xbc,1000\n"  # quantity 컬럼 누락
    files = {"file": ("bad.csv", csv, "text/csv")}
    resp = await client.post("/items/upload", files=files)
    assert resp.status_code == 400


async def test_upload_unsupported_format_returns_400(client: AsyncClient) -> None:
    files = {"file": ("data.txt", b"hello", "text/plain")}
    resp = await client.post("/items/upload", files=files)
    assert resp.status_code == 400
