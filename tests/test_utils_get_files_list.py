import os
import pytest

from dotenv import load_dotenv

from utils import get_files_list

load_dotenv()

DEFAULT_DIRECTORY = os.getenv("DEFAULT_DIRECTORY")


@pytest.fixture
def files_fixture():
    return ["example1.log", "dir/example2.log", "example3.txt"]


def test_basic_file_paths(files_fixture):
    result = get_files_list(files_fixture)
    expected = [
        os.path.join(DEFAULT_DIRECTORY, "example1.log"),
        os.path.join(DEFAULT_DIRECTORY, "dir/example2.log"),
        os.path.join(DEFAULT_DIRECTORY, "example3.txt"),
    ]
    assert result == expected


@pytest.mark.parametrize(
    "input_files,expected",
    [
        (["single.file"], [os.path.join(DEFAULT_DIRECTORY, "single.file")]),
        (
            ["f1", "f2"],
            [
                os.path.join(DEFAULT_DIRECTORY, "f1"),
                os.path.join(DEFAULT_DIRECTORY, "f2"),
            ],
        ),
        (["path/to/file"], [os.path.join(DEFAULT_DIRECTORY, "path/to/file")]),
        ([], []),
    ],
)
def test_parametrized_cases(input_files, expected):
    assert get_files_list(input_files) == expected


def test_none_input():
    with pytest.raises(TypeError):
        get_files_list(None)


def test_non_string_elements():
    with pytest.raises(TypeError):
        get_files_list([123, "file.txt"])
