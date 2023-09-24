from typing import Protocol, TypeVar


class DataSet(Protocol):
    def close(self) -> None:
        ...

    def process_data(self) -> None:
        ...


Dataset_T = TypeVar("Dataset_T", bound=DataSet)
