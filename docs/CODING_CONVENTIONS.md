# 코딩 컨벤션

## 언어 / 도구

- Python 3.12+
- 린트·포맷: **ruff** (`uv run ruff check .`, `uv run ruff format .`)
- 스타일 기준: PEP8 (line-length 100)

## 네이밍

| 대상 | 규칙 | 예시 |
|------|------|------|
| 변수 / 함수 | `snake_case` | `create_item`, `item_id` |
| 클래스 | `PascalCase` | `Item`, `ItemCreate` |
| 상수 | `UPPER_SNAKE_CASE` | `REQUIRED_COLUMNS` |
| 모듈 / 파일 | `snake_case` | `file_processor.py` |

- Pydantic 스키마는 역할을 접미사로 명시: `XxxCreate`, `XxxUpdate`, `XxxRead`.

## 타입 힌트

- 모든 함수 시그니처에 타입 힌트를 붙인다.
- Python 3.12 문법 사용: `str | None`, `list[int]`, `dict[str, str]`.

## 계층 구조 (레이어드 아키텍처)

관심사를 분리한다. 새 기능은 아래 계층 순서를 따른다:

```
api/routes  (요청/응답, HTTP 상태코드 — 얇게 유지)
    ↓
crud        (DB 접근 로직)  /  services (비즈니스 로직: 파일 파싱 등)
    ↓
models      (SQLAlchemy ORM 테이블)
schemas     (Pydantic 요청/응답 모델)
core        (설정, DB 연결 등 공통 인프라)
```

### 규칙
- **라우터는 얇게**: 검증·상태코드 처리만 하고, 실제 로직은 `crud`/`services`에 위임한다.
- **DB 접근은 `crud`에만**: 라우터에서 SQLAlchemy 쿼리를 직접 작성하지 않는다.
- **비즈니스 로직은 `services`에**: 파일 파싱·외부연동 등은 서비스 계층으로.
- **입출력은 `schemas`로**: ORM 모델을 API에 그대로 노출하지 않고 `ItemRead` 등으로 변환한다.

## 비동기(async)

- DB I/O 는 async 세션(`AsyncSession`)을 사용한다.
- 라우터·CRUD·서비스의 I/O 함수는 `async def` 로 작성한다.

## Docstring / 주석

- 모든 모듈·공개 함수에 한 줄 이상의 docstring 을 한글로 작성한다.
- 주석은 "무엇"보다 "왜"를 설명한다.

## 에러 처리

- 클라이언트 입력 오류는 `HTTPException`(4xx)으로 명확히 반환한다.
- 서비스 계층은 도메인 예외(예: `FileProcessingError`)를 던지고, 라우터가 HTTP 응답으로 변환한다.

## 테스트

- 새 기능/버그 수정에는 테스트를 추가한다.
- 테스트는 Docker 없이 실행되도록 SQLite 인메모리를 사용한다(`tests/conftest.py`).
