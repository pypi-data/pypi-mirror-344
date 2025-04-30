from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional, Tuple, Union
from xml.etree.ElementTree import Element, SubElement

from ._utils import Customization, assert_not_none, parse_3_floats, process_attribute
from .base import Component


@dataclass(frozen=True)
class Box(Component):
    size: Tuple[float, float, float]

    @classmethod
    def from_xml_element(cls, element: Element) -> "Box":
        return cls(size=parse_3_floats(assert_not_none(element.get("size"))))

    def to_xml_element(self, parent: Element) -> None:
        SubElement(parent, "box").set("size", f"{self.size[0]} {self.size[1]} {self.size[2]}")


@dataclass(frozen=True)
class Cylinder(Component):
    radius: float
    length: float

    @classmethod
    def from_xml_element(cls, element: Element) -> "Cylinder":
        return cls(
            radius=float(assert_not_none(element.get("radius"))),
            length=float(assert_not_none(element.get("length"))),
        )

    def to_xml_element(self, parent: Element) -> None:
        cyl_el = SubElement(parent, "cylinder")
        cyl_el.set("radius", str(self.radius))
        cyl_el.set("length", str(self.length))


@dataclass(frozen=True)
class Sphere(Component):
    radius: float

    @classmethod
    def from_xml_element(cls, element: Element) -> "Sphere":
        return cls(radius=float(assert_not_none(element.get("radius"))))

    def to_xml_element(self, parent: Element) -> None:
        SubElement(parent, "sphere").set("radius", str(self.radius))


@dataclass(frozen=True)
class Mesh(Component):
    filename: str
    scale: Optional[Tuple[float, float, float]]

    @classmethod
    def from_xml_element(cls, element: Element) -> "Mesh":
        return cls(
            filename=assert_not_none(element.get("filename")),
            scale=process_attribute(element, "scale", parse_3_floats),
        )

    def to_xml_element(self, parent: Element) -> None:
        mesh_el = SubElement(parent, "mesh")
        mesh_el.set("filename", self.filename)
        if self.scale:
            mesh_el.set("scale", f"{self.scale[0]} {self.scale[1]} {self.scale[2]}")


@dataclass(frozen=True)
class Geometry(Component):
    geometry: Union[Box, Cylinder, Sphere, Mesh]

    @classmethod
    def from_xml_element(cls, element: Element) -> "Geometry":
        if (box_el := element.find("box")) is not None:
            return cls(Box.from_xml_element(box_el))
        elif (cylinder_el := element.find("cylinder")) is not None:
            return cls(Cylinder.from_xml_element(cylinder_el))
        elif (sphere_el := element.find("sphere")) is not None:
            return cls(Sphere.from_xml_element(sphere_el))
        elif (mesh_el := element.find("mesh")) is not None:
            return cls(Mesh.from_xml_element(mesh_el))
        else:
            raise ValueError("Unknown geometry type")

    def to_xml_element(self, parent: Element) -> None:
        self.geometry.to_xml_element(SubElement(parent, "geometry"))

    def customize(self, customization: Customization, context: Literal["mesh", "visual"]) -> "Geometry":
        prefix = customization.get("prefix")
        if isinstance(self.geometry, Mesh):
            # filename이 prefix로 시작하지 않으면, prefix를 붙입니다.
            geo = self.geometry
            filename = Path(geo.filename)
            if prefix and not self.geometry.filename.startswith(prefix):
                filename = filename.with_name(f"{prefix}{filename.name}")
            if context == "visual":
                base = customization.get("visual_basedir")
                suffix = customization.get("visual_suffix")
            elif context == "mesh":
                base = customization.get("mesh_basedir")
                suffix = customization.get("mesh_suffix")
            if base:
                if base.is_file():
                    base = base.parent
                filename = base / filename.name
            if suffix:
                filename = filename.with_suffix(suffix)
            return self.__class__(geo.__class__(filename=filename.as_posix(), scale=geo.scale))
        return self
