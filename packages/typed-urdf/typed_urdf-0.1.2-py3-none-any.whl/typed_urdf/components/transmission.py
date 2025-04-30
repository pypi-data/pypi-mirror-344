from dataclasses import dataclass
from typing import Optional, Tuple
from xml.etree.ElementTree import Element, SubElement

from ._utils import Customization, assert_not_none
from .base import Component, HasName


@dataclass(frozen=True)
class TransmissionJoint(Component, HasName):
    """
    <joint name="foo_joint">
      <hardwareInterface>EffortJointInterface</hardwareInterface>
      ...
    </joint>
    """

    hardware_interfaces: Tuple[str, ...]

    def customize(self, customization: Customization) -> "TransmissionJoint":
        prefix = customization.get("prefix")
        if prefix and not self.name.startswith(prefix):
            name = f"{prefix}{self.name}"
        else:
            name = self.name
        return self.__class__(hardware_interfaces=self.hardware_interfaces, name=name)

    @classmethod
    def from_xml_element(cls, element: Element) -> "TransmissionJoint":
        return cls(
            name=assert_not_none(element.get("name")),
            hardware_interfaces=tuple(
                hw_el.text for hw_el in element.findall("hardwareInterface") if hw_el.text is not None
            ),
        )

    def to_xml_element(self, parent: Element) -> None:
        joint_el = SubElement(parent, "joint")
        joint_el.set("name", self.name)
        for hw in self.hardware_interfaces:
            hw_el = SubElement(joint_el, "hardwareInterface")
            hw_el.text = hw


@dataclass(frozen=True)
class TransmissionActuator(Component, HasName):
    """
    <actuator name="foo_motor">
      <mechanicalReduction>50</mechanicalReduction>
      <hardwareInterface>EffortJointInterface</hardwareInterface>
      ...
    </actuator>
    """

    mechanical_reduction: Optional[float]
    hardware_interfaces: Tuple[str, ...]

    def customize(self, customization: Customization) -> "TransmissionActuator":
        prefix = customization.get("prefix")
        if prefix and not self.name.startswith(prefix):
            name = f"{prefix}{self.name}"
        else:
            name = self.name
        return self.__class__(
            mechanical_reduction=self.mechanical_reduction,
            hardware_interfaces=self.hardware_interfaces,
            name=name,
        )

    @classmethod
    def from_xml_element(cls, element: Element) -> "TransmissionActuator":
        mech_el = element.find("mechanicalReduction")
        if mech_el is not None and mech_el.text:
            mechanical_reduction = float(mech_el.text)
        else:
            mechanical_reduction = None
        return cls(
            name=assert_not_none(element.get("name")),
            mechanical_reduction=mechanical_reduction,
            hardware_interfaces=tuple(
                hw_el.text for hw_el in element.findall("hardwareInterface") if hw_el.text is not None
            ),
        )

    def to_xml_element(self, parent: Element) -> None:
        actuator_el = SubElement(parent, "actuator")
        actuator_el.set("name", self.name)
        if self.mechanical_reduction is not None:
            SubElement(actuator_el, "mechanicalReduction").text = str(self.mechanical_reduction)
        for hw in self.hardware_interfaces:
            SubElement(actuator_el, "hardwareInterface").text = hw


@dataclass(frozen=True)
class Transmission(Component, HasName):
    """
    <transmission name="simple_trans">
      <type>transmission_interface/SimpleTransmission</type>
      <joint name="foo_joint"> ... </joint>
      <actuator name="foo_motor"> ... </actuator>
    </transmission>
    """

    type: str
    joints: Tuple[TransmissionJoint, ...]
    actuators: Tuple[TransmissionActuator, ...]

    def customize(self, customization: Customization) -> "Transmission":
        prefix = customization.get("prefix")
        if prefix and not self.name.startswith(prefix):
            name = f"{prefix}{self.name}"
        else:
            name = self.name
        return self.__class__(
            type=self.type,
            joints=tuple(j.customize(customization) for j in self.joints),
            actuators=tuple(a.customize(customization) for a in self.actuators),
            name=name,
        )

    @classmethod
    def from_xml_element(cls, element: Element) -> "Transmission":
        return cls(
            name=assert_not_none(element.get("name")),
            type=assert_not_none(assert_not_none(element.find("type")).text),
            joints=tuple(TransmissionJoint.from_xml_element(j_el) for j_el in element.findall("joint")),
            actuators=tuple(TransmissionActuator.from_xml_element(a_el) for a_el in element.findall("actuator")),
        )

    def to_xml_element(self, parent: Element) -> None:
        trans_el = SubElement(parent, "transmission")
        trans_el.set("name", self.name)
        SubElement(trans_el, "type").text = self.type
        for j in self.joints:
            j.to_xml_element(trans_el)
        for a in self.actuators:
            a.to_xml_element(trans_el)
