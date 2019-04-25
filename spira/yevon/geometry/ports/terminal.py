import gdspy
import pyclipper
import numpy as np
import spira.all as spira
from copy import copy, deepcopy
from numpy.linalg import norm
from spira.yevon import utils

from spira.core import param
from spira.yevon.gdsii.base import __Elemental__
from spira.yevon.rdd import get_rule_deck

from spira.core.param.variables import *
from spira.yevon.layer import LayerField
from spira.core.descriptor import DataField
from spira.yevon.geometry.coord import CoordField
from spira.core.descriptor import DataField, FunctionField
from spira.yevon.geometry.ports.base import __HorizontalPort__
from spira.yevon.gdsii.group import Group
from spira.yevon.geometry.coord import Coord


RDD = get_rule_deck()


class Terminal(__HorizontalPort__):
    """  """

    width = NumberField(default=2*1e6)

    edgelayer = LayerField(name='Edge', number=63)
    arrowlayer = LayerField(name='Arrow', number=77)

    edge = DataField(fdef_name='create_edge')
    arrow = DataField(fdef_name='create_arrow')

    def get_length(self):
        if not hasattr(self, '__length__'):
            key = self.gds_layer.name
            if key in RDD.keys:
                if RDD.name == 'MiTLL':
                    self.__length__ = RDD[key].MIN_SIZE * 1e6
                elif RDD.name == 'AiST':
                    self.__length__ = RDD[key].WIDTH * 1e6
            else:
                self.__length__ = RDD.GDSII.TERM_WIDTH
        return self.__length__

    def set_length(self, value):
        self.__length__ = value

    length = FunctionField(get_length, set_length, doc='Set the width of the terminal edge.')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return ("[SPiRA: Terminal] (name {}, midpoint {} orientation {})").format(self.name, self.midpoint, self.orientation)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return (self.name == other.name)
        # print(self.midpoint)
        # print(other.midpoint)
        # if not isinstance(self.midpoint, Coord):
        #     self.midpoint = Coord(self.midpoint[0], self.midpoint[1])
        # return (self.midpoint == other.midpoint and (self.orientation == other.orientation))

    def __ne__(self, other):
        return (self.midpoint != other.midpoint or (self.orientation != other.orientation)) 

    def transform(self, transformation):
        if transformation is not None:
            transformation.apply_to_object(self)
        return self
        
    def transform_copy(self, transformation):
        T = deepcopy(self)
        T.transform(transformation)
        return T

    def commit_to_gdspy(self, cell=None, transformation=None):
        if self.__repr__() not in list(Terminal.__committed__.keys()):
            self.edge.commit_to_gdspy(cell=cell, transformation=transformation)
            self.arrow.commit_to_gdspy(cell=cell, transformation=transformation)
            self.label.commit_to_gdspy(cell=cell, transformation=transformation)
            Terminal.__committed__.update({self.__repr__(): self})
        else:
            p = Terminal.__committed__[self.__repr__()]
            p.edge.commit_to_gdspy(cell=cell)
            p.arrow.commit_to_gdspy(cell=cell)
            p.label.commit_to_gdspy(cell=cell)

    def create_edge(self):
        from spira.yevon.geometry import shapes
        dx = self.length
        dy = self.width - dx
        rect_shape = shapes.RectangleShape(p1=[0, 0], p2=[dx, dy])
        tf = spira.Translation(self.midpoint) + spira.Rotation(self.orientation - 90)
        ply = spira.Polygon(shape=rect_shape, gds_layer=self.edgelayer)
        ply.center = (0,0)
        ply.transform(tf)
        # ply.__rotate__(angle=self.orientation-90)
        # ply.__translate__(dx=self.midpoint[0], dy=self.midpoint[1])
        return ply

    def create_arrow(self):
        from spira.yevon.geometry import shapes
        arrow_shape = shapes.ArrowShape(a=self.length, b=self.length/2, c=self.length*2)
        arrow_shape.apply_merge
        tf = spira.Translation(self.midpoint) + spira.Rotation(self.orientation)
        # tf = spira.Translation(self.midpoint) + spira.Rotation(self.orientation - 90)
        # ply = spira.Polygon(shape=arrow_shape, gds_layer=self.arrowlayer, transformation=tf)
        ply = spira.Polygon(shape=arrow_shape, gds_layer=self.arrowlayer)
        ply.center = (0,0)
        ply.transform(tf)
        return ply

    def encloses(self, points):
        if pyclipper.PointInPolygon(self.endpoints[0], points) != 0:
            return True
        elif pyclipper.PointInPolygon(self.endpoints[1], points) != 0:
            return True

    def encloses_midpoint(self, points):
        return pyclipper.PointInPolygon(self.midpoint, points) != 0

    @property
    def endpoints(self):
        dx = self.length/2*np.cos((self.orientation - 90)*np.pi/180)
        dy = self.length/2*np.sin((self.orientation - 90)*np.pi/180)
        left_point = self.midpoint - np.array([dx,dy])
        right_point = self.midpoint + np.array([dx,dy])
        return np.array([left_point, right_point])

    @endpoints.setter
    def endpoints(self, points):
        p1, p2 = np.array(points[0]), np.array(points[1])
        self.midpoint = (p1+p2)/2
        dx, dy = p2-p1
        self.orientation = np.arctan2(dx,dy)*180/np.pi
        self.width = np.sqrt(dx**2 + dy**2)

    # def create_elementals(self, elems):
    #     # elems += self.edge
    #     # elems += self.arrow
    #     # elems += self.label
    #     return elems


class EdgeTerminal(Terminal):
    """
    Terminals are horizontal ports that connect SRef instances
    in the horizontal plane. They typcially represents the
    i/o ports of a components.

    Examples
    --------
    >>> term = spira.Terminal()
    """

    def __repr__(self):
        return ("[SPiRA: EdgeTerm] (name {}, number {}, datatype {}, midpoint {}, " +
            "width {}, orientation {})").format(self.name,
            self.gds_layer.number, self.gds_layer.datatype, self.midpoint,
            self.width, self.orientation
        )

    def __reflect__(self):
        """ Do not reflect EdgeTerms when reference is reflected. """
        self.midpoint = [self.midpoint[0], -self.midpoint[1]]
        self.orientation = 180 - self.orientation
        self.orientation = np.mod(self.orientation, 360)
        return self

