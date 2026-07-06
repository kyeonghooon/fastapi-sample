---
name: add-crud
description: Use when 새 도메인, 엔티티, 리소스, CRUD API, model/schema/crud/route 계층을 추가해야 할 때.
---

# add-crud

새 도메인의 CRUD를 기존 Item 패턴과 동일한 레이어드 구조로 추가한다.

## 시작 전 확인

- `app/models/item.py`, `app/schemas/item.py`, `app/crud/item.py`, `app/api/routes/items.py`, `tests/test_items.py`가 실제로 있는지 확인한다.
- 파일 구조가 문서와 다르면 현재 구조를 우선하고, 없는 템플릿 파일을 있다고 가정하지 않는다.
- 불명확하면 사용자에게 엔티티 이름, 테이블명, 라우트 prefix, 필드 목록, 타입, 필수/선택 여부, 기본값을 확인한다.
- 불규칙 복수형이나 도메인 용어가 있으면 라우트명과 테이블명을 먼저 합의한다.

## 생성할 파일 (Item을 템플릿으로 참고)

1. **`app/models/<name>.py`** — `app/models/item.py` 참고
   - `Base` 상속, `__tablename__`, `Mapped[...]` 컬럼 정의
   - MySQL/SQLite 공통 타입만 사용

2. **`app/schemas/<name>.py`** — `app/schemas/item.py` 참고
   - `<Name>Base`, `<Name>Create`, `<Name>Update`(모두 Optional), `<Name>Read`(`from_attributes=True`)

3. **`app/crud/<name>.py`** — `app/crud/item.py` 참고
   - `create_*`, `get_*`, `list_*`, `update_*`, `delete_*`
   - DB I/O는 `AsyncSession`을 사용하고 라우터에 SQLAlchemy 쿼리를 두지 않음

4. **`app/api/routes/<name>.py`** — `app/api/routes/items.py` 참고
   - `APIRouter(prefix="/<plural>", tags=["<plural>"])`
   - POST(201)/GET목록/GET단건/PUT/DELETE(204), 404 처리
   - ORM 모델을 직접 반환하지 않고 Read 스키마로 응답

## 등록 (중요)

- `app/main.py` 에서:
  - `from app.api.routes import <name>` 추가
  - `app.include_router(<name>.router)` 추가
  - 모델 import 추가 (테이블 등록용)
- `tests/conftest.py` 에도 모델 import 추가 (테스트 테이블 생성용)
- `__init__.py`에서 기존 모델/라우터를 모으는 패턴이 있으면 새 엔티티도 같은 방식으로 등록

## 테스트

- `tests/test_<name>.py` 를 `tests/test_items.py` 패턴으로 작성한다.
- 최소 케이스: 생성 → 목록 조회 → 단건 조회 → 수정 → 삭제 → 삭제 후 404.
- 필수값 누락, 존재하지 않는 id, 부분 업데이트 같은 에러/경계 케이스를 기존 테스트 수준에 맞춰 추가한다.

## 마무리

- 관련 테스트를 먼저 실행한 뒤 `uv run pytest -v` 및 `uv run ruff check .` 로 검증한다.
- 검증을 실행할 수 없으면 이유와 대체 확인 내용을 보고한다.
