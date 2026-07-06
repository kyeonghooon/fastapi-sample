---
name: run-server
description: Use when FastAPI 서버 실행, localhost 검증, health check, Swagger, items CRUD 수동 동작 확인이 필요할 때.
---

# run-server

FastAPI 서버를 기동하고 실제 요청을 보내 동작을 검증하는 절차.

## 시작 전 확인

- `app/main.py`, `pyproject.toml`, `docker-compose.yml`가 실제로 있는지 확인한다.
- 파일이 없으면 서버 실행을 시도하지 말고 현재 폴더 상태와 빠진 파일을 보고한다.
- 기존 서버가 이미 떠 있으면 새로 띄우기 전에 포트와 사용 중인 프로세스를 확인한다.

## 절차

1. **DB 준비** (MySQL 사용 시)
   ```bash
   docker compose up -d db
   ```
   헬스체크 통과 확인:
   ```bash
   docker compose ps
   ```

2. **의존성 설치** (최초 1회 또는 pyproject 변경 시)
   ```bash
   uv sync
   ```

3. **서버 실행** (필요하면 백그라운드로 띄우고 로그 확인)
   ```bash
   uv run uvicorn app.main:app --reload
   ```
   - 기본 주소는 `http://localhost:8000` 이다.
   - 8000 포트가 사용 중이면 사용자에게 알리거나 다른 포트로 실행한다.
   - 검증만 요청받았다면 끝나고 서버 프로세스를 정리한다. 계속 실행 요청이면 유지한다.

4. **동작 검증** — 실제 생성 응답의 id를 재사용한다. `id=1`을 가정하지 않는다.
   ```bash
   BASE_URL=http://localhost:8000

   curl -sS "$BASE_URL/health"

   CREATE_RESPONSE=$(curl -sS -X POST "$BASE_URL/items" \
     -H 'Content-Type: application/json' \
     -d '{"name":"테스트상품","description":"확인용","price":1000,"quantity":5}')
   ITEM_ID=$(python -c 'import json,sys; print(json.load(sys.stdin)["id"])' <<< "$CREATE_RESPONSE")

   curl -sS "$BASE_URL/items"
   curl -sS "$BASE_URL/items/$ITEM_ID"
   curl -sS -X PUT "$BASE_URL/items/$ITEM_ID" \
     -H 'Content-Type: application/json' \
     -d '{"price":2000}'
   curl -sS -X DELETE "$BASE_URL/items/$ITEM_ID" -w '%{http_code}\n'
   curl -sS "$BASE_URL/items/$ITEM_ID" -w '%{http_code}\n'
   ```

5. **파일 업로드가 변경된 경우** — `sample_data/items.csv`가 있으면 `/items/upload`도 확인한다.

6. **결과 요약**: 각 응답의 상태코드와 본문이 기대와 일치하는지 확인해 보고한다.
   - 생성 201, 조회 200, 삭제 204, 없는 id 404
   - 실패 시 서버 로그, DB 상태, 요청/응답 본문을 함께 확인

## 참고

- Swagger UI: http://localhost:8000/docs 에서 수동 확인 가능.
- DB 없이 빠르게 확인만 하려면 테스트(`run-tests` 스킬)를 사용한다.
