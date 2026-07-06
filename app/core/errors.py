"""검증 오류 메시지 한글화 공용 헬퍼.

Pydantic 검증 오류를 원문(영어) 번역이 아니라 **오류 타입 코드 기반**으로
한글 문구를 매핑한다. 파일 업로드 행 오류와 API 요청 검증(422)에서 공통으로 사용한다.
"""

from collections.abc import Sequence
from typing import Any

# 필드명 → 사용자용 한글 라벨
FIELD_LABELS: dict[str, str] = {
    "name": "상품명",
    "description": "설명",
    "price": "가격",
    "quantity": "수량",
    "skip": "skip",
    "limit": "limit",
}


def _field_label(loc: Sequence[Any]) -> str:
    """오류 위치(loc)에서 사용자에게 보여줄 필드 라벨을 뽑는다.

    loc 예: ("body", "name") / ("name",) / ("query", "limit")
    """
    # 'body', 'query' 같은 위치 접두어를 제외한 마지막 문자열을 필드로 본다.
    fields = [p for p in loc if isinstance(p, str) and p not in ("body", "query", "path")]
    field = fields[-1] if fields else (str(loc[-1]) if loc else "값")
    return FIELD_LABELS.get(field, field)


def _fmt_num(value: Any) -> str:
    """정수로 떨어지는 숫자는 소수점 없이 표시 (0.0 → 0)."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def translate_error(err: Any) -> str:
    """Pydantic 오류 1건(dict/ErrorDetails)을 "라벨: 한글 사유" 문자열로 변환한다."""
    label = _field_label(err.get("loc", ()))
    ctx = err.get("ctx", {}) or {}
    etype = err.get("type", "")

    messages: dict[str, str] = {
        "missing": "필수 항목입니다",
        "string_too_short": f"최소 {ctx.get('min_length', 1)}자 이상이어야 합니다",
        "string_too_long": f"최대 {ctx.get('max_length', '')}자까지 가능합니다",
        "string_type": "문자열이어야 합니다",
        "greater_than_equal": f"{_fmt_num(ctx.get('ge', 0))} 이상이어야 합니다",
        "greater_than": f"{_fmt_num(ctx.get('gt', 0))}보다 커야 합니다",
        "less_than_equal": f"{_fmt_num(ctx.get('le', ''))} 이하여야 합니다",
        "int_parsing": "정수여야 합니다",
        "int_type": "정수여야 합니다",
        "float_parsing": "숫자여야 합니다",
        "float_type": "숫자여야 합니다",
        "decimal_parsing": "숫자여야 합니다",
        "value_error": "값이 올바르지 않습니다",
    }
    # 매핑에 없으면 원문 메시지로 폴백 (최소한 정보는 유지)
    reason = messages.get(etype, err.get("msg", "값이 올바르지 않습니다"))
    return f"{label}: {reason}"


def summarize_errors(errors: Sequence[Any]) -> str:
    """여러 오류를 한 줄(; 구분)로 요약한다. (파일 업로드 행 오류용)"""
    return "; ".join(translate_error(e) for e in errors)
