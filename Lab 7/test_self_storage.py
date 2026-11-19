import math

from hypothesis import given, settings, strategies as st
from self_storage import parse_rental, duration_average, payable_rent

# Inputs that are not plain text at all: None, numbers, lists, bytes...
non_text = st.none() | st.integers() | st.floats() | st.booleans() | st.binary() | st.lists(st.integers())

# Numbers rendered as text, including the awkward ones (nan, inf, huge, negative).
number_text = st.one_of(
    st.integers().map(str),
    st.floats(allow_nan=True, allow_infinity=True).map(str),
    st.sampled_from(["nan", "inf", "-inf", "1e400", "-0", "", " ", "abc", "1_000", "0x10"]),
)


# ---------------------------------------------------------------- parse_rental

@settings(max_examples=300)
@given(st.text() | st.none())
def test_parse_rental_no_crash(s):
    try:
        parse_rental(s)
    except Exception as e:
        assert False, f"parse_rental crashed with: {e!r}"


@given(non_text)
def test_parse_rental_non_text_no_crash(value):
    try:
        parse_rental(value)
    except Exception as e:
        assert False, f"parse_rental crashed with: {e!r}"


@given(st.text(), st.text(), st.text())
def test_parse_rental_extra_separators_no_crash(a, b, c):
    try:
        parse_rental(f"{a}:{b}:{c}")
    except Exception as e:
        assert False, f"parse_rental crashed with: {e!r}"


@given(st.text(), number_text)
def test_parse_rental_valid_result(unit, months):
    try:
        result = parse_rental(f"{unit}:{months}")
    except Exception as e:
        assert False, f"parse_rental crashed with: {e!r}"
    if result is not None:
        name, m = result
        assert name != "", "empty unit name accepted"
        assert math.isfinite(m), f"non-finite months accepted: {m}"
        assert m > 0, f"non-positive months accepted: {m}"


# ------------------------------------------------------------ duration_average

@settings(max_examples=300)
@given(st.text() | st.none())
def test_duration_average_no_crash(s):
    try:
        duration_average(s)
    except Exception as e:
        assert False, f"duration_average crashed with: {e!r}"


@given(non_text)
def test_duration_average_non_text_no_crash(value):
    try:
        duration_average(value)
    except Exception as e:
        assert False, f"duration_average crashed with: {e!r}"


@given(st.lists(number_text))
def test_duration_average_number_lists_no_crash(parts):
    try:
        duration_average(",".join(parts))
    except Exception as e:
        assert False, f"duration_average crashed with: {e!r}"


@given(st.lists(st.integers(min_value=1, max_value=600), min_size=1))
def test_duration_average_within_bounds(months):
    result = duration_average(",".join(map(str, months)))
    assert result is not None
    assert min(months) <= result <= max(months)


@given(st.lists(st.integers(max_value=0), min_size=1))
def test_duration_average_rejects_non_positive(months):
    try:
        result = duration_average(",".join(map(str, months)))
    except Exception as e:
        assert False, f"duration_average crashed with: {e!r}"
    assert result is None, f"non-positive months accepted: {months} -> {result}"


# ---------------------------------------------------------------- payable_rent

@settings(max_examples=300)
@given(st.text() | st.none())
def test_payable_rent_no_crash(s):
    try:
        payable_rent(s)
    except Exception as e:
        assert False, f"payable_rent crashed with: {e!r}"


@given(non_text)
def test_payable_rent_non_text_no_crash(value):
    try:
        payable_rent(value)
    except Exception as e:
        assert False, f"payable_rent crashed with: {e!r}"


@given(number_text, number_text)
def test_payable_rent_result_is_valid(rent, discount):
    try:
        result = payable_rent(f"{rent}|{discount}")
    except Exception as e:
        assert False, f"payable_rent crashed with: {e!r}"
    if result is not None:
        assert math.isfinite(result), f"non-finite rent returned: {result}"
        assert result >= 0, f"negative rent returned: {result}"


@given(st.floats(min_value=0, max_value=1e6), st.floats(min_value=0, max_value=1e6))
def test_payable_rent_never_exceeds_taxed_rent(rent, discount):
    result = payable_rent(f"{rent}|{discount}")
    assert result is not None
    assert 0 <= result <= round(rent * 1.18, 2) + 0.01
