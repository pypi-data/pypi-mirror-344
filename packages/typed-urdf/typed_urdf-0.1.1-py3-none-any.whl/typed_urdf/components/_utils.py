from pathlib import Path
from typing import Callable, Optional, Tuple, Type, TypedDict, TypeVar, Union
from xml.etree.ElementTree import Element

from .base import Component

T = TypeVar("T")
ComponentT = TypeVar("ComponentT", bound=Component)


class Customization(TypedDict, total=False):
    """URDF에서 사용자 정의 속성을 나타내는 딕셔너리입니다."""

    prefix: str
    collision_basedir: Union[Path, str]
    collision_suffix: str
    visual_basedir: Union[Path, str]
    visual_suffix: str


def parse_3_floats(s: str) -> Tuple[float, float, float]:
    parts = s.split()
    x = float(parts[0]) if len(parts) > 0 else 0.0
    y = float(parts[1]) if len(parts) > 1 else 0.0
    z = float(parts[2]) if len(parts) > 2 else 0.0
    return (x, y, z)


def parse_4_floats(s: str) -> Tuple[float, float, float, float]:
    parts = s.split()
    r = float(parts[0]) if len(parts) > 0 else 0.0
    g = float(parts[1]) if len(parts) > 1 else 0.0
    b = float(parts[2]) if len(parts) > 2 else 0.0
    a = float(parts[3]) if len(parts) > 3 else 1.0
    return (r, g, b, a)


def parse_child_object(cls: Type[ComponentT], root_element: Element, name: str) -> Optional[ComponentT]:
    """root_element에서 name을 가진 자식 엘리먼트를 찾아서 cls로 변환."""
    el = root_element.find(name)
    if el is not None:
        return cls.from_xml_element(el)


def assert_not_none(obj: Optional[T]) -> T:
    assert obj is not None, "Expected a non-None object"
    return obj


def find_child_attribute(element: Element, child_name: str, child_attr_name: str) -> Optional[str]:
    child_el = element.find(child_name)
    if child_el is not None:
        return child_el.get(child_attr_name)


def process_attribute(element: Element, attribute_name: str, callback: Callable[[str], T]) -> Optional[T]:
    if (value := element.get(attribute_name)) is not None:
        return callback(value)
