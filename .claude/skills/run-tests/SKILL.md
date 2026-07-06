---
name: run-tests
description: Use when pytest, ruff, 테스트 실행, 실패 분석, 변경사항 검증, 회귀 확인이 필요할 때.
---

# run-tests

pytest 기반 테스트를 실행하고 결과를 정리한다. 테스트는 SQLite 인메모리를
사용하므로 **Docker/MySQL 없이** 실행된다.

## 시작 전 확인

- `pyproject.toml`와 `tests/`가 실제로 있는지 확인한다.
- 테스트 파일이 없거나 프로젝트 코드가 없는 상태라면 테스트를 실행하지 말고 현재 상태를 보고한다.
- 변경 범위가 좁으면 관련 테스트를 먼저 실행한 뒤 전체 테스트로 넓힌다.

## 절차

1. **의존성 확인** (최초 실행, lock/pyproject 변경, 환경 오류 시)
   ```bash
   uv sync
   ```

2. **관련 테스트 실행**
   ```bash
   uv run pytest tests/test_items.py -v
   uv run pytest tests/test_files.py -v
   ```
   변경한 영역에 맞춰 필요한 파일만 먼저 실행한다.

3. **전체 테스트 실행**
   ```bash
   uv run pytest -v
   ```

4. **린트 확인**
   ```bash
   uv run ruff check .
   ```

5. **결과 요약**: 실행한 명령, 통과/실패 개수, 실패 위치를 보고한다.

6. **실패 시 분석**:
   - 실패한 테스트의 assert 메시지와 트레이스백을 읽는다.
   - 필요하면 `uv run pytest -x -vv` (첫 실패에서 멈추고 상세 출력)로 재현.
   - 원인이 코드 버그인지 테스트 기대값 문제인지 구분해 수정한다.
   - 수정 후 같은 테스트를 다시 실행하고, 마지막에 전체 테스트/린트를 실행한다.

## 참고

- 테스트 픽스처는 `tests/conftest.py` 에 있고, `get_db`를 인메모리 세션으로 오버라이드한다.
- 새 모델을 추가했다면 `conftest.py`의 모델 import에 추가해야 테이블이 생성된다.
- 문서만 변경한 경우에는 테스트 대신 변경한 Markdown을 다시 읽어 경로와 명령을 확인한다.
