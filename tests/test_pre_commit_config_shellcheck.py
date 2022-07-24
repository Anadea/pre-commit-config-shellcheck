from argparse import Namespace
from typing import Any, Dict, List
from subprocess import TimeoutExpired

import pytest
from pytest_mock import MockerFixture
from _pytest.capture import CaptureFixture
from pre_commit_config_shellcheck import Shellcheck


__all__: List[str] = []


def test__get_options(mocker: MockerFixture) -> None:
    """
    _get_options method must return argparse namespace.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch(
        "sys.argv",
        ["pre_commit_config_shellcheck.py", "tests/fixtures/.pre-commit-config.yaml"],
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


def test__parse_file(mocker: MockerFixture, parsed_file: Dict[str, Any]) -> None:
    """
    _get_entries method must return list of entries.

    :param mocker: mock
    :type mocker: MockerFixture
    :param parsed_file: parsed file fixture
    :type parsed_file: Dict[str, Any]
    """
    mocker.patch(
        "sys.argv",
        ["pre_commit_config_shellcheck.py", "tests/fixtures/.pre-commit-config.yaml"],
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
    assert captured.err == "No file test.yaml found\n"


def test__parse_file__empty(mocker: MockerFixture) -> None:
    """
    _get_entries method must return None.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch(
        "sys.argv",
        [
            "pre_commit_config_shellcheck.py",
            "tests/fixtures/.pre-commit-config--empty.yaml",
        ],
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
    assert captured.err == "tests/__init__.py is not a YAML file\n"


def test__find_entries(mocker: MockerFixture, parsed_file: Dict[str, Any]) -> None:
    """
    _find_entries method must return list of entries.

    :param mocker: mock
    :type mocker: MockerFixture
    :param parsed_file: parsed file fixture
    :type parsed_file: Dict[str, Any]
    """
    mocker.patch("sys.argv", ["pre_commit_config_shellcheck.py"])

    checker = Shellcheck()  # type: ignore

    assert checker._find_entries(parsed_file) == [
        {
            "entry": {"line": 9, "entry": "seed-isort-config\nsleep infinity\n"},
            "id": {"line": 4, "id": "seed-isort-config"},
        },
        {
            "entry": {"line": 17, "entry": "removestar -i ${NAME}"},  # noqa: FS003
            "id": {"line": 13, "id": "removestar"},
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


def test__find_entries__string(
    mocker: MockerFixture, capsys: CaptureFixture  # type: ignore
) -> None:
    """
    _find_entries method must exit with incorrect format error.

    :param mocker: mock
    :type mocker: MockerFixture
    :param capsys: std output fixture
    :type capsys: CaptureFixture
    """
    mocker.patch(
        "sys.argv",
        [
            "pre_commit_config_shellcheck.py",
            "tests/fixtures/.pre-commit-config--string.yaml",
        ],
    )

    checker = Shellcheck()  # type: ignore

    with pytest.raises(SystemExit):
        checker._find_entries(checker._parse_file())

    captured = capsys.readouterr()
    assert (
        captured.err
        == "An error happened while checking tests/fixtures/.pre-commit-config--string.yaml file: incorrect format\n"  # noqa: E501, W503
    )


def test__list_entries(mocker: MockerFixture) -> None:
    """
    _list_entries method must return list of entries.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch(
        "sys.argv",
        ["pre_commit_config_shellcheck.py", "tests/fixtures/.pre-commit-config.yaml"],
    )

    checker = Shellcheck()  # type: ignore

    assert checker._list_entries() == [
        {
            "entry": {"line": 9, "entry": "seed-isort-config\nsleep infinity\n"},
            "id": {"line": 4, "id": "seed-isort-config"},
        },
        {
            "entry": {"line": 17, "entry": "removestar -i ${NAME}"},  # noqa: FS003
            "id": {"line": 13, "id": "removestar"},
        },
    ]


def test__list_entries__bad_format(mocker: MockerFixture) -> None:
    """
    _list_entries method must return None.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch(
        "sys.argv",
        [
            "pre_commit_config_shellcheck.py",
            "tests/fixtures/.pre-commit-config--wrong.yaml",
        ],
    )

    checker = Shellcheck()  # type: ignore

    assert checker._list_entries() == []


def test__list_entries__empty(mocker: MockerFixture) -> None:
    """
    _list_entries method must return None.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch(
        "sys.argv",
        [
            "pre_commit_config_shellcheck.py",
            "tests/fixtures/.pre-commit-config--empty.yaml",
        ],
    )

    checker = Shellcheck()  # type: ignore

    assert checker._list_entries() == []


def test__write_output(
    mocker: MockerFixture, capsys: CaptureFixture  # type: ignore
) -> None:
    """
    _check_entries method must write in stdout warning in entrypoint.

    :param mocker: mock
    :type mocker: MockerFixture
    :param capsys: std output fixture
    :type capsys: CaptureFixture
    """
    mocker.patch(
        "sys.argv",
        [
            "pre_commit_config_shellcheck.py",
            "tests/fixtures/.pre-commit-config.yaml",
        ],
    )

    entry = {
        "id": {"line": 13, "id": "removestar"},
        "entry": {"line": 17, "entry": "removestar -i ${NAME}"},  # noqa: FS003
    }
    output = """
In entry "removestar" line 2:
removestar -i ${NAME}
              ^-----^ SC2086: Double quote to prevent globbing and word splitting.

Did you mean: \nremovestar -i "${NAME}"

For more information:
  https://www.shellcheck.net/wiki/SC2086 -- Double quote to prevent globbing ...
"""

    checker = Shellcheck()  # type: ignore
    checker._write_output(entry=entry, output=output)  # type: ignore

    captured = capsys.readouterr()
    expected = """
In entry "removestar" on line 17:
removestar -i ${NAME}
              ^-----^ SC2086: Double quote to prevent globbing and word splitting.

Did you mean: \nremovestar -i "${NAME}"

For more information:
  https://www.shellcheck.net/wiki/SC2086 -- Double quote to prevent globbing ...
"""
    assert captured.out == expected


def test__check_entries(
    mocker: MockerFixture, capsys: CaptureFixture  # type: ignore
) -> None:
    """
    _check_entries method must write in stdout warning in entrypoint.

    :param mocker: mock
    :type mocker: MockerFixture
    :param capsys: std output fixture
    :type capsys: CaptureFixture
    """
    mocker.patch(
        "sys.argv",
        [
            "pre_commit_config_shellcheck.py",
            "tests/fixtures/.pre-commit-config.yaml",
        ],
    )

    checker = Shellcheck()  # type: ignore
    checker._check_entries()

    captured = capsys.readouterr()
    expected = """
In entry "removestar" on line 17:
removestar -i ${NAME}
              ^-----^ SC2086: Double quote to prevent globbing and word splitting.

Did you mean: \nremovestar -i "${NAME}"

For more information:
  https://www.shellcheck.net/wiki/SC2086 -- Double quote to prevent globbing ...
"""
    assert captured.out == expected


def test__check_entries__stderr(
    mocker: MockerFixture, capsys: CaptureFixture  # type: ignore
) -> None:
    """
    _check_entries method must return None.

    :param mocker: mock
    :type mocker: MockerFixture
    :param capsys: std output fixture
    :type capsys: CaptureFixture
    """
    mocker.patch(
        "sys.argv",
        [
            "pre_commit_config_shellcheck.py",
            "tests/fixtures/.pre-commit-config.yaml",
        ],
    )
    mocker.patch(
        "subprocess.Popen.communicate", return_value=(b"", b"Some text returned")
    )

    checker = Shellcheck()  # type: ignore
    with pytest.raises(SystemExit):
        checker._check_entries()

    captured = capsys.readouterr()
    assert (
        captured.err
        == "Failed to check entrypoint seed-isort-config on line 9: Some text returned"  # noqa: W503, E501
    )


def test__check_entries__timeout(
    mocker: MockerFixture, capsys: CaptureFixture  # type: ignore
) -> None:
    """
    _check_entries method must return None.

    :param mocker: mock
    :type mocker: MockerFixture
    :param capsys: std output fixture
    :type capsys: CaptureFixture
    """
    mocker.patch(
        "sys.argv",
        [
            "pre_commit_config_shellcheck.py",
            "tests/fixtures/.pre-commit-config.yaml",
        ],
    )
    mocker.patch(
        "subprocess.Popen.communicate",
        side_effect=TimeoutExpired(cmd="", timeout=0, stderr="Failure"),
    )

    checker = Shellcheck()  # type: ignore
    with pytest.raises(SystemExit):
        checker._check_entries()

    captured = capsys.readouterr()
    assert (
        captured.err
        == "Failed to check entrypoint seed-isort-config on line 9: Failure"  # noqa: W503, E501
    )


def test__check_entries__wrong_shellcheck(
    mocker: MockerFixture, capsys: CaptureFixture  # type: ignore
) -> None:
    """
    _check_entries method must write in stdout warning in entrypoint.

    :param mocker: mock
    :type mocker: MockerFixture
    :param capsys: std output fixture
    :type capsys: CaptureFixture
    """
    mocker.patch(
        "sys.argv",
        [
            "pre_commit_config_shellcheck.py",
            "tests/fixtures/.pre-commit-config.yaml",
            "-s",
            "/test/shellcheck",
        ],
    )

    checker = Shellcheck()  # type: ignore

    with pytest.raises(SystemExit):
        checker._check_entries()

    captured = capsys.readouterr()
    expected = "No shellcheck found: '/test/shellcheck'\n"
    assert captured.err == expected
