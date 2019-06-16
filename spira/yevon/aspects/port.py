from spira.yevon.aspects.base import __Aspects__
from spira.yevon.geometry.ports.port_list import PortListField
from spira.core.transformable import Transformable
from spira.yevon.gdsii.elem_list import ElementalListField
from spira.core.parameters.descriptor import DataField
from spira.yevon.process.gdsii_layer import LayerField
from spira.core.parameters.variables import *
from spira.yevon import constants
from spira.yevon.geometry.ports.port import Port
from spira.yevon.process.gdsii_layer import Layer
from spira.yevon.geometry import shapes
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class PortProperty(__Aspects__):
    """ Port properties that connects to layout structures. """

    disable_edge_ports = BoolField(default=False, doc='Disable the viewing of polygon edge ports.')

    ports = PortListField(fdef_name='__create_ports__', doc='List of ports to be added to the cell instance.')

    def __create_ports__(self, ports):
        return self.create_ports(ports)

    def create_ports(self, ports):
        return ports


class CellPortProperty(PortProperty):
    def __create_ports__(self, ports):
        from spira.yevon.gdsii.polygon import Polygon
        for e in self.elementals:
            if isinstance(e, Polygon):
                for p in e.ports:
                    ports += p
        return self.create_ports(ports)


class TransformablePortProperty(PortProperty, Transformable):
    def __create_ports__(self, ports):
        ports = self.create_ports(ports).transform_copy(self.transformation)
        # ports = self.create_ports(ports)
        return ports


class SRefPortProperty(TransformablePortProperty):
    def create_ports(self, ports):
        from copy import deepcopy
        pp = deepcopy(self.ref.ports)
        ports = pp.move(self.midpoint)
        # ports = pp.move_new(self.midpoint)
        # ports = pp.transform_copy(self.transformation).move(self.midpoint)
        # ports = pp.move(self.midpoint).transform(-self.transformation)
        # ports = pp.move(self.midpoint).transform_copy(self.transformation)
        # ports = pp.transform_copy(self.transformation).move(self.midpoint).transform(-self.transformation)
        # ports = pp.transform_copy(self.transformation).move(self.midpoint)
        # ports = pp.transform_copy(self.transformation)
        # ports = pp.transform_copy(self.transformation).move_new(self.midpoint).transform(-self.transformation)
        return ports


# class PolygonPortProperty(TransformablePortProperty):
class PolygonPortProperty(PortProperty):

    edge_ports = ElementalListField()

    metal_port = DataField(fdef_name='create_metal_port')
    contact_ports = DataField(fdef_name='create_contact_ports')

    layer1 = LayerField()
    layer2 = LayerField()

    def create_metal_port(self):
        layer = Layer(
            name=self.name,
            number=self.layer.layer.number,
            datatype=RDD.PURPOSE.METAL.datatype
        )
        return Port(
            name='P_metal',
            midpoint=self.polygon.center,
            gds_layer=layer
        )

    def create_contact_ports(self):
        l1 = Layer(
            name=self.name,
            number=self.layer1.number,
            datatype=RDD.PURPOSE.PRIM.VIA.datatype
        )
        p1 = Port(
            name='P_contact_1',
            midpoint=self.shape.bbox_info.center,
            gds_layer=l1
        )
        l2 = Layer(
            name=self.name,
            number=self.layer2.number,
            datatype=RDD.PURPOSE.PRIM.VIA.datatype
        )
        p2 = Port(
            name='P_contact_2',
            midpoint=self.shape.bbox_info.center,
            gds_layer=l2
        )
        return [p1, p2]

    def create_edge_ports(self, edges):
        from copy import deepcopy
        # T = deepcopy(self.transformation)
        T = self.transformation
        # shape = self.shape.transform(T)
        shape = deepcopy(self.shape).transform(T)
        # shape = self.shape
        return shapes.shape_edge_ports(shape, self.layer, self.id_string())

    def create_ports(self, ports):
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        if layer.purpose.symbol == 'METAL':
            for edge in self.edge_ports:
                ports += edge
        # ports.transform(-self.transformation)
        return ports

    # def create_ports(self, ports):
    #     # if self.enable_edges:
    #     if self.layer.purpose == RDD.PURPOSE.JUNCTION:
    #         ports += self.contact_ports
    #     elif self.layer.purpose == RDD.PURPOSE.VIA:
    #         ports += self.contact_ports
    #     elif self.layer.purpose == RDD.PURPOSE.METAL:
    #         if self.level == 1:
    #             ports += self.metal_port
    #         for edge in self.edge_ports:
    #             ports += edge
    #     elif self.layer.purpose == RDD.PURPOSE.PROTECTION:
    #         for edge in self.edge_ports:
    #             ports += edge
    #     return ports
            
    

