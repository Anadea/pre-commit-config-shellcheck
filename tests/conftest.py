from typing import Any, Dict, List

import pytest


__all__: List[str] = ["parsed_file"]


@pytest.fixture
def parsed_file() -> Dict[str, Any]:
    """
    Create parsed YAML file fixture.

    :return: example of parsed file
    :rtype: Dict[str, Any]
    """
    return {  # noqa: ECE001
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
                        "entry": "seed-isort-config\nsleep infinity\n",
                        "types": ["python"],
                        "__line__id": 4,
                        "__line__name": 5,
                        "__line__stages": 6,
                        "__line__language": 7,
                        "__line__pass_filenames": 8,
                        "__line__entry": 9,
                        "__line__types": 12,
                    },
                    {
                        "id": "removestar",
                        "name": "removestar",
                        "stages": ["commit"],
                        "language": "system",
                        "entry": "removestar -i ${NAME}",  # noqa: FS003
                        "types": ["python"],
                        "__line__id": 13,
                        "__line__name": 14,
                        "__line__stages": 15,
                        "__line__language": 16,
                        "__line__entry": 17,
                        "__line__types": 18,
                    },
                ],
                "__line__repo": 2,
                "__line__hooks": 3,
            }
        ],
        "__line__repos": 1,
    }
