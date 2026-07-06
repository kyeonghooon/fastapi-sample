# FastAPI Sample

CRUD 및 엑셀/CSV 처리를 확인하기 위한 학습·데모용 FastAPI 서버.

> ⚠️ **현재 상태**: 1단계(문서·컨벤션·스킬) 완료 / 2단계(앱 구현) 준비 중.
> 아래 스택·실행 방법·엔드포인트는 2단계 구현이 진행되면서 채워집니다.

## 예정 스택

- **FastAPI** + **uvicorn**
- **SQLAlchemy 2.0 (async)** + **MySQL** (Docker) — 테스트는 SQLite 인메모리
- **pandas / openpyxl** (엑셀·CSV 처리)
- **uv** (패키지 관리) · **pytest** (테스트) · **ruff** (린트/포맷)

## 빠른 시작

> 🚧 준비 중 — 앱 구현(2단계) 완료 시 작성.

## 주요 엔드포인트

> 🚧 준비 중 — CRUD 및 파일 업로드 엔드포인트 구현 시 작성.

## 디렉토리 구조

> 🚧 준비 중 — 앱 코드 추가 시 작성.

현재 존재하는 것:
```
CLAUDE.md                 # 프로젝트 가이드 (에이전트용)
docs/                     # 컨벤션 문서
.claude/skills/           # Claude Code 스킬 4종
```

## 문서

- [CLAUDE.md](CLAUDE.md) — 프로젝트 개요·아키텍처·명령 가이드
- [docs/GIT_CONVENTIONS.md](docs/GIT_CONVENTIONS.md) — 커밋/브랜치/PR/문서 갱신 규칙
- [docs/CODING_CONVENTIONS.md](docs/CODING_CONVENTIONS.md) — 코드 스타일·구조 규칙
