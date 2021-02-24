#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2020 FABRIC Testbed
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Author: Ilya Baldin (ibaldin@renci.org)
"""
Abstract definition of ASM (Abstract Slice Model) functionality
"""

from typing import List, Dict
from abc import ABCMeta, abstractmethod

from fim.slivers.network_node import NodeSliver
from fim.slivers.attached_components import ComponentSliver, AttachedComponentsInfo
from fim.slivers.switch_fabric import SwitchFabricSliver, SwitchFabricInfo
from fim.slivers.interface_info import InterfaceSliver, InterfaceInfo
from fim.slivers.capacities_labels import Capacities, Labels
from fim.slivers.network_link import NetworkLinkSliver
from fim.graph.abc_property_graph import ABCPropertyGraph, PropertyGraphQueryException


class ABCASMPropertyGraph(ABCPropertyGraph, metaclass=ABCMeta):
    """
    Interface for an ASM Mixin on top of a property graph
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_all_network_nodes') and
                callable(subclass.get_all_network_nodes) or NotImplemented)

    @abstractmethod
    def check_node_unique(self, *, label: str, name: str):
        """
        Check no other node of this class/label and name exists
        :param label:
        :param name:
        :return:
        """

    @abstractmethod
    def get_all_network_nodes(self) -> List[str]:
        """
        Get a list of nodes IDs in a slice model
        :return:
        """

    @abstractmethod
    def get_all_network_links(self) -> List[str]:
        """
        Get a list of link node ids in a slice model
        :return:
        """

    @abstractmethod
    def find_node_by_name(self, node_name: str, label: str) -> str:
        """
        Get node id of node based on its name and class/label. Throw
        exception if multiple matches found.
        :param node_name:
        :param label: node label or class of the node
        :return:
        """

    @staticmethod
    def node_sliver_from_graph_properties_dict(d: Dict[str, str]) -> NodeSliver:
        n = NodeSliver()
        if d.get(ABCPropertyGraph.PROP_IMAGE_REF, None) is None:
            image_ref = None
            image_type = None
        else:
            image_ref, image_type = d[ABCPropertyGraph.PROP_IMAGE_REF].split(',')
        n.set_properties(resource_name=d.get(ABCPropertyGraph.PROP_NAME, None),
                         resource_type=n.type_from_str(d.get(ABCPropertyGraph.PROP_TYPE, None)),
                         capacities=Capacities().from_json(d.get(ABCPropertyGraph.PROP_CAPACITIES, None)),
                         labels=Labels().from_json(d.get(ABCPropertyGraph.PROP_LABELS, None)),
                         site=d.get(ABCPropertyGraph.PROP_SITE, None),
                         image_ref=image_ref,
                         image_type=image_type,
                         management_ip=d.get(ABCPropertyGraph.PROP_MGMT_IP, None),
                         allocation_constraints=d.get(ABCPropertyGraph.PROP_ALLOCATION_CONSTRAINTS, None),
                         service_endpoint=d.get(ABCPropertyGraph.PROP_SERVICE_ENDPOINT, None),
                         details=d.get(ABCPropertyGraph.PROP_DETAILS, None)
                         )
        return n

    @staticmethod
    def link_sliver_from_graph_properties_dict(d: Dict[str, str]) -> NetworkLinkSliver:
        n = NetworkLinkSliver()
        n.set_properties(resource_name=d.get(ABCPropertyGraph.PROP_NAME, None),
                         resource_type=n.type_from_str(d.get(ABCPropertyGraph.PROP_TYPE, None)),
                         capacities=Capacities().from_json(d.get(ABCPropertyGraph.PROP_CAPACITIES, None)),
                         labels=Labels().from_json(d.get(ABCPropertyGraph.PROP_LABELS, None)),
                         layer=n.layer_from_str(d.get(ABCPropertyGraph.PROP_LAYER, None)),
                         technology=d.get(ABCPropertyGraph.PROP_TECHNOLOGY, None),
                         details=d.get(ABCPropertyGraph.PROP_DETAILS, None)
                         )
        return n

    @staticmethod
    def component_sliver_from_graph_properties_dict(d: Dict[str, str]) -> ComponentSliver:
        """
        Create component sliver from node graph properties
        :param d:
        :return:
        """
        cs = ComponentSliver()
        cs.set_properties(name=d.get(ABCPropertyGraph.PROP_NAME, None),
                          resource_type=cs.type_from_str(d.get(ABCPropertyGraph.PROP_TYPE, None)),
                          capacities=Capacities().from_json(d.get(ABCPropertyGraph.PROP_CAPACITIES, None)),
                          labels=Labels().from_json(d.get(ABCPropertyGraph.PROP_LABELS, None)),
                          details=d.get(ABCPropertyGraph.PROP_DETAILS, None)
                          )
        return cs

    @staticmethod
    def switch_fabric_sliver_from_graph_properties_dict(d: Dict[str, str]) -> SwitchFabricSliver:
        """
        SwitchFabric sliver from node graph properties
        :param d:
        :return:
        """
        sf = SwitchFabricSliver()
        sf.set_properties(name=d.get(ABCPropertyGraph.PROP_NAME, None),
                          resource_type=sf.type_from_str(d.get(ABCPropertyGraph.PROP_TYPE, None)),
                          capacities=Capacities().from_json(d.get(ABCPropertyGraph.PROP_CAPACITIES, None)),
                          labels=Labels().from_json(d.get(ABCPropertyGraph.PROP_LABELS, None)),
                          layer=sf.layer_from_str(d.get(ABCPropertyGraph.PROP_LAYER, None)),
                          details=d.get(ABCPropertyGraph.PROP_DETAILS, None)
                          )
        return sf

    @staticmethod
    def interface_sliver_from_graph_properties_dict(d: Dict[str, str]) -> InterfaceSliver:
        """
        Interface sliver from node graph properties
        :param d:
        :return:
        """
        isl = InterfaceSliver()
        isl.set_properties(name=d.get(ABCPropertyGraph.PROP_NAME, None),
                           resource_type=isl.type_from_str(d.get(ABCPropertyGraph.PROP_TYPE, None)),
                           capacities=Capacities().from_json(d.get(ABCPropertyGraph.PROP_CAPACITIES, None)),
                           labels=Labels().from_json(d.get(ABCPropertyGraph.PROP_LABELS, None)),
                           details=d.get(ABCPropertyGraph.PROP_DETAILS, None)
                           )
        return isl

    @staticmethod
    def node_sliver_to_graph_properties_dict(sliver: NodeSliver) -> Dict[str, str]:
        """
        This method knows how to map sliver fields to graph properties
        :param sliver:
        :return:
        """
        prop_dict = dict()

        if sliver.resource_name is not None:
            prop_dict[ABCPropertyGraph.PROP_NAME] = sliver.resource_name
        if sliver.resource_type is not None:
            prop_dict[ABCPropertyGraph.PROP_TYPE] = str(sliver.resource_type)
        if sliver.capacities is not None:
            prop_dict[ABCPropertyGraph.PROP_CAPACITIES] = sliver.capacities.to_json()
        if sliver.labels is not None:
            prop_dict[ABCPropertyGraph.PROP_LABELS] = sliver.labels.to_json()
        if sliver.site is not None:
            prop_dict[ABCPropertyGraph.PROP_SITE] = sliver.site
        if sliver.image_ref is not None and sliver.image_type is not None:
            prop_dict[ABCPropertyGraph.PROP_IMAGE_REF] = sliver.image_ref + ',' + str(sliver.image_type)
        if sliver.management_ip is not None:
            prop_dict[ABCPropertyGraph.PROP_MGMT_IP] = str(sliver.management_ip)
        if sliver.allocation_constraints is not None:
            prop_dict[ABCPropertyGraph.PROP_ALLOCATION_CONSTRAINTS] = sliver.allocation_constraints
        if sliver.service_endpoint is not None:
            prop_dict[ABCPropertyGraph.PROP_SERVICE_ENDPOINT] = str(sliver.service_endpoint)
        if sliver.details is not None:
            prop_dict[ABCPropertyGraph.PROP_DETAILS] = sliver.details
        return prop_dict

    @staticmethod
    def link_sliver_to_graph_properties_dict(sliver: NetworkLinkSliver) -> Dict[str, str]:
        """
        This method knows how to map sliver fields to graph properties
        :param sliver:
        :return:
        """
        prop_dict = dict()

        if sliver.resource_name is not None:
            prop_dict[ABCPropertyGraph.PROP_NAME] = sliver.resource_name
        if sliver.resource_type is not None:
            prop_dict[ABCPropertyGraph.PROP_TYPE] = str(sliver.resource_type)
        if sliver.capacities is not None:
            prop_dict[ABCPropertyGraph.PROP_CAPACITIES] = sliver.capacities.to_json()
        if sliver.labels is not None:
            prop_dict[ABCPropertyGraph.PROP_LABELS] = sliver.labels.to_json()
        if sliver.layer is not None:
            prop_dict[ABCPropertyGraph.PROP_LAYER] = str(sliver.layer)
        if sliver.technology is not None:
            prop_dict[ABCPropertyGraph.PROP_TECHNOLOGY] = str(sliver.technology)
        if sliver.details is not None:
            prop_dict[ABCPropertyGraph.PROP_DETAILS] = sliver.details

        return prop_dict

    @staticmethod
    def component_sliver_to_graph_properties_dict(sliver: ComponentSliver) -> Dict[str, str]:
        """
        This method knows how to map component sliver fields to graph properties
        :param sliver:
        :return:
        """
        prop_dict = dict()

        if sliver.resource_name is not None:
            prop_dict[ABCPropertyGraph.PROP_NAME] = sliver.resource_name
        if sliver.resource_type is not None:
            prop_dict[ABCPropertyGraph.PROP_TYPE] = str(sliver.resource_type)
        if sliver.capacities is not None:
            prop_dict[ABCPropertyGraph.PROP_CAPACITIES] = sliver.capacities.to_json()
        if sliver.labels is not None:
            prop_dict[ABCPropertyGraph.PROP_LABELS] = sliver.labels.to_json()
        if sliver.details is not None:
            prop_dict[ABCPropertyGraph.PROP_DETAILS] = sliver.details

        return prop_dict

    @staticmethod
    def switch_fabric_sliver_to_graph_properties_dict(sliver: SwitchFabricSliver) -> Dict[str, str]:
        """
        This method knows how to map switch fabric sliver fields to graph properties
        :param sliver:
        :return:
        """
        prop_dict = dict()

        if sliver.resource_name is not None:
            prop_dict[ABCPropertyGraph.PROP_NAME] = sliver.resource_name
        if sliver.resource_type is not None:
            prop_dict[ABCPropertyGraph.PROP_TYPE] = str(sliver.resource_type)
        if sliver.capacities is not None:
            prop_dict[ABCPropertyGraph.PROP_CAPACITIES] = sliver.capacities.to_json()
        if sliver.labels is not None:
            prop_dict[ABCPropertyGraph.PROP_LABELS] = sliver.labels.to_json()
        if sliver.layer is not None:
            prop_dict[ABCPropertyGraph.PROP_LAYER] = str(sliver.layer)
        if sliver.details is not None:
            prop_dict[ABCPropertyGraph.PROP_DETAILS] = sliver.details

        return prop_dict

    @staticmethod
    def interface_sliver_to_graph_properties_dict(sliver: InterfaceSliver) -> Dict[str, str]:
        """
        This method knows how to map interface sliver fields to graph properties
        :param sliver:
        :return:
        """
        prop_dict = dict()

        if sliver.resource_name is not None:
            prop_dict[ABCPropertyGraph.PROP_NAME] = sliver.resource_name
        if sliver.resource_type is not None:
            prop_dict[ABCPropertyGraph.PROP_TYPE] = str(sliver.resource_type)
        if sliver.capacities is not None:
            prop_dict[ABCPropertyGraph.PROP_CAPACITIES] = sliver.capacities.to_json()
        if sliver.labels is not None:
            prop_dict[ABCPropertyGraph.PROP_LABELS] = sliver.labels.to_json()
        if sliver.details is not None:
            prop_dict[ABCPropertyGraph.PROP_DETAILS] = sliver.details

        return prop_dict

    def get_all_link_interfaces(self, link_id: str) -> List[str]:
        assert link_id is not None
        # check this is a link
        labels, parent_props = self.get_node_properties(node_id=link_id)
        if ABCPropertyGraph.CLASS_Link not in labels:
            raise PropertyGraphQueryException(graph_id=self.graph_id, node_id=link_id,
                                              msg="Node type is not Link")
        return self.get_first_neighbor(node_id=link_id, rel=ABCPropertyGraph.REL_CONNECTS,
                                       node_label=ABCPropertyGraph.CLASS_ConnectionPoint)

    def get_all_network_node_components(self, parent_node_id: str) -> List[str]:
        """
        Return a list of components, children of a prent (presumably network node)
        :param parent_node_id:
        :return:
        """
        assert parent_node_id is not None
        # check that parent is a NetworkNode
        labels, parent_props = self.get_node_properties(node_id=parent_node_id)
        if ABCPropertyGraph.CLASS_NetworkNode not in labels:
            raise PropertyGraphQueryException(graph_id=self.graph_id, node_id=parent_node_id,
                                              msg="Parent node type is not NetworkNode")
        return self.get_first_neighbor(node_id=parent_node_id, rel=ABCPropertyGraph.REL_HAS,
                                       node_label=ABCPropertyGraph.CLASS_Component)

    def get_all_network_node_or_component_sfs(self, parent_node_id: str) -> List[str]:
        assert parent_node_id is not None
        # check that parent is a NetworkNode or Component
        labels, parent_props = self.get_node_properties(node_id=parent_node_id)
        if ABCPropertyGraph.CLASS_NetworkNode not in labels and \
            ABCPropertyGraph.CLASS_Component not in labels:
            raise PropertyGraphQueryException(graph_id=self.graph_id, node_id=parent_node_id,
                                              msg="Parent node type is not NetworkNode or Component")
        return self.get_first_neighbor(node_id=parent_node_id, rel=ABCPropertyGraph.REL_HAS,
                                       node_label=ABCPropertyGraph.CLASS_SwitchFabric)

    def get_all_node_or_component_connection_points(self, parent_node_id: str) -> List[str]:
        """
        Get a list of interfaces attached via switch fabrics
        :param parent_node_id:
        :return:
        """
        assert parent_node_id is not None
        labels, parent_props = self.get_node_properties(node_id=parent_node_id)
        if ABCPropertyGraph.CLASS_NetworkNode not in labels and \
                ABCPropertyGraph.CLASS_Component not in labels:
            raise PropertyGraphQueryException(graph_id=self.graph_id, node_id=parent_node_id,
                                              msg="Parent node type is not NetworkNode or Component")
        sfs_ifs = self.get_first_and_second_neighbor(node_id=parent_node_id, rel1=ABCPropertyGraph.REL_HAS,
                                                     node1_label=ABCPropertyGraph.CLASS_SwitchFabric,
                                                     rel2=ABCPropertyGraph.REL_CONNECTS,
                                                     node2_label=ABCPropertyGraph.CLASS_ConnectionPoint)
        ret = list()
        # return only interface IDs, not interested in SwitchFabrics
        for tup in sfs_ifs:
            ret.append(tup[1])
        return ret

    def get_all_sf_connection_points(self, parent_node_id: str) -> List[str]:
        assert parent_node_id is not None
        # check that parent is a SwitchFabric
        labels, parent_props = self.get_node_properties(node_id=parent_node_id)
        if ABCPropertyGraph.CLASS_SwitchFabric not in labels:
            raise PropertyGraphQueryException(graph_id=self.graph_id, node_id=parent_node_id,
                                              msg="Parent node type is not SwitchFabric")
        return self.get_first_neighbor(node_id=parent_node_id, rel=ABCPropertyGraph.REL_CONNECTS,
                                       node_label=ABCPropertyGraph.CLASS_ConnectionPoint)

    def find_component_by_name(self, *, parent_node_id: str, component_name: str) -> str:

        component_id_list = self.get_all_network_node_components(parent_node_id=parent_node_id)
        for cid in component_id_list:
            _, cprops = self.get_node_properties(node_id=cid)
            if cprops[ABCPropertyGraph.PROP_NAME] == component_name:
                return cid
        raise PropertyGraphQueryException(graph_id=self.graph_id, node_id=None,
                                          msg=f"Unable to find component with name {component_name}")

    def find_sf_by_name(self, *, parent_node_id: str, sfname: str) -> str:

        sf_id_list = self.get_all_network_node_or_component_sfs(parent_node_id=parent_node_id)
        for cid in sf_id_list:
            _, cprops = self.get_node_properties(node_id=cid)
            if cprops[ABCPropertyGraph.PROP_NAME] == sfname:
                return cid
        raise PropertyGraphQueryException(graph_id=self.graph_id, node_id=None,
                                          msg=f"Unable to find SwitchFabric with name {sfname}")

    def find_connection_point_by_name(self, *, parent_node_id: str, iname: str) -> str:

        if_id_list = self.get_all_sf_connection_points(parent_node_id=parent_node_id)
        for cid in if_id_list:
            _, cprops = self.get_node_properties(node_id=cid)
            if cprops[ABCPropertyGraph.PROP_NAME] == iname:
                return cid
        raise PropertyGraphQueryException(graph_id=self.graph_id, node_id=None,
                                          msg=f"Unable to find ConnectionPoint with name {iname}")

    def remove_network_node_with_components_sfs_cps_and_links(self, node_id: str):
        """
        Remove a network node, all of components and their interfaces, parent interfaces
        and connected links (as appropriate)
        :param node_id:
        :return:
        """
        # the network node itself
        # its components and switch fabrics
        # component switch fabrics
        # switch fabric interfaces (if present)
        # their parent interfaces (if present)
        # the 'Link' objects connected to interfaces if only one or no other interface connects to them

        # check we are a network node
        labels, node_props = self.get_node_properties(node_id=node_id)
        if ABCPropertyGraph.CLASS_NetworkNode not in labels:
            raise PropertyGraphQueryException(graph_id=self.graph_id, node_id=node_id,
                                              msg="This node type is not NetworkNode")
        # get a list of components
        components = self.get_first_neighbor(node_id=node_id, rel=ABCPropertyGraph.REL_HAS,
                                             node_label=ABCPropertyGraph.CLASS_Component)
        for cid in components:
            self.remove_component_with_sfs_cps_and_links(node_id=cid)

        # get a list of switch fabrics, delete the node
        switch_fabrics = self.get_first_neighbor(node_id=node_id, rel=ABCPropertyGraph.REL_HAS,
                                                 node_label=ABCPropertyGraph.CLASS_SwitchFabric)
        self.delete_node(node_id=node_id)
        for cid in switch_fabrics:
            self.remove_sf_with_cps_and_links(node_id=cid)

    def remove_component_with_sfs_cps_and_links(self, node_id: str):
        """
        Remove a component of a network node with all attached elements (switch fabrics
        and interfaces). Parent interfaces and links are removed if they have no other
        children or connected interfaces.
        :param node_id: component node id
        :return:
        """
        # check we are a component
        labels, node_props = self.get_node_properties(node_id=node_id)
        if ABCPropertyGraph.CLASS_Component not in labels:
            raise PropertyGraphQueryException(graph_id=self.graph_id, node_id=node_id,
                                              msg="This node type is not Component")
        # get a list of SwitchFabrics, delete the node
        switch_fabrics = self.get_first_neighbor(node_id=node_id, rel=ABCPropertyGraph.REL_HAS,
                                                 node_label=ABCPropertyGraph.CLASS_SwitchFabric)
        self.delete_node(node_id=node_id)
        for sf in switch_fabrics:
            self.remove_sf_with_cps_and_links(node_id=sf)

    def remove_network_link(self, node_id: str):

        # check we are a link
        labels, node_props = self.get_node_properties(node_id=node_id)
        if ABCPropertyGraph.CLASS_Link not in labels:
            raise PropertyGraphQueryException(graph_id=self.graph_id, node_id=node_id,
                                              msg="This node type is not Link")
        # edges to interfaces/connection points will disappear
        self.delete_node(node_id=node_id)

    def remove_sf_with_cps_and_links(self, node_id: str):
        """
        Remove switch fabric with subtending interfaces and links
        :param node_id:
        :return:
        """
        # check we are a switch fabric
        labels, node_props = self.get_node_properties(node_id=node_id)
        if ABCPropertyGraph.CLASS_SwitchFabric not in labels:
            raise PropertyGraphQueryException(graph_id=self.graph_id, node_id=node_id,
                                              msg="This node type is not SwitchFabric")
        # get a list of interfaces, delete the switch fabric
        interfaces = self.get_first_neighbor(node_id=node_id, rel=ABCPropertyGraph.REL_CONNECTS,
                                             node_label=ABCPropertyGraph.CLASS_ConnectionPoint)
        self.delete_node(node_id=node_id)
        for iif in interfaces:
            self.remove_cp_and_links(node_id=iif)

    def remove_cp_and_links(self, node_id: str):
        """
        Remove ConnectionPoint and links. Parent ConnectionPoints and links are removed
        if they have no other children or other connected connection points.
        :param node_id: interface node id
        :return:
        """
        # some interfaces may have parent interfaces, which can be deleted if they only have the
        # one child
        interfaces_to_delete = {node_id}
        parents = self.get_first_neighbor(node_id=node_id,
                                          rel=ABCPropertyGraph.REL_CONNECTS,
                                          node_label=ABCPropertyGraph.CLASS_ConnectionPoint)
        for parent in parents:  # really should only be one parent interface
            children = self.get_first_neighbor(node_id=parent,
                                               rel=ABCPropertyGraph.REL_CONNECTS,
                                               node_label=ABCPropertyGraph.CLASS_ConnectionPoint)
            if len(children) == 1:  # if only child, can delete parent
                interfaces_to_delete.add(parent)
        # interfaces themselves and parent interfaces
        # may be connected to links which can be deleted if nothing
        # else connects to them
        links_to_delete = set()
        for interface in interfaces_to_delete:
            links = self.get_first_neighbor(node_id=interface,
                                            rel=ABCPropertyGraph.REL_CONNECTS,
                                            node_label=ABCPropertyGraph.CLASS_Link)
            for link in links:  # should only be one
                connected_interfaces = self.get_first_neighbor(node_id=link,
                                                               rel=ABCPropertyGraph.REL_CONNECTS,
                                                               node_label=ABCPropertyGraph.CLASS_ConnectionPoint)
                if len(connected_interfaces) == 2:  # connected to us and another thing, can delete
                    links_to_delete.add(link)
        # delete nodes in these sets
        for deleted_id in interfaces_to_delete.union(links_to_delete):
            self.delete_node(node_id=deleted_id)

    def add_network_node_sliver(self, *, sliver: NodeSliver):

        assert sliver is not None
        assert sliver.node_id is not None
        assert self.check_node_unique(label=ABCPropertyGraph.CLASS_NetworkNode, name=sliver.resource_name)

        props = self.node_sliver_to_graph_properties_dict(sliver)
        self.add_node(node_id=sliver.node_id, label=ABCPropertyGraph.CLASS_NetworkNode, props=props)
        # if components aren't empty, add components, their switch fabrics and interfaces
        aci = sliver.attached_components_info
        if aci is not None:
            for csliver in aci.devices.values():
                self.add_component_sliver(parent_node_id=sliver.node_id,
                                          component=csliver)
        # if switch fabrics arent empty add them with their interfaces
        sfi = sliver.switch_fabric_info
        if sfi is not None:
            for sf in sfi.switch_fabrics.values():
                self.add_switch_fabric_sliver(parent_node_id=sliver.node_id,
                                              switch_fabric=sf)

    def add_network_link_sliver(self, *, lsliver: NetworkLinkSliver, interfaces: List[str]):

        assert lsliver is not None
        assert lsliver.node_id is not None
        assert self.check_node_unique(label=ABCPropertyGraph.CLASS_Link, name=lsliver.resource_name)
        assert interfaces is not None

        props = self.link_sliver_to_graph_properties_dict(lsliver)
        self.add_node(node_id=lsliver.node_id, label=ABCPropertyGraph.CLASS_Link, props=props)
        # add edge links to specified interfaces
        for i in interfaces:
            self.add_link(node_a=lsliver.node_id, rel=ABCPropertyGraph.REL_CONNECTS, node_b=i)

    def add_component_sliver(self, *, parent_node_id: str, component: ComponentSliver):
        """
        Add network node component as a sliver, linking back to parent
        :param parent_node_id:
        :param component:
        :return:
        """
        assert component.node_id is not None
        assert parent_node_id is not None
        assert self.check_node_unique(label=ABCPropertyGraph.CLASS_Component, name=component.resource_name)
        props = self.component_sliver_to_graph_properties_dict(component)
        self.add_node(node_id=component.node_id, label=ABCPropertyGraph.CLASS_Component, props=props)
        self.add_link(node_a=parent_node_id, rel=ABCPropertyGraph.REL_HAS, node_b=component.node_id)
        sfi = component.switch_fabric_info
        if sfi is not None:
            for sf in sfi.switch_fabrics.values():
                self.add_switch_fabric_sliver(parent_node_id=component.node_id,
                                              switch_fabric=sf)

    def add_switch_fabric_sliver(self, *, parent_node_id: str, switch_fabric: SwitchFabricSliver):
        """
        Add switch fabric as a sliver to either node or component, linking back to parent.
        :param parent_node_id:
        :param switch_fabric:
        :return:
        """
        assert parent_node_id is not None
        assert switch_fabric.node_id is not None
        assert self.check_node_unique(label=ABCPropertyGraph.CLASS_SwitchFabric,
                                      name=switch_fabric.resource_name)
        props = self.switch_fabric_sliver_to_graph_properties_dict(switch_fabric)
        self.add_node(node_id=switch_fabric.node_id, label=ABCPropertyGraph.CLASS_SwitchFabric, props=props)
        self.add_link(node_a=parent_node_id, rel=ABCPropertyGraph.REL_HAS, node_b=switch_fabric.node_id)
        ii = switch_fabric.interface_info
        if ii is not None:
            for i in ii.interfaces.values():
                self.add_interface_sliver(parent_node_id=switch_fabric.node_id,
                                          interface=i)

    def add_interface_sliver(self, *, parent_node_id: str, interface: InterfaceSliver):
        """
        Add interface to a switch fabric, linking back to parent.
        :param parent_node_id: switch fabric id
        :param interface: interface sliver description
        :return:
        """
        assert interface.node_id is not None
        assert parent_node_id is not None
        assert self.check_node_unique(label=ABCPropertyGraph.CLASS_ConnectionPoint, name=interface.resource_name)
        props = self.interface_sliver_to_graph_properties_dict(interface)
        self.add_node(node_id=interface.node_id, label=ABCPropertyGraph.CLASS_ConnectionPoint, props=props)
        self.add_link(node_a=parent_node_id, rel=ABCPropertyGraph.REL_CONNECTS, node_b=interface.node_id)

    def build_deep_node_sliver(self, *, node_id: str) -> NodeSliver:
        """
        Build a deep NetworkNode or other similar (e.g.
        network-attached storage) sliver from a graph node
        :param node_id:
        :return:
        """
        clazzes, props = self.get_node_properties(node_id=node_id)
        if ABCPropertyGraph.CLASS_NetworkNode not in clazzes:
            raise PropertyGraphQueryException(node_id=node_id, graph_id=self.graph_id,
                                              msg="Node is not of class NetworkNode")
        # create top-level sliver
        ns = self.node_sliver_from_graph_properties_dict(props)
        # find and build deep slivers of switch fabrics (if any) and components (if any)
        comps = self.get_first_neighbor(node_id=node_id, rel=ABCPropertyGraph.REL_HAS,
                                        node_label=ABCPropertyGraph.CLASS_Component)
        if comps is not None and len(comps) > 0:
            aci = AttachedComponentsInfo()
            for c in comps:
                cs = self.build_deep_component_sliver(node_id=c)
                aci.add_device(cs)
            ns.attached_components_info = aci

        sfs = self.get_first_neighbor(node_id=node_id, rel=ABCPropertyGraph.REL_HAS,
                                      node_label=ABCPropertyGraph.CLASS_SwitchFabric)
        if sfs is not None and len(sfs) > 0:
            sfi = SwitchFabricInfo()
            for s in sfs:
                sfsl = self.build_deep_sf_sliver(node_id=s)
                sfi.add_switch_fabric(sfsl)
            ns.switch_fabric_info = sfi

        return ns

    def build_deep_sf_sliver(self, *, node_id: str) -> SwitchFabricSliver:
        clazzes, props = self.get_node_properties(node_id=node_id)
        if ABCPropertyGraph.CLASS_SwitchFabric not in clazzes:
            raise PropertyGraphQueryException(node_id=node_id, graph_id=self.graph_id,
                                              msg="Node is not of class SwitchFabric")
        # create top-level sliver
        sfs = self.switch_fabric_sliver_from_graph_properties_dict(props)
        # find interfaces and attach
        ifs = self.get_first_neighbor(node_id=node_id, rel=ABCPropertyGraph.REL_CONNECTS,
                                      node_label=ABCPropertyGraph.CLASS_ConnectionPoint)
        if ifs is not None and len(ifs) > 0:
            ifi = InterfaceInfo()
            for i in ifs:
                _, iprops = self.get_node_properties(node_id=i)
                ifsl = self.interface_sliver_from_graph_properties_dict(iprops)
                ifi.add_interface(ifsl)
            sfs.interface_info = ifi
        return sfs

    def build_deep_component_sliver(self, *, node_id: str) -> ComponentSliver:
        clazzes, props = self.get_node_properties(node_id=node_id)
        if ABCPropertyGraph.CLASS_Component not in clazzes:
            raise PropertyGraphQueryException(node_id=node_id, graph_id=self.graph_id,
                                              msg="Node is not of class Component")
        # create top-level sliver
        cs = self.component_sliver_from_graph_properties_dict(props)
        # find any switch fabrics, build and attach
        sfs = self.get_first_neighbor(node_id=node_id, rel=ABCPropertyGraph.REL_HAS,
                                      node_label=ABCPropertyGraph.CLASS_SwitchFabric)
        if sfs is not None and len(sfs) > 0:
            sfi = SwitchFabricInfo()
            for s in sfs:
                sfsl = self.build_deep_sf_sliver(node_id=s)
                sfi.add_switch_fabric(sfsl)
            cs.switch_fabric_info = sfi
        return cs