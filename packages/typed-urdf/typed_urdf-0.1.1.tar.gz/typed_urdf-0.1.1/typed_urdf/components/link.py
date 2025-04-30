from dataclasses import dataclass
from typing import Optional, Tuple
from xml.etree.ElementTree import Element, SubElement

from ._utils import Customization, assert_not_none, parse_child_object
from .base import Component, HasName
from .extra import Collision, Inertial, Visual


@dataclass(frozen=True)
class Link(Component, HasName):
    inertial: Optional[Inertial]
    visuals: Tuple[Visual, ...]
    collisions: Tuple[Collision, ...]

    def customize(self, customization: Customization) -> "Link":
        prefix = customization.get("prefix")

        if prefix and not self.name.startswith(prefix):
            name = f"{prefix}{self.name}"
        else:
            name = self.name
        return self.__class__(
            inertial=self.inertial,
            visuals=tuple(v.customize(customization) for v in self.visuals),
            collisions=tuple(c.customize(customization) for c in self.collisions),
            name=name,
        )

    @classmethod
    def from_xml_element(cls, element: Element) -> "Link":
        return cls(
            name=assert_not_none(element.get("name")),
            inertial=parse_child_object(Inertial, element, "inertial"),
            visuals=tuple(v for v in (Visual.from_xml_element(vis_el) for vis_el in element.findall("visual")) if v),
            collisions=tuple(
                c for c in (Collision.from_xml_element(col_el) for col_el in element.findall("collision")) if c
            ),
        )

    def to_xml_element(self, parent: Element) -> None:
        link_el = SubElement(parent, "link")
        link_el.set("name", self.name)
        if self.inertial:
            self.inertial.to_xml_element(link_el)
        for visual in self.visuals:
            visual.to_xml_element(link_el)
        for collision in self.collisions:
            collision.to_xml_element(link_el)
