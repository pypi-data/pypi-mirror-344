from dataclasses import dataclass
from typing import Optional, Tuple
from xml.etree.ElementTree import Element, SubElement

from ._utils import (
    Customization,
    assert_not_none,
    find_child_attribute,
    parse_3_floats,
    parse_4_floats,
    parse_child_object,
    process_attribute,
)
from .base import Component, HasName
from .geometry import Geometry


@dataclass(frozen=True)
class Origin(Component):
    xyz: Optional[Tuple[float, float, float]]
    rpy: Optional[Tuple[float, float, float]]

    @classmethod
    def from_xml_element(cls, element: Element):
        return cls(
            xyz=process_attribute(element, "xyz", parse_3_floats),
            rpy=process_attribute(element, "rpy", parse_3_floats),
        )

    def to_xml_element(self, parent: Element) -> None:
        origin_el = SubElement(parent, "origin")
        if self.xyz:
            origin_el.set("xyz", f"{self.xyz[0]} {self.xyz[1]} {self.xyz[2]}")
        if self.rpy:
            origin_el.set("rpy", f"{self.rpy[0]} {self.rpy[1]} {self.rpy[2]}")


@dataclass(frozen=True)
class Color(Component):
    rgba: Tuple[float, float, float, float]

    @classmethod
    def from_xml_element(cls, element: Element):
        return cls(rgba=parse_4_floats(assert_not_none(element.get("rgba"))))

    def to_xml_element(self, parent: Element) -> None:
        SubElement(parent, "color").set(
            "rgba",
            f"{self.rgba[0]} {self.rgba[1]} {self.rgba[2]} {self.rgba[3]}",
        )


@dataclass(frozen=True)
class Material(Component, HasName):
    color: Optional[Color]
    texture: Optional[str]

    @classmethod
    def from_xml_element(cls, element: Element):
        return cls(
            name=assert_not_none(element.get("name")),
            color=parse_child_object(Color, element, "color"),
            texture=find_child_attribute(element, "texture", "filename"),
        )

    def to_xml_element(self, parent: Element) -> None:
        material_el = SubElement(parent, "material")
        material_el.set("name", self.name)
        if self.color:
            self.color.to_xml_element(material_el)
        if self.texture:
            SubElement(material_el, "texture").set("filename", self.texture)


@dataclass(frozen=True)
class Visual(Component):
    geometry: Geometry
    origin: Optional[Origin]
    material: Optional[Material]
    name: Optional[str]

    @classmethod
    def from_xml_element(cls, element: Element):
        return cls(
            geometry=assert_not_none(parse_child_object(Geometry, element, "geometry")),
            origin=parse_child_object(Origin, element, "origin"),
            material=parse_child_object(Material, element, "material"),
            name=element.get(key="name"),
        )

    def customize(self, customization: Customization):
        prefix = customization.get("prefix")
        if prefix and self.name and not self.name.startswith(prefix):
            name = f"{prefix}{self.name}"
        else:
            name = self.name
        return self.__class__(
            geometry=self.geometry.customize(customization, "visual"),
            origin=self.origin,
            material=self.material,
            name=name,
        )

    def to_xml_element(self, parent: Element) -> None:
        visual_el = SubElement(parent, "visual")
        if self.name:
            visual_el.set("name", self.name)
        if self.origin:
            self.origin.to_xml_element(visual_el)
        self.geometry.to_xml_element(visual_el)
        if self.material:
            self.material.to_xml_element(visual_el)


@dataclass(frozen=True)
class Collision(Component):
    geometry: Geometry
    origin: Optional[Origin]
    name: Optional[str]

    @classmethod
    def from_xml_element(cls, element: Element):
        return cls(
            geometry=assert_not_none(parse_child_object(Geometry, element, "geometry")),
            origin=parse_child_object(Origin, element, "origin"),
            name=element.get("name"),
        )

    def customize(self, customization: Customization):
        prefix = customization.get("prefix")
        if prefix and self.name and not self.name.startswith(prefix):
            name = f"{prefix}{self.name}"
        else:
            name = self.name
        return self.__class__(
            geometry=self.geometry.customize(customization, "mesh"),
            origin=self.origin,
            name=name,
        )

    def to_xml_element(self, parent: Element) -> None:
        collision_el = SubElement(parent, "collision")
        if self.name:
            collision_el.set("name", self.name)
        if self.origin:
            self.origin.to_xml_element(collision_el)
        self.geometry.to_xml_element(collision_el)


@dataclass(frozen=True)
class Calibration(Component):
    rising: Optional[float]
    falling: Optional[float]

    @classmethod
    def from_xml_element(cls, element: Element):
        return cls(
            rising=process_attribute(element, "rising", float),
            falling=process_attribute(element, "falling", float),
        )

    def to_xml_element(self, parent: Element) -> None:
        calib_el = SubElement(parent, "calibration")
        if self.rising is not None:
            calib_el.set("rising", str(self.rising))
        if self.falling is not None:
            calib_el.set("falling", str(self.falling))


@dataclass(frozen=True)
class Inertia(Component):
    ixx: float
    ixy: float
    ixz: float
    iyy: float
    iyz: float
    izz: float

    @classmethod
    def from_xml_element(cls, element: Element):
        return cls(
            ixx=float(assert_not_none(element.get("ixx"))),
            ixy=float(assert_not_none(element.get("ixy"))),
            ixz=float(assert_not_none(element.get("ixz"))),
            iyy=float(assert_not_none(element.get("iyy"))),
            iyz=float(assert_not_none(element.get("iyz"))),
            izz=float(assert_not_none(element.get("izz"))),
        )

    def to_xml_element(self, parent: Element) -> None:
        inertia_el = SubElement(parent, "inertia")
        inertia_el.set("ixx", str(self.ixx))
        inertia_el.set("ixy", str(self.ixy))
        inertia_el.set("ixz", str(self.ixz))
        inertia_el.set("iyy", str(self.iyy))
        inertia_el.set("iyz", str(self.iyz))
        inertia_el.set("izz", str(self.izz))


@dataclass(frozen=True)
class Inertial(Component):
    origin: Optional[Origin]
    mass: float
    inertia: Inertia

    @classmethod
    def from_xml_element(cls, element: Element):
        return cls(
            origin=parse_child_object(Origin, element, "origin"),
            mass=float(assert_not_none(find_child_attribute(element, "mass", "value"))),
            inertia=assert_not_none(parse_child_object(Inertia, element, "inertia")),
        )

    def to_xml_element(self, parent: Element) -> None:
        inertial_el = SubElement(parent, "inertial")
        if self.origin:
            self.origin.to_xml_element(inertial_el)
        SubElement(inertial_el, "mass").set("value", str(self.mass))
        self.inertia.to_xml_element(inertial_el)


@dataclass(frozen=True)
class Axis(Component):
    xyz: Tuple[float, float, float]

    @classmethod
    def from_xml_element(cls, element: Element):
        return cls(xyz=parse_3_floats(assert_not_none(element.get("xyz"))))

    def to_xml_element(self, parent: Element) -> None:
        SubElement(parent, "axis").set("xyz", f"{self.xyz[0]} {self.xyz[1]} {self.xyz[2]}")


@dataclass(frozen=True)
class Dynamics(Component):
    damping: Optional[float]
    friction: Optional[float]

    @classmethod
    def from_xml_element(cls, element: Element):
        return cls(
            damping=process_attribute(element, "damping", float),
            friction=process_attribute(element, "friction", float),
        )

    def to_xml_element(self, parent: Element) -> None:
        dyn_el = SubElement(parent, "dynamics")
        if self.damping is not None:
            dyn_el.set("damping", str(self.damping))
        if self.friction is not None:
            dyn_el.set("friction", str(self.friction))


@dataclass(frozen=True)
class Limit(Component):
    lower: Optional[float]
    upper: Optional[float]
    effort: float
    velocity: float

    @classmethod
    def from_xml_element(cls, element: Element):
        return cls(
            lower=process_attribute(element, "lower", float),
            upper=process_attribute(element, "upper", float),
            effort=float(assert_not_none(element.get("effort"))),
            velocity=float(assert_not_none(element.get("velocity"))),
        )

    def to_xml_element(self, parent: Element) -> None:
        limit_el = SubElement(parent, "limit")
        if self.lower is not None:
            limit_el.set("lower", str(self.lower))
        if self.upper is not None:
            limit_el.set("upper", str(self.upper))
        limit_el.set("effort", str(self.effort))
        limit_el.set("velocity", str(self.velocity))


@dataclass(frozen=True)
class SafetyController(Component):
    k_velocity: float
    soft_lower_limit: Optional[float]
    soft_upper_limit: Optional[float]
    k_position: Optional[float]

    @classmethod
    def from_xml_element(cls, element: Element):
        return cls(
            k_velocity=float(assert_not_none(element.get("k_velocity"))),
            soft_lower_limit=process_attribute(element, "soft_lower_limit", float),
            soft_upper_limit=process_attribute(element, "soft_upper_limit", float),
            k_position=process_attribute(element, "k_position", float),
        )

    def to_xml_element(self, parent: Element) -> None:
        sc_el = SubElement(parent, "safety_controller")
        sc_el.set("k_velocity", str(self.k_velocity))
        if self.soft_lower_limit is not None:
            sc_el.set("soft_lower_limit", str(self.soft_lower_limit))
        if self.soft_upper_limit is not None:
            sc_el.set("soft_upper_limit", str(self.soft_upper_limit))
        if self.k_position is not None:
            sc_el.set("k_position", str(self.k_position))


@dataclass(frozen=True)
class Mimic(Component):
    joint: str
    multiplier: Optional[float]
    offset: Optional[float]

    @classmethod
    def from_xml_element(cls, element: Element):
        return cls(
            joint=assert_not_none(element.get("joint")),
            multiplier=process_attribute(element, "multiplier", float),
            offset=process_attribute(element, "offset", float),
        )

    def customize(self, customization: Customization):
        prefix = customization.get("prefix")
        if prefix and not self.joint.startswith(prefix):
            joint = f"{prefix}{self.joint}"
        else:
            joint = self.joint
        return self.__class__(
            joint=joint,
            multiplier=self.multiplier,
            offset=self.offset,
        )

    def to_xml_element(self, parent: Element) -> None:
        mimic_el = SubElement(parent, "mimic")
        mimic_el.set("joint", self.joint)
        if self.multiplier is not None:
            mimic_el.set("multiplier", str(self.multiplier))
        if self.offset is not None:
            mimic_el.set("offset", str(self.offset))
