# FastAPI Sample

CRUD 및 엑셀/CSV 처리를 확인하기 위한 학습·데모용 FastAPI 서버.

## 스택

- **FastAPI** + **uvicorn**
- **SQLAlchemy 2.0 (async)** + **MySQL** (Docker) — 테스트는 SQLite 인메모리
- **pandas / openpyxl** (엑셀·CSV 처리)
- **uv** (패키지 관리) · **pytest** (테스트) · **ruff** (린트/포맷)

## 사전 준비

- [uv](https://docs.astral.sh/uv/) 설치
- Docker / Docker Compose 설치 (MySQL 사용 시)

## 빠른 시작

```bash
# 1) 환경변수 준비
cp .env.example .env

# 2) MySQL 컨테이너 기동 (DB만)
docker compose up -d db

# 3) 의존성 설치
uv sync

# 4) 서버 실행
uv run uvicorn app.main:app --reload

# 5) 문서(Swagger UI) 확인
open http://localhost:8000/docs
```

> 앱까지 컨테이너로 실행하려면: `docker compose --profile app up --build`

## 주요 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| GET | `/health` | 상태 확인 |
| POST | `/items` | 상품 생성 (201) |
| GET | `/items` | 상품 목록 (`skip`, `limit`) |
| GET | `/items/{id}` | 상품 단건 조회 |
| PUT | `/items/{id}` | 상품 수정 (부분 수정) |
| DELETE | `/items/{id}` | 상품 삭제 (204) |
| POST | `/items/upload` | 엑셀/CSV 업로드 일괄 등록 |

### 사용 예시 (curl)

```bash
# 생성
curl -X POST localhost:8000/items \
  -H 'Content-Type: application/json' \
  -d '{"name":"사과","description":"국산","price":1500,"quantity":10}'

# 목록
curl localhost:8000/items

# 파일 업로드 (CSV / XLSX)
curl -X POST localhost:8000/items/upload -F 'file=@sample_data/items.csv'
```

업로드 응답 예시:
```json
{"filename": "items.csv", "created": 4, "failed": 3,
 "errors": [{"row": 4, "message": "name: String should have at least 1 character"}]}
```

## 파일 업로드 형식

- 지원 형식: `.csv`, `.xlsx`
- **필수 컬럼**: `name`, `price`, `quantity`
- **선택 컬럼**: `description`
- 유효한 행은 저장되고, 잘못된 행은 저장되지 않고 오류 리포트로 반환된다(부분 성공).

## 테스트 / 린트

```bash
uv run pytest -v      # 테스트 (Docker 불필요, SQLite 인메모리)
uv run ruff check .   # 린트
uv run ruff format .  # 포맷
```

## 디렉토리 구조

```
app/
├── main.py              # 앱 진입점, lifespan(테이블 생성), 라우터 등록
├── core/                # 설정(config), DB 연결(database)
├── models/              # SQLAlchemy ORM 모델 (item)
├── schemas/             # Pydantic 요청/응답 스키마 (item)
├── crud/                # DB 접근 로직 (item)
├── services/            # 비즈니스 로직 (file_processor)
└── api/routes/          # 엔드포인트 (items, files)
tests/                   # pytest 테스트
sample_data/             # 업로드 테스트용 샘플 (items.csv, items.xlsx)
```

## 문서

- [CLAUDE.md](CLAUDE.md) — 프로젝트 개요·아키텍처·명령 가이드
- [docs/GIT_CONVENTIONS.md](docs/GIT_CONVENTIONS.md) — 커밋/브랜치/PR/문서 갱신 규칙
- [docs/CODING_CONVENTIONS.md](docs/CODING_CONVENTIONS.md) — 코드 스타일·구조 규칙
