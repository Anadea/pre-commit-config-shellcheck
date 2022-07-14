#!/usr/bin/env python
import os
import sys
from argparse import Namespace, ArgumentParser
from typing import Any, Dict, List, Tuple, Union

import yaml
from yaml.scanner import ScannerError
from yaml.resolver import BaseResolver
from yaml import Node, Loader, ScalarNode


__all__: List[str] = ["main", "Shellcheck"]


class CustomLoader(Loader):
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

        for node_key, _node_value in node.value:
            shadow_key_node = ScalarNode(
                tag=BaseResolver.DEFAULT_SCALAR_TAG, value="__line__" + node_key.value
            )
            shadow_value_node = ScalarNode(
                tag=BaseResolver.DEFAULT_SCALAR_TAG, value=node_key.__line__
            )
            node_pair_lst_for_appending.append((shadow_key_node, shadow_value_node))

        node.value += node_pair_lst_for_appending
        return super().construct_mapping(node=node, deep=deep)  # type: ignore


class Shellcheck:
    """YAML shellchecker for entry points."""

    def __init__(self):
        """Get command line args."""
        self.options: Namespace = self._get_options()

    def _get_options(self) -> Namespace:
        """
        Parse commandline options arguments.

        :return: parsed command line arguments
        :rtype: Namespace
        """
        parser: ArgumentParser = ArgumentParser(
            description="Tool for checking shell code in YAML entry points"
        )

        parser.add_argument(
            "path",
            nargs="?",
            default=".pre-commit-config.yaml",
            action="store",
            metavar="PATH",
            help="file to check",
        )

        options: Namespace = parser.parse_args()

        return options

    def _parse_file(
        self,
    ) -> Dict[str, List[Dict[str, Any]]]:  # noqa: SIM907
        """
        Parse requested file.

        :return: parsed YAML file
        :rtype: Dict[str, List[Dict[str, Any]]]
        """
        try:
            with open(self.options.path) as stream:
                file: Dict[str, Any] = yaml.load(stream=stream, Loader=CustomLoader)
        except FileNotFoundError:
            sys.stderr.write(f"No file {self.options.path} found")
            sys.exit(os.EX_OSFILE)
        except ScannerError:
            sys.stderr.write(f"{self.options.path} is not a YAML file")
            sys.exit(os.EX_IOERR)

        return file

    def _find_entries(  # noqa: CCR001
        self, yaml_file: Dict[str, Any]
    ) -> List[Dict[str, Tuple[int, str]]]:
        """
        Find all entries in provided YAML file.

        :param yaml_file: constructed mapping of read YAML file
        :type yaml_file: Dict[str, Any]
        :return: list of ids and entries with number of lines they are attached to
        :rtype: List[Dict[str, Tuple[int, str]]]
        """
        result: List[Dict[str, Tuple[int, str]]] = []
        for repository in yaml_file.get("repos", []):
            for hook in repository.get("hooks", []):
                if "entry" in hook:
                    result.append(
                        {
                            "id": (hook["__line__id"], hook["id"]),
                            "entry": (hook["__line__entry"], hook["entry"]),
                        }
                    )
        return result

    def list_entries(
        self,
    ) -> Union[List[Dict[str, Tuple[int, str]]], None]:  # noqa: SIM907
        """
        Parse requested file and find all entries in it.

        :return: list of ids and entries with number of lines
            they are attached to or None if no entries are found
        :rtype: Union[List[Dict[str, Tuple[int, str]]], None]
        """
        file = self._parse_file()
        if file:
            result = self._find_entries(file)
            if result:
                return result
        return None


def main() -> None:
    """Program main."""
    checker = Shellcheck()  # type: ignore
    sys.stdout.write(str(checker.list_entries()))


if __name__ == "__main__":

    main()
