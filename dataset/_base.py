from pprint import pprint
from typing import Any, Protocol, TypeVar

import jmespath
import requests


def download_geojson(url: str) -> dict[str, Any]:
    response = requests.get(url)

    if response.status_code != 200:
        raise RuntimeError("Unable to download data!")

    return response.json()


# https://github.com/Ades551/flight-record/blob/main/backend/threads/spokendata.py#L24
def find_in_json_object(
    json_obj: dict | list, *expression_paths: str
) -> list[tuple[Any, ...]]:
    """Finds all occurrences in an object of type json.

    Args:
        json_obj (dict | list): JSON-like object
        *expression_paths (str): regex for the desired path

    Returns:
        list[tuple[Any, ...]]: List of all occurrences
    """
    # construct expression
    expression = f"[{', '.join(expression_paths)}]"
    if isinstance(json_obj, list):
        expression = f"[*].{expression}"

    result: list[list[Any]] = jmespath.search(expression, json_obj)

    # return only values that are valid
    return [(values) for values in result if None not in values]


class DataSet(Protocol):
    def close(self) -> None:
        ...

    def process_data(self) -> None:
        ...


Dataset_T = TypeVar("Dataset_T", bound=DataSet)
