#!/usr/bin/env python

import re
import sys
import tempfile
import subprocess  # nosec
from argparse import Namespace, ArgumentParser
from typing import Any, Dict, List, Tuple, Union

import yaml
from yaml.scanner import ScannerError
from yaml.resolver import BaseResolver
from yaml import Node, Loader, ScalarNode


__all__: List[str] = ["main", "PreCommitConfigShellcheck"]


# metadata
VERSION = (0, 3, 3)
__version__ = ".".join(map(str, VERSION))


class CustomYamlLoader(Loader):
    """Custom class for YAML loader."""

    def compose_node(
        self, parent: Union[Node, None], index: int  # noqa: SIM907
    ) -> Union[Node, None]:  # noqa: SIM907
        """
        Composes a YAML node and adds line number to it.

        :param parent: parent of the currently composing node
        :type parent: Union[Node, None]
        :param index: index of the node to composed
        :type index: int
        :return: constructed node with line number
        :rtype: Union[Node, None]
        """
        node = super().compose_node(parent=parent, index=index)
        node.__line__ = self.line + 1  # type: ignore

        return node

    def construct_mapping(self, node: Node, deep: bool = False) -> Dict[str, Any]:
        """
        Create mapping for node with providing line numbers for each node key.

        :param node: node to create mapping of
        :type node: Node
        :param deep: whether objects that are potentially generators are recursively
            being built or appended to the list to be resolved later on
        :type deep: bool
        :return: node mapping
        :rtype: Dict[str, Any]
        """
        node_pair_lst_for_appending = []

        for node_key, _ in node.value:
            shadow_key_node = ScalarNode(
                tag=BaseResolver.DEFAULT_SCALAR_TAG, value="__line__" + node_key.value
            )
            shadow_value_node = ScalarNode(
                tag=BaseResolver.DEFAULT_SCALAR_TAG, value=node_key.__line__
            )
            node_pair_lst_for_appending.append((shadow_key_node, shadow_value_node))

        node.value += node_pair_lst_for_appending

        return super().construct_mapping(node=node, deep=deep)  # type: ignore


class PreCommitConfigShellcheck:
    """Tool for shellchecking pre-commit config files."""

    EXIT_CODE_SUCCESS: int = 0
    EXIT_CODE_ERROR: int = 2
    EXIT_CODE_FILE_NOT_FOUND: int = 5

    def __init__(self):
        """Get command line args."""
        self.options: Namespace = self._get_options()

    @staticmethod
    def _get_options() -> Namespace:
        """
        Parse commandline options arguments.

        :return: parsed command line arguments
        :rtype: Namespace
        """
        parser: ArgumentParser = ArgumentParser(
            description="Tool for checking entry points in the pre-commit config with ShellCheck."  # noqa: E501
        )

        parser.add_argument(
            "path",
            nargs="?",
            default=".pre-commit-config.yaml",
            action="store",
            metavar="PATH",
            help="file to check",
        )
        parser.add_argument(
            "-s",
            "--shellcheck",
            action="store",
            dest="shellcheck",
            type=str,
            default="shellcheck",
            metavar="SHELLCHECK",
            help="ShellCheck path",
        )
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=f"{__version__}",
        )

        options: Namespace = parser.parse_args()

        return options

    def _parse_file(
        self,
    ) -> Dict[str, List[Dict[str, Any]]]:  # noqa: SIM907
        """
        Parse requested file.

        :return: parsed config
        :rtype: Dict[str, List[Dict[str, Any]]]
        """
        try:
            with open(self.options.path) as stream:
                file_: Dict[str, Any] = yaml.load(  # nosec  # noqa: DUO109
                    stream=stream, Loader=CustomYamlLoader
                )
        except FileNotFoundError:
            sys.stderr.write(f"No file {self.options.path} found\n")
            sys.exit(self.EXIT_CODE_FILE_NOT_FOUND)
        except ScannerError:
            sys.stderr.write(f"{self.options.path} is not a YAML file\n")
            sys.exit(self.EXIT_CODE_ERROR)

        return file_

    def _find_entries(  # noqa: CCR001
        self, data: Dict[str, Any]
    ) -> List[Dict[str, Dict[str, Union[int, str]]]]:
        """
        Find all entries in provided config.

        :param data: constructed mapping of file
        :type data: Dict[str, Any]
        :return: list of ids and entries with number of lines they are attached to
        :rtype: List[Dict[str, Dict[str, Union[int, str]]]]
        """
        result: List[Dict[str, Dict[str, Union[int, str]]]] = []
        try:
            for repository in data.get("repos", []):
                for hook in repository.get("hooks", []):
                    if "entry" in hook:
                        result.append(
                            {
                                "id": {"line": hook["__line__id"], "id": hook["id"]},
                                "entry": {
                                    "line": hook["__line__entry"],
                                    "entry": hook["entry"],
                                },
                            }
                        )
        except TypeError:
            sys.stderr.write(
                f"An error happened while checking {self.options.path} file: incorrect format\n"  # noqa: E501
            )
            sys.exit(self.EXIT_CODE_ERROR)

        return result

    def _list_entries(
        self,
    ) -> List[Dict[str, Dict[str, Union[int, str]]]]:  # noqa: SIM907
        """
        Parse requested file and find all entries in it.

        :return: list of ids and entries with number of lines they are attached to
        :rtype: List[Dict[str, Dict[str, Union[int, str]]]]
        """
        file = self._parse_file()
        if file:
            result = self._find_entries(file)
            if result:

                return result

        return []

    def _create_output(
        self, entry: Dict[str, Dict[str, Union[int, str]]], output: str
    ) -> Tuple[str, int]:
        """
        Edit and write shellcheck output.

        :param entry: entry data to insert into output
        :type entry: Dict[str, Dict[str, Union[int, str]]]
        :param output: base output to edit and process
        :type output: str
        :return: subprocess output with process exit code
        :rtype: Tuple[str, int]
        """
        # regular expression for finding line number from output text:
        # returns two groups: "line #" for output replacement and line number itself
        regular = re.findall(r"In entry \".*\" (?P<switch>line (?P<line>\d+))", output)
        if not regular:
            return output, self.EXIT_CODE_SUCCESS
        for line_number in regular:
            # subtract 2 because of number of lines difference
            # in temporary file and source file
            entry_line = int(entry["entry"]["line"])
            new_line_number = (entry_line + int(line_number[1])) - 2

            output = output.replace(
                line_number[0],
                f"on line {new_line_number}",
            )

        return output, self.EXIT_CODE_ERROR

    @staticmethod
    def _write_output(output: str, code: int) -> None:
        """
        Write whole tool output and exit with desired code.

        :param output: output to write in console:
        :type output: str
        :param code: exit code for the tool
        :type code: int
        """
        sys.stdout.write(output)
        sys.exit(code)

    def _check_entry_file(
        self,
        entry: Dict[str, Dict[str, Union[int, str]]],
        tmp,
    ) -> Tuple[bytes, bytes]:
        """
        Run a shellcheck command on temporary file.

        :param entry: entry data to insert into output
        :type entry: Dict[str, Dict[str, Union[int, str]]]
        :param tmp: created temporary file
        :type tmp: _TemporaryFileWrapper
        :return: process output
        :rtype: Tuple[bytes, bytes]
        """
        try:
            process = subprocess.Popen(  # nosec
                args=[self.options.shellcheck, tmp.name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except FileNotFoundError:
            sys.stderr.write(f"No shellcheck found: '{self.options.shellcheck}'\n")
            sys.exit(self.EXIT_CODE_FILE_NOT_FOUND)

        try:
            stdout, stderr = process.communicate()

        except subprocess.TimeoutExpired as err:
            sys.stderr.write(
                f"Failed to check entrypoint {entry['id']['id']} on line {entry['entry']['line']}: {err.stderr}"  # noqa: E501
            )
            sys.exit(self.EXIT_CODE_ERROR)

        if stderr:
            sys.stderr.write(
                f"Failed to check entrypoint {entry['id']['id']} on line {entry['entry']['line']}: {stderr.decode('UTF-8')}"  # noqa: E501
            )
            sys.exit(self.EXIT_CODE_ERROR)

        return stdout, stderr

    def _check_entries(self) -> None:
        """Check the created file for possible entrypoints issues."""
        result = ""
        exit_ = self.EXIT_CODE_SUCCESS
        for entry in self._list_entries():
            with tempfile.NamedTemporaryFile("w+") as tmp:
                tmp.write("#!/bin/sh\n")
                tmp.write(str(entry["entry"]["entry"]))
                tmp.flush()

                stdout, _ = self._check_entry_file(entry, tmp)
                name = f"entry \"{entry['id']['id']}\""
                output = stdout.decode("utf-8").replace(tmp.name, name)

                output, code = self._create_output(entry=entry, output=output)
                result += output
                if code != self.EXIT_CODE_SUCCESS:
                    exit_ = code

        self._write_output(output=result, code=exit_)

    def check(self) -> None:
        """Check file for entrypoints and verify them."""
        self._check_entries()


def main() -> None:
    """Program main."""
    checker = PreCommitConfigShellcheck()  # type: ignore
    checker.check()


if __name__ == "__main__":
    main()
