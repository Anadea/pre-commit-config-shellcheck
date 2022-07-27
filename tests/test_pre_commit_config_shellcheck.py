from argparse import Namespace
from typing import Any, Dict, List
from subprocess import TimeoutExpired

import pytest
from pytest_mock import MockerFixture
from _pytest.capture import CaptureFixture
from pre_commit_config_shellcheck import PreCommitConfigShellcheck


__all__: List[str] = [
    "test_pre_commit_config_shellcheck___list_entries",
    "test_pre_commit_config_shellcheck___list_entries__bad_format",
    "test_pre_commit_config_shellcheck___create_output",
    "test_pre_commit_config_shellcheck___write_output__empty",
    "test_pre_commit_config_shellcheck___write_output",
    "test_pre_commit_config_shellcheck___check_entries__wrong_shellcheck",
    "test_pre_commit_config_shellcheck___list_entries__empty",
    "test_pre_commit_config_shellcheck___check_entries__stderr",
    "test_pre_commit_config_shellcheck___check_entries__timeout",
    "test_pre_commit_config_shellcheck___find_entries__empty",
    "test_pre_commit_config_shellcheck___find_entries__string",
    "test_pre_commit_config_shellcheck___parse_file",
    "test_pre_commit_config_shellcheck___parse_file__incorrect_path_option",
    "test_pre_commit_config_shellcheck___parse_file__empty",
    "test_pre_commit_config_shellcheck___parse_file__incorrect_file_type",
    "test_pre_commit_config_shellcheck___get_options__missing_path_option",
    "test_pre_commit_config_shellcheck___find_entries",
    "test_pre_commit_config_shellcheck___check_entries",
    "test_pre_commit_config_shellcheck___get_options",
]


def test_pre_commit_config_shellcheck___get_options(mocker: MockerFixture) -> None:
    """
    _get_options method must return argparse namespace.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch(
        "sys.argv",
        ["pre_commit_config_shellcheck.py", "tests/fixtures/.pre-commit-config.yaml"],
    )
    checker = PreCommitConfigShellcheck()  # type: ignore

    assert isinstance(checker.options, Namespace)


def test_pre_commit_config_shellcheck___get_options__missing_path_option(
    mocker: MockerFixture,
) -> None:
    """
    _get_options method must return default path if not provided.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch("sys.argv", ["pre_commit_config_shellcheck.py"])

    checker = PreCommitConfigShellcheck()  # type: ignore

    assert checker.options.path == ".pre-commit-config.yaml"


def test_pre_commit_config_shellcheck___parse_file(
    mocker: MockerFixture, parsed_file: Dict[str, Any]
) -> None:
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

    checker = PreCommitConfigShellcheck()  # type: ignore

    assert checker._parse_file() == parsed_file


def test_pre_commit_config_shellcheck___parse_file__incorrect_path_option(
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

    checker = PreCommitConfigShellcheck()  # type: ignore
    with pytest.raises(SystemExit):
        checker._parse_file()

    captured = capsys.readouterr()
    assert captured.err == "No file test.yaml found\n"


def test_pre_commit_config_shellcheck___parse_file__empty(
    mocker: MockerFixture,
) -> None:
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

    checker = PreCommitConfigShellcheck()  # type: ignore

    assert checker._parse_file() is None


def test_pre_commit_config_shellcheck___parse_file__incorrect_file_type(
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

    checker = PreCommitConfigShellcheck()  # type: ignore
    with pytest.raises(SystemExit):
        checker._parse_file()

    captured = capsys.readouterr()
    assert captured.err == "tests/__init__.py is not a YAML file\n"


def test_pre_commit_config_shellcheck___find_entries(
    mocker: MockerFixture, parsed_file: Dict[str, Any]
) -> None:
    """
    _find_entries method must return list of entries.

    :param mocker: mock
    :type mocker: MockerFixture
    :param parsed_file: parsed file fixture
    :type parsed_file: Dict[str, Any]
    """
    mocker.patch("sys.argv", ["pre_commit_config_shellcheck.py"])

    checker = PreCommitConfigShellcheck()  # type: ignore

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


def test_pre_commit_config_shellcheck___find_entries__empty(
    mocker: MockerFixture,
) -> None:
    """
    _find_entries method must return empty list.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch("sys.argv", ["pre_commit_config_shellcheck.py"])

    checker = PreCommitConfigShellcheck()  # type: ignore

    assert checker._find_entries({}) == []


def test_pre_commit_config_shellcheck___find_entries__string(
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

    checker = PreCommitConfigShellcheck()  # type: ignore

    with pytest.raises(SystemExit):
        checker._find_entries(checker._parse_file())

    captured = capsys.readouterr()
    assert (
        captured.err
        == "An error happened while checking tests/fixtures/.pre-commit-config--string.yaml file: incorrect format\n"  # noqa: E501, W503
    )


def test_pre_commit_config_shellcheck___list_entries(mocker: MockerFixture) -> None:
    """
    _list_entries method must return list of entries.

    :param mocker: mock
    :type mocker: MockerFixture
    """
    mocker.patch(
        "sys.argv",
        ["pre_commit_config_shellcheck.py", "tests/fixtures/.pre-commit-config.yaml"],
    )

    checker = PreCommitConfigShellcheck()  # type: ignore

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


def test_pre_commit_config_shellcheck___list_entries__bad_format(
    mocker: MockerFixture,
) -> None:
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

    checker = PreCommitConfigShellcheck()  # type: ignore

    assert checker._list_entries() == []


def test_pre_commit_config_shellcheck___list_entries__empty(
    mocker: MockerFixture,
) -> None:
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

    checker = PreCommitConfigShellcheck()  # type: ignore

    assert checker._list_entries() == []


def test_pre_commit_config_shellcheck___create_output(mocker: MockerFixture) -> None:
    """
    _create_output method must return process output and desired exit code.

    :param mocker: mock
    :type mocker: MockerFixture
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

    checker = PreCommitConfigShellcheck()  # type: ignore
    expected = (
        """
In entry "removestar" on line 17:
removestar -i ${NAME}
              ^-----^ SC2086: Double quote to prevent globbing and word splitting.

Did you mean: \nremovestar -i "${NAME}"

For more information:
  https://www.shellcheck.net/wiki/SC2086 -- Double quote to prevent globbing ...
""",
        checker.EXIT_CODE_ERROR,
    )

    assert checker._create_output(entry=entry, output=output) == expected  # type: ignore  # noqa: E501


def test_pre_commit_config_shellcheck___write_output(
    mocker: MockerFixture, capsys: CaptureFixture  # type: ignore
) -> None:
    """
    _write_output method must write in stdout all warnings in entrypoints and exit with exit code.

    :param mocker: mock
    :type mocker: MockerFixture
    :param capsys: std output fixture
    :type capsys: CaptureFixture
    """  # noqa: E501
    mocker.patch(
        "sys.argv",
        [
            "pre_commit_config_shellcheck.py",
            "tests/fixtures/.pre-commit-config.yaml",
        ],
    )
    checker = PreCommitConfigShellcheck()  # type: ignore
    output = """
In entry "removestar" on line 17:
removestar -i ${NAME}
              ^-----^ SC2086: Double quote to prevent globbing and word splitting.

Did you mean: \nremovestar -i "${NAME}"

For more information:
  https://www.shellcheck.net/wiki/SC2086 -- Double quote to prevent globbing ...
"""
    code = checker.EXIT_CODE_ERROR
    with pytest.raises(SystemExit):
        checker._write_output(output=output, code=code)

    captured = capsys.readouterr()
    assert captured.out == output


def test_pre_commit_config_shellcheck___write_output__empty(
    mocker: MockerFixture, capsys: CaptureFixture  # type: ignore
) -> None:
    """
    _write_output method must exit with no errors.

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
    checker = PreCommitConfigShellcheck()  # type: ignore
    output = ""
    code = 0
    with pytest.raises(SystemExit):
        checker._write_output(output=output, code=code)

    captured = capsys.readouterr()
    assert captured.out == output


def test_pre_commit_config_shellcheck___check_entries(
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

    checker = PreCommitConfigShellcheck()  # type: ignore
    with pytest.raises(SystemExit):
        checker._check_entries()

    captured = capsys.readouterr()
    expected = """
In entry "removestar" on line 17:
removestar -i ${NAME}
              ^-----^ SC2086 (info): Double quote to prevent globbing and word splitting.

Did you mean: \nremovestar -i "${NAME}"

For more information:
  https://www.shellcheck.net/wiki/SC2086 -- Double quote to prevent globbing ...
"""  # noqa: E501
    assert captured.out == expected


def test_pre_commit_config_shellcheck___check_entries__stderr(
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

    checker = PreCommitConfigShellcheck()  # type: ignore
    with pytest.raises(SystemExit):
        checker._check_entries()

    captured = capsys.readouterr()
    assert (
        captured.err
        == "Failed to check entrypoint seed-isort-config on line 9: Some text returned"  # noqa: W503, E501
    )


def test_pre_commit_config_shellcheck___check_entries__timeout(
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

    checker = PreCommitConfigShellcheck()  # type: ignore
    with pytest.raises(SystemExit):
        checker._check_entries()

    captured = capsys.readouterr()
    assert (
        captured.err
        == "Failed to check entrypoint seed-isort-config on line 9: Failure"  # noqa: W503, E501
    )


def test_pre_commit_config_shellcheck___check_entries__wrong_shellcheck(
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

    checker = PreCommitConfigShellcheck()  # type: ignore

    with pytest.raises(SystemExit):
        checker._check_entries()

    captured = capsys.readouterr()
    expected = "No shellcheck found: '/test/shellcheck'\n"
    assert captured.err == expected
