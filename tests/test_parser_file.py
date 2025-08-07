import argparse
import pytest

from parser_file import create_parser


@pytest.fixture
def parser_fixture():
    return create_parser()


def test_create_parser(parser_fixture):
    assert isinstance(parser_fixture, argparse.ArgumentParser)
    assert parser_fixture.description == "parser"


def test_file_arg(parser_fixture):
    with pytest.raises(SystemExit):
        parser_fixture.parse_args([])

    args = parser_fixture.parse_args(["--file", "data.txt"])
    assert args.file == ["data.txt"]

    args = parser_fixture.parse_args(["-f", "f1.txt", "f2.txt"])
    assert args.file == ["f1.txt", "f2.txt"]

    for action in parser_fixture._get_optional_actions():
        if "--file" in action.option_strings:
            assert action.required is True
            assert action.nargs == "+"
            assert action.help == "Files for processing"
            assert "-f" in action.option_strings
            return

    pytest.fail("Аргумент --file не найден в парсере")


def test_report_arg(parser_fixture):
    report_arg = next(
        action
        for action in parser_fixture._actions
        if "--report" in action.option_strings
    )

    assert report_arg.required is False
    assert report_arg.nargs is None
    assert report_arg.help == "Enter report"


def test_date_args(parser_fixture):
    date_arg = next(
        action
        for action in parser_fixture._actions
        if "--date" in action.option_strings
    )

    assert date_arg.required is False
    assert date_arg.nargs == "+"
    assert date_arg.help == "Enter day"
    assert "-d" in date_arg.option_strings
    assert "--date" in date_arg.option_strings
    missed_date = parser_fixture.parse_args(["-f", "file.txt"])
    assert missed_date.date is None


@pytest.mark.parametrize(
    "args,expected",
    [
        (["-f", "file.txt"], {"file": ["file.txt"], "report": None, "date": None}),
        (
            ["--file", "f1", "f2", "-r", "rep"],
            {"file": ["f1", "f2"], "report": "rep", "date": None},
        ),
        (
            ["-f", "data.txt", "--date", "2023-01-01", "2023-01-02"],
            {
                "file": ["data.txt"],
                "report": None,
                "date": ["2023-01-01", "2023-01-02"],
            },
        ),
    ],
)
def test_argument_parsing(args, expected):
    parser = create_parser()
    result = parser.parse_args(args)

    assert result.file == expected["file"]
    assert result.report == expected["report"]
    assert result.date == expected["date"]
