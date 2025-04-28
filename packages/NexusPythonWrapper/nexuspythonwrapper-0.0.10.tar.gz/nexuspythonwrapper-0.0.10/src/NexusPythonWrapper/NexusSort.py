import json
from typing import Self

class NexusSort:
    def __init__(self) -> None:
        self._sort_params = []

    def sort(self, field: str, ascending: bool = True) -> Self:
        self._sort_params.append(
            {
                'field': field,
                'ascending': ascending
            }
        )
        return self

    def build(self, raw:bool = False) -> list[dict] | str:
        return self._sort_params if raw else json.dumps(self._sort_params)

    def __str__(self) -> str:
        return self.build()
