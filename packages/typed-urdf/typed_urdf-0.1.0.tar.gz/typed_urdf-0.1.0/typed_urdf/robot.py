import logging
import xml.etree.ElementTree as ET
from copy import deepcopy
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union
from xml.etree.ElementTree import Element, tostring

import networkx as nx

from .components._utils import Customization, assert_not_none
from .components.extra import Material
from .components.geometry import Mesh
from .components.joint import Joint
from .components.link import Link
from .components.transmission import Transmission

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Robot:
    name: str
    links: Tuple[Link, ...]
    joints: Tuple[Joint, ...]
    transmissions: Tuple[Transmission, ...]

    def __post_init__(self):
        _validate_transmissions(self)
        link_map = self.link_map
        for link in self.links:
            self.graph.add_node(link)
        for joint in self.joints:
            self.graph.add_edge(link_map[joint.child], link_map[joint.parent], joint=joint)
        _validate_graph(self)

    @classmethod
    def from_xml_element(cls, element: Element) -> "Robot":
        return cls(
            name=assert_not_none(element.get("name")),
            links=tuple(Link.from_xml_element(link_el) for link_el in element.findall("link")),
            joints=tuple(Joint.from_xml_element(joint_el) for joint_el in element.findall("joint")),
            transmissions=tuple(
                Transmission.from_xml_element(trans_el) for trans_el in element.findall("transmission")
            ),
        )

    @classmethod
    def from_urdf(
        cls, urdf_string_or_path: Union[str, Path], encoding: Optional[str] = "utf-8", errors: Optional[str] = None
    ) -> "Robot":
        if isinstance(urdf_string_or_path, Path):
            urdf_string = urdf_string_or_path.read_text(encoding=encoding, errors=errors)
        else:
            urdf_string = urdf_string_or_path
        return cls.from_xml_element(ET.fromstring(urdf_string))

    def customize(self, customization: Customization) -> "Robot":
        name = self.name
        return self.__class__(
            name=name,
            links=tuple(link.customize(customization) for link in self.links),
            joints=tuple(joint.customize(customization) for joint in self.joints),
            transmissions=tuple(transmission.customize(customization) for transmission in self.transmissions),
        )

    def to_urdf(self, encoding: str = "utf-8") -> str:
        root = self.to_xml_element()

        def indent(elem: Element, level: int) -> Element[str]:
            i = "\n" + level * "  "
            j = "\n" + (level - 1) * "  "
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + "  "
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
                for subelem in elem:
                    indent(subelem, level + 1)
                if not elem.tail or not elem.tail.strip():
                    elem.tail = j
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = j
            return elem

        indent(root, level=1)
        return tostring(root, method="xml", encoding=encoding).decode(encoding)

    def to_xml_element(self) -> Element:
        robot_el = Element("robot")
        robot_el.set("name", self.name)
        for link in self.links:
            link.to_xml_element(robot_el)
        for joint in self.joints:
            joint.to_xml_element(robot_el)
        for trans in self.transmissions:
            trans.to_xml_element(robot_el)
        return robot_el

    @cached_property
    def filenames(self) -> Set[str]:
        return {
            geometry.filename
            for link in self.links
            for vis_or_col in link.visuals + link.collisions
            if isinstance(geometry := vis_or_col.geometry.geometry, Mesh)
        }

    @cached_property
    def graph(self) -> nx.DiGraph:
        return nx.DiGraph()

    @cached_property
    def material_map(self) -> Dict[str, Material]:
        """Merge the top-level material set with the link materials."""
        material_map: Dict[str, Material] = {}
        for link in self.links:
            for v in link.visuals:
                if v.material is None:
                    continue
                if v.material.name not in material_map:
                    material_map[v.material.name] = v.material
        return material_map

    @cached_property
    def joint_map(self) -> Dict[str, Joint]:
        return {j.name: j for j in self.joints}

    @cached_property
    def link_map(self) -> Dict[str, Link]:
        return {link.name: link for link in self.links}

    @cached_property
    def materials(self) -> List[Material]:
        return [m for m in self.material_map.values()]

    @cached_property
    def paths_to_base(self) -> Dict[Link, List[Link]]:
        shortest_path = nx.shortest_path(self.graph, target=self.base_link)
        assert isinstance(shortest_path, dict) and all(
            isinstance(k, Link) and isinstance(v, list) for k, v in shortest_path.items()
        )
        return shortest_path

    @cached_property
    def base_link(self) -> Link:
        base_link: Optional[Link] = None
        for n in self.graph:
            assert isinstance(n, Link)
            if not nx.descendants(self.graph, n):
                if base_link is None:
                    base_link = n
                else:
                    raise ValueError(f"Links {n.name} and {base_link.name} are both base links!")
        if base_link is None:
            raise ValueError("No base link found!")
        return base_link

    @cached_property
    def end_links(self) -> List[Link]:
        return [n for n in self.graph if isinstance(n, Link) and not nx.ancestors(self.graph, n)]

    @cached_property
    def actuated_joints(self) -> Dict[str, Joint]:
        """Raise an exception of any joints are invalidly specified.

        Checks for the following:

        - Joint parents are valid link names.
        - Joint children are valid link names that aren't the same as parent.
        - Joint mimics have valid joint names that aren't the same joint.

        Returns
        -------
        actuated_joints : dict of str to :class:`.Joint`
            The actuated joints.
        """
        link_map = self.link_map
        joint_map = self.joint_map
        actuated_joints: List[Joint] = []
        for joint in self.joints:
            if joint.parent not in link_map:
                raise ValueError(f"Joint {joint.name} has invalid parent link name {joint.parent}")
            if joint.child not in link_map:
                raise ValueError(f"Joint {joint.name} has invalid child link name {joint.child}")
            if joint.child == joint.parent:
                raise ValueError(f"Joint {joint.name} has matching parent and child")
            if joint.mimic is not None:
                if joint.mimic.joint not in joint_map:
                    raise ValueError(f"Joint {joint.name} has an invalid mimic joint name {joint.mimic.joint}")
                if joint.mimic.joint == joint.name:
                    raise ValueError(f"Joint {joint.mimic.joint} set up to mimic itself")
            elif joint.type != "fixed":
                actuated_joints.append(joint)

        return {joint.name: joint for joint in actuated_joints}

    @cached_property
    def sorted_actuated_joints(self) -> Dict[str, Joint]:
        """Sort joints by ascending distance from the base link (topologically).

        Returns
        -------
        joints : list of :class:`.Joint`
            The sorted joints.
        """

        link_map = self.link_map
        paths_to_base = self.paths_to_base
        actuated_joints = self.actuated_joints
        lengths: Dict[str, int] = {
            joint_name: len(paths_to_base[link_map[joint.child]]) for joint_name, joint in actuated_joints.items()
        }
        return {joint_name: joint for joint_name, joint in sorted(actuated_joints.items(), key=lambda x: lengths[x[0]])}

    @cached_property
    def reverse_topological_order(self) -> List[Link]:
        """Return the links in reverse topological order."""
        result = list(reversed(list(nx.topological_sort(self.graph))))
        assert isinstance(result, list) and all(isinstance(link, Link) for link in result)
        return result

    def copy(self) -> "Robot":
        """Create a deep copy of the robot.

        Returns:
            Robot: A new Robot instance that is a deep copy of the current one.
        """
        return deepcopy(self)


def _validate_graph(robot: Robot) -> None:
    """Raise an exception if the link-joint structure is invalid.

    Checks for the following:

    - The graph is connected in the undirected sense.
    - The graph is acyclic in the directed sense.
    - The graph has only one base link.
    """

    # Check that the link graph is weakly connected
    if not nx.is_weakly_connected(robot.graph):
        link_clusters: List[List[str]] = [
            [str(link.name) for link in links if isinstance(link, Link)]
            for links in nx.weakly_connected_components(robot.graph)
        ]
        raise ValueError(
            "Links are not all connected. Connected components are:\n\t"
            + "\n\t".join(", ".join(lc) for lc in link_clusters)
        )

    # Check that link graph is acyclic
    if not nx.is_directed_acyclic_graph(robot.graph):
        raise ValueError("There are cycles in the link graph")
    robot.sorted_actuated_joints
    robot.reverse_topological_order


def _validate_transmissions(robot: Robot) -> None:
    """Raise an exception of any transmissions are invalidly specified.

    Checks for the following:

    - Transmission joints have valid joint names.
    """
    joint_map = robot.joint_map
    for t in robot.transmissions:
        for joint in t.joints:
            if joint.name not in joint_map:
                raise ValueError(f"Transmission {t.name} has invalid joint name {joint.name}")
