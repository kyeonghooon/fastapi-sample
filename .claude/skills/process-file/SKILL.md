---
name: process-file
description: Use when 엑셀, CSV, 파일 업로드, 컬럼 매핑, 행별 검증, 일괄 저장, 업로드 API를 추가하거나 수정해야 할 때.
---

# process-file

엑셀/CSV 파일 처리 로직을 추가/확장하는 절차. 핵심 로직은
`app/services/file_processor.py`, 엔드포인트는 `app/api/routes/files.py`에 있다.

## 시작 전 확인

- `app/services/file_processor.py`, `app/api/routes/files.py`, `app/crud/item.py`, `tests/test_files.py`가 실제로 있는지 확인한다.
- 파일 구조가 문서와 다르면 현재 구조를 우선하고, 없는 파일을 있다고 가정하지 않는다.
- 라우터는 얇게 유지하고, 파싱·검증은 서비스에 둔다.

## 구조 이해

- `parse_items_file(filename, content) -> ParseResult` : 파싱·행별 검증
  - `ParseResult.items` (유효 행 → `ItemCreate`), `ParseResult.errors` (`RowError`)
  - 파일 전체 오류(형식 미지원/필수 컬럼 누락)는 `FileProcessingError` 발생
- 엔드포인트 `POST /items/upload` : 파싱 → `crud.bulk_create_items` → 요약 응답

## 컬럼/검증 규칙 변경

`file_processor.py` 에서:
- 필수 컬럼: `REQUIRED_COLUMNS` 수정
- 지원 확장자: `SUPPORTED_EXTENSIONS` 및 `_read_dataframe` 수정
- 행 변환/검증: `parse_items_file` 루프의 `ItemCreate(...)` 매핑 수정
  (값 정리는 `_clean_str`/`_clean_optional_str` 활용)
- 컬럼명 비교는 대소문자·공백 처리 방식이 기존 테스트와 맞는지 확인
- 잘못된 행은 가능한 한 행별 오류로 모으고, 파일 전체를 처리할 수 없는 경우만 `FileProcessingError` 사용

## 다른 엔티티용 업로드 추가 시

- `parse_<entity>_file` 함수를 유사 패턴으로 작성 (해당 스키마의 Create 사용)
- 해당 엔티티 crud에 `bulk_create_*` 추가
- `files.py`에 업로드 엔드포인트 추가 또는 엔티티별 라우트로 분리
- 응답 형식은 기존 `/items/upload`의 created/failed/errors 요약과 최대한 맞춘다.

## 검증 방법

- 정상 행 + 의도적 오류 행을 섞은 샘플로 테스트한다 (`sample_data/items.csv` 참고).
- `tests/test_files.py` 에 케이스 추가:
  - 정상 CSV/XLSX → created/failed 건수
  - 필수 컬럼 누락 → 400
  - 미지원 형식 → 400
  - 일부 행 실패 → 유효 행은 저장, 오류 행은 리포트
- `uv run pytest tests/test_files.py -v` 로 확인.
- 마무리 전 `uv run pytest -v` 및 `uv run ruff check .` 실행을 권장한다.
