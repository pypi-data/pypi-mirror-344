import json
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Optional, Type, TypeVar
from xml.etree.ElementTree import Element

ComponentT = TypeVar("ComponentT", bound="Component")


@dataclass(frozen=True)
class Component(ABC):
    def to_json(self, indent: Optional[int] = 2) -> str:
        return json.dumps(asdict(self), indent=indent)

    @classmethod
    @abstractmethod
    def from_xml_element(cls: Type[ComponentT], element: Element) -> ComponentT: ...

    @abstractmethod
    def to_xml_element(self, parent: Element) -> None: ...


@dataclass(frozen=True)
class HasName:
    name: str
