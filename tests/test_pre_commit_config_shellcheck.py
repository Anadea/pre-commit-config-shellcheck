from argparse import Namespace

import pytest
from pytest_mock import MockerFixture
from _pytest.capture import CaptureFixture
from pre_commit_config_shellcheck import Shellcheck


parsed_file = {  # noqa: ECE001
    "repos": [
        {
            "repo": "local",
            "hooks": [
                {
                    "id": "seed-isort-config",
                    "name": "seed-isort-config",
                    "stages": ["commit"],
                    "language": "system",
                    "pass_filenames": False,
                    "entry": "seed-isort-config",
                    "types": ["python"],
                    "__line__id": 4,
                    "__line__name": 5,
                    "__line__stages": 6,
                    "__line__language": 7,
                    "__line__pass_filenames": 8,
                    "__line__entry": 9,
                    "__line__types": 10,
                },
                {
                    "id": "removestar",
                    "name": "removestar",
                    "stages": ["commit"],
                    "language": "system",
                    "entry": "removestar -i ${NAME}",  # noqa: FS003
                    "types": ["python"],
                    "__line__id": 11,
                    "__line__name": 12,
                    "__line__stages": 13,
                    "__line__language": 14,
                    "__line__entry": 15,
                    "__line__types": 16,
                },
            ],
            "__line__repo": 2,
            "__line__hooks": 3,
        }
    ],
    "__line__repos": 1,
}


def test__get_options(mocker: MockerFixture) -> None:
    """
    _get_options method must return argparse namespace.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch(
        "sys.argv",
        ["pre_commit_config_shellcheck.py", "tests/data/.pre-commit-config.yaml"],
    )
    checker = Shellcheck()  # type: ignore

    assert isinstance(checker.options, Namespace)


def test__get_options__missing_path_option(mocker: MockerFixture) -> None:
    """
    _get_options method must return default path if not provided.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch("sys.argv", ["pre_commit_config_shellcheck.py"])

    checker = Shellcheck()  # type: ignore

    assert checker.options.path == ".pre-commit-config.yaml"


def test__parse_file(mocker: MockerFixture) -> None:
    """
    _get_entries method must return list of entries.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch(
        "sys.argv",
        ["pre_commit_config_shellcheck.py", "tests/data/.pre-commit-config.yaml"],
    )

    checker = Shellcheck()  # type: ignore

    assert checker._parse_file() == parsed_file


def test__parse_file__incorrect_path_option(
    mocker: MockerFixture, capsys: CaptureFixture  # type: ignore
) -> None:
    """
    _parse_file method must exit with file not found error.

    :param mocker: mock
    :type mocker: MockerFixture
    :param capsys: std output fixture
    :type capsys: CaptureFixture
    """
    mocker.patch("sys.argv", ["pre_commit_config_shellcheck.py", "test.yaml"])

    checker = Shellcheck()  # type: ignore
    with pytest.raises(SystemExit):
        checker._parse_file()

    captured = capsys.readouterr()
    assert captured.err == "No file test.yaml found"


def test__parse_file__empty(mocker: MockerFixture) -> None:
    """
    _get_entries method must return None.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch(
        "sys.argv",
        ["pre_commit_config_shellcheck.py", "tests/data/empty.yaml"],
    )

    checker = Shellcheck()  # type: ignore

    assert checker._parse_file() is None


def test__parse_file__incorrect_file_type(
    mocker: MockerFixture, capsys: CaptureFixture  # type: ignore
) -> None:
    """
    _parse_file method must exit with file is not YAML error.

    :param mocker: mock
    :type mocker: MockerFixture
    :param capsys: std output fixture
    :type capsys: CaptureFixture
    """
    mocker.patch("sys.argv", ["pre_commit_config_shellcheck.py", "tests/__init__.py"])

    checker = Shellcheck()  # type: ignore
    with pytest.raises(SystemExit):
        checker._parse_file()

    captured = capsys.readouterr()
    assert captured.err == "tests/__init__.py is not a YAML file"


def test__find_entries(mocker: MockerFixture) -> None:
    """
    _find_entries method must return list of entries.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch("sys.argv", ["pre_commit_config_shellcheck.py"])

    checker = Shellcheck()  # type: ignore

    assert checker._find_entries(parsed_file) == [
        {
            "entry": (9, "seed-isort-config"),
            "id": (4, "seed-isort-config"),
        },
        {
            "entry": (15, "removestar -i ${NAME}"),  # noqa: FS003
            "id": (11, "removestar"),
        },
    ]


def test__find_entries__empty(mocker: MockerFixture) -> None:
    """
    _find_entries method must return empty list.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch("sys.argv", ["pre_commit_config_shellcheck.py"])

    checker = Shellcheck()  # type: ignore

    assert checker._find_entries({}) == []


def test_list_entries(mocker: MockerFixture) -> None:
    """
    list_entries method must return list of entries.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch(
        "sys.argv",
        ["pre_commit_config_shellcheck.py", "tests/data/.pre-commit-config.yaml"],
    )

    checker = Shellcheck()  # type: ignore

    assert checker.list_entries() == [
        {
            "entry": (9, "seed-isort-config"),
            "id": (4, "seed-isort-config"),
        },
        {
            "entry": (15, "removestar -i ${NAME}"),  # noqa: FS003
            "id": (11, "removestar"),
        },
    ]


def test_list_entries__empty(mocker: MockerFixture) -> None:
    """
    list_entries method must return None.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch(
        "sys.argv", ["pre_commit_config_shellcheck.py", "tests/data/empty.yaml"]
    )

    checker = Shellcheck()  # type: ignore

    assert checker.list_entries() is None
