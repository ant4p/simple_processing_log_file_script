from datetime import date
import pytest

from utils import get_search_dates


def test_none_input():
    assert get_search_dates() is None
    assert get_search_dates(None) is None


def test_single_date_string():
    result = get_search_dates("2023-01-15")
    assert result == [date(2023, 1, 15)]


def test_multiple_dates():
    result = get_search_dates(["2023-01-15", "2023-01-16"])
    assert result == [date(2023, 1, 15), date(2023, 1, 16)]


def test_invalid_date_format():
    result = get_search_dates("15-01-2023")
    assert result == {}


def test_mixed_valid_invalid_dates():
    result = get_search_dates(["2023-01-15", "invalid", "2023-01-16"])
    assert result == {}


@pytest.mark.parametrize(
    "input_date,expected",
    [
        pytest.param("2023-01-15", [date(2023, 1, 15)], id="valid_single_date"),
        pytest.param(
            ["2023-01-15", "2023-01-16"],
            [date(2023, 1, 15), date(2023, 1, 16)],
            id="valid_multiple_dates",
        ),
        pytest.param("2023/01/15", {}, id="invalid_format"),
        pytest.param(["2023-01-15", "2023/01/16"], {}, id="mixed_valid_invalid"),
        pytest.param("not-a-date", {}, id="not_a_date"),
        pytest.param(123, {}, id="integer_input"),
        pytest.param(["2023-01-15", 123], {}, id="mixed_with_integer"),
        pytest.param([], [], id="empty_list"),
        pytest.param(None, None, id="none_input"),
    ],
)
def test_parametrized_cases(input_date, expected):
    assert get_search_dates(input_date) == expected
