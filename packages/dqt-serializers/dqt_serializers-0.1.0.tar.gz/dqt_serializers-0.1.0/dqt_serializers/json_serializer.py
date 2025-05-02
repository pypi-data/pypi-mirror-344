import json
from .base import Serializer
from typing import Dict, List, Union


class JsonSerializer(Serializer):
    def serialize(self, data: Union[Dict, List], path: str) -> None:
        try:
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
        except TypeError as e:
            raise ValueError(f"Invalid data type for JSON: {str(e)}")

    def deserialize(self, path: str) -> Union[Dict, List]:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")