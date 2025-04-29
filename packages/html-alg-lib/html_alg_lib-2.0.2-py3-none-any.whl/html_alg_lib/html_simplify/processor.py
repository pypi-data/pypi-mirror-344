from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from lxml import html


@dataclass
class DataPack:
    root: html.HtmlElement
    info: dict[str, Any]


class BaseProcess(ABC):
    def __init__(self, config: dict[str, Any]):
        self.config = config

    @classmethod
    def setup(self):
        pass

    @abstractmethod
    def apply(self, input_data: DataPack) -> DataPack:
        pass
