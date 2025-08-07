from display_reports import average_tabulate


def test_average_tabulate_basic():
    test_stats = {
        "/api": {"total": 10, "avg_response_time": 0.123456},
        "/home": {"total": 5, "avg_response_time": 0.234567},
    }

    result = average_tabulate(test_stats)

    assert "handler" in result
    assert "total" in result
    assert "avg_response_time" in result

    assert result.index("/home") < result.index("/api")

    assert "0.123" in result
    assert "0.235" in result


def test_average_tabulate_empty():
    result = average_tabulate({})
    assert "handler" in result
    assert "No data" not in result
