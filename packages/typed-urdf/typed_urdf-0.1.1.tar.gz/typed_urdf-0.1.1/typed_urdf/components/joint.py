from dataclasses import dataclass
from typing import Optional
from xml.etree.ElementTree import Element, SubElement

from ._utils import Customization, assert_not_none, find_child_attribute, parse_child_object
from .base import Component, HasName
from .extra import Axis, Calibration, Dynamics, Limit, Mimic, Origin, SafetyController


@dataclass(frozen=True)
class Joint(Component, HasName):
    type: str
    parent: str
    child: str
    origin: Optional[Origin]
    axis: Optional[Axis]
    calibration: Optional[Calibration]
    dynamics: Optional[Dynamics]
    limit: Optional[Limit]
    mimic: Optional[Mimic]
    safety_controller: Optional[SafetyController]

    def customize(self, customization: Customization) -> "Joint":
        prefix = customization.get("prefix")
        if prefix and not self.name.startswith(prefix):
            name = f"{prefix}{self.name}"
        else:
            name = self.name

        if prefix and not self.parent.startswith(prefix):
            parent: str = f"{prefix}{self.parent}"
        else:
            parent = self.parent

        if prefix and not self.child.startswith(prefix):
            child = f"{prefix}{self.child}"
        else:
            child = self.child

        if self.mimic is not None:
            mimic = self.mimic.customize(customization)
        else:
            mimic = None

        return self.__class__(
            type=self.type,
            parent=parent,
            child=child,
            origin=self.origin,
            axis=self.axis,
            calibration=self.calibration,
            dynamics=self.dynamics,
            limit=self.limit,
            mimic=mimic,
            safety_controller=self.safety_controller,
            name=name,
        )

    @classmethod
    def from_xml_element(cls, element: Element) -> "Joint":
        return cls(
            name=assert_not_none(element.get("name")),
            type=assert_not_none(element.get("type")),
            origin=parse_child_object(Origin, element, "origin"),
            parent=assert_not_none(find_child_attribute(element, "parent", "link")),
            child=assert_not_none(find_child_attribute(element, "child", "link")),
            axis=parse_child_object(Axis, element, "axis"),
            calibration=parse_child_object(Calibration, element, "calibration"),
            dynamics=parse_child_object(Dynamics, element, "dynamics"),
            limit=parse_child_object(Limit, element, "limit"),
            mimic=parse_child_object(Mimic, element, "mimic"),
            safety_controller=parse_child_object(SafetyController, element, "safety_controller"),
        )

    def to_xml_element(self, parent: Element) -> None:
        joint_el = SubElement(parent, "joint")
        joint_el.set("name", self.name)
        joint_el.set("type", self.type)
        if self.origin:
            self.origin.to_xml_element(joint_el)
        parent_el = SubElement(joint_el, "parent")
        parent_el.set("link", self.parent)
        child_el = SubElement(joint_el, "child")
        child_el.set("link", self.child)
        if self.axis and self.type not in ("fixed", "floating"):
            self.axis.to_xml_element(joint_el)
        if self.calibration:
            self.calibration.to_xml_element(joint_el)
        if self.dynamics:
            self.dynamics.to_xml_element(joint_el)
        if self.limit:
            self.limit.to_xml_element(joint_el)
        if self.mimic:
            self.mimic.to_xml_element(joint_el)
        if self.safety_controller:
            self.safety_controller.to_xml_element(joint_el)
