from hypothesis import given, strategies as st
from course_registration_parser import format_course_code, total_credits, parse_student_record

@given(st.text() | st.none())
def test_format_course_code_no_crash(s):
    try:
        result = format_course_code(s)
        assert result is None or isinstance(result, str)
    except Exception as e:
        assert False, f"format_course_code crashed with: {type(e).__name__}: {e}"

@given(st.text() | st.none())
def test_total_credits_no_crash(s):
    try:
        result = total_credits(s)
        assert isinstance(result, int)
    except Exception as e:
        assert False, f"total_credits crashed with: {type(e).__name__}: {e}"

@given(st.text() | st.none())
def test_parse_student_record_no_crash(s):
    try:
        result = parse_student_record(s)
        assert result is None or isinstance(result, dict)
    except Exception as e:
        assert False, f"parse_student_record crashed with: {type(e).__name__}: {e}"
