import json
import os
from datetime import datetime
from tempfile import TemporaryDirectory

import pytest

from reports import average_report


@pytest.fixture
def setup_test_files():
    with TemporaryDirectory() as temp_dir:
        file1 = os.path.join(temp_dir, "log1.log")
        file2 = os.path.join(temp_dir, "log2.log")

        with open(file1, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "@timestamp": "2023-01-15T12:00:00+0000",
                    "url": "/api",
                    "response_time": 0.2,
                },
                f,
            )
            f.write("\n")
            json.dump(
                {
                    "@timestamp": "2023-01-15T12:01:00+0000",
                    "url": "/api",
                    "response_time": 0.3,
                },
                f,
            )

        with open(file2, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "@timestamp": "2023-01-16T12:00:00+0000",
                    "url": "/home",
                    "response_time": 0.1,
                },
                f,
            )

        yield [file1, file2]


def test_average_report_with_valid_data(setup_test_files):
    original_get_files_list = average_report.__globals__["get_files_list"]
    original_get_search_dates = average_report.__globals__["get_search_dates"]

    try:
        average_report.__globals__["get_files_list"] = lambda x: setup_test_files
        average_report.__globals__["get_search_dates"] = lambda x: None

        result = average_report("dummy_path")

        assert "/api" in result
        assert result["/api"]["total"] == 2
        assert result["/api"]["avg_response_time"] == pytest.approx(0.5)
        assert result["/home"]["total"] == 1
        assert result["/home"]["avg_response_time"] == pytest.approx(0.1)

    finally:
        average_report.__globals__["get_files_list"] = original_get_files_list
        average_report.__globals__["get_search_dates"] = original_get_search_dates


def test_with_date_filter(setup_test_files):
    test_date = datetime.strptime("2023-01-15", "%Y-%m-%d").date()

    original_get_files_list = average_report.__globals__["get_files_list"]
    original_get_search_dates = average_report.__globals__["get_search_dates"]

    try:
        average_report.__globals__["get_files_list"] = lambda x: setup_test_files
        average_report.__globals__["get_search_dates"] = lambda x: [test_date]

        result = average_report("dummy_path", date="2023-01-15")

        assert "/api" in result
        assert "/home" not in result
    finally:
        average_report.__globals__["get_files_list"] = original_get_files_list
        average_report.__globals__["get_search_dates"] = original_get_search_dates


def test_with_bad_json(tmp_path):
    bad_file = tmp_path / "bad.log"
    bad_file.write_text("invalid json\n")

    original_get_files_list = average_report.__globals__["get_files_list"]

    try:
        average_report.__globals__["get_files_list"] = lambda x: [str(bad_file)]

        result = average_report("bad_path")
        assert result == {}

    finally:
        average_report.__globals__["get_files_list"] = original_get_files_list


def test_file_not_found():
    original_get_files_list = average_report.__globals__["get_files_list"]

    try:
        average_report.__globals__["get_files_list"] = lambda x: ["nonexistent.log"]

        result = average_report("missing")
        assert result == {}

    finally:
        average_report.__globals__["get_files_list"] = original_get_files_list


def test_without_url(tmp_path):
    no_url_file = tmp_path / "no_url.log"
    with no_url_file.open("w") as f:
        json.dump({"@timestamp": "2023-01-15T12:00:00+0000", "response_time": 0.2}, f)

    original_get_files_list = average_report.__globals__["get_files_list"]

    try:
        average_report.__globals__["get_files_list"] = lambda x: [str(no_url_file)]

        result = average_report("no_url_path")
        assert result == {}

    finally:
        average_report.__globals__["get_files_list"] = original_get_files_list
