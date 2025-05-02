import pandas as pd
from .base import Serializer
from typing import Union


class CsvSerializer(Serializer):
    def serialize(self, data: Union[pd.DataFrame, list], path: str) -> None:
        if isinstance(data, pd.DataFrame):
            data.to_csv(path, index=False)
        elif isinstance(data, list):
            pd.DataFrame(data).to_csv(path, index=False)
        else:
            raise ValueError("Unsupported data type for CSV serialization")

    def deserialize(self, path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(path)
        except Exception as e:
            raise IOError(f"Failed to deserialize CSV: {str(e)}")
