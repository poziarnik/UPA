from abc import ABC, abstractmethod
from typing import TypeVar


class DataSet(ABC):
    ...


Dataset_T = TypeVar("Dataset_T", bound=DataSet)
