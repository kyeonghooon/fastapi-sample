"""Item CRUD 엔드포인트 테스트."""

from httpx import AsyncClient


async def test_health(client: AsyncClient) -> None:
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


async def test_create_and_get_item(client: AsyncClient) -> None:
    # 생성
    resp = await client.post(
        "/items",
        json={"name": "사과", "description": "국산", "price": 1500, "quantity": 10},
    )
    assert resp.status_code == 201
    created = resp.json()
    assert created["id"] > 0
    assert created["name"] == "사과"
    item_id = created["id"]

    # 단건 조회
    resp = await client.get(f"/items/{item_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "사과"


async def test_list_items(client: AsyncClient) -> None:
    for i in range(3):
        await client.post("/items", json={"name": f"상품{i}", "price": 100 * i, "quantity": i})
    resp = await client.get("/items")
    assert resp.status_code == 200
    assert len(resp.json()) == 3


async def test_update_item(client: AsyncClient) -> None:
    resp = await client.post("/items", json={"name": "구", "price": 100, "quantity": 1})
    item_id = resp.json()["id"]

    resp = await client.put(f"/items/{item_id}", json={"name": "신", "price": 200})
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "신"
    assert body["price"] == 200
    assert body["quantity"] == 1  # 전달 안 한 필드는 유지


async def test_delete_item(client: AsyncClient) -> None:
    resp = await client.post("/items", json={"name": "삭제대상", "price": 10, "quantity": 1})
    item_id = resp.json()["id"]

    resp = await client.delete(f"/items/{item_id}")
    assert resp.status_code == 204

    resp = await client.get(f"/items/{item_id}")
    assert resp.status_code == 404


async def test_get_missing_item_returns_404(client: AsyncClient) -> None:
    resp = await client.get("/items/9999")
    assert resp.status_code == 404


async def test_create_invalid_item_returns_422(client: AsyncClient) -> None:
    # 이름 누락 → 검증 실패
    resp = await client.post("/items", json={"price": 100, "quantity": 1})
    assert resp.status_code == 422
