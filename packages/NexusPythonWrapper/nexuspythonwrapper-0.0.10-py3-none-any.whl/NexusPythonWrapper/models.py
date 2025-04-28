import json
from typing import Dict, List

class Result:
    def __init__(self, status_code: int, message: str = '', result: List[Dict] = None, metadata: dict = None):
        self.status_code = status_code
        self.message = message
        self.result = result if result else []
        self.metadata = metadata if metadata else {}

    def extend(self, rows: List[Dict] | 'Result'):
        if isinstance(rows, list):
            self.result.extend(rows)

        if isinstance(rows, Result):
            self.result.extend(rows.result)
            self.metadata.update(rows.metadata)

    def __str__(self):
        return json.dumps(
            {
                'status_code': self.status_code,
                'message': self.message,
                'result': self.result,
                'metadata': self.metadata
            }, indent=4
        )