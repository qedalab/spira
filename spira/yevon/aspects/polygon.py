import gdspy
import hashlib
import numpy as np

from spira.yevon.utils import clipping
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.gdsii.elem_list import ElementalList
from spira.yevon.aspects.clipper import __ClipperAspects__
from spira.yevon.aspects.geometry import __GeometryAspects__
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class PolygonAspects(__GeometryAspects__):
    """

    Examples
    --------
    """

    @property
    def points(self):
        return self.shape.points

    @property
    def area(self):
        return gdspy.Polygon(self.shape.points).area()

    @property
    def count(self):
        return np.size(self.shape.points, 0)

    @property
    def process(self):
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        return layer.process.symbol

    @property
    def purpose(self):
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        return layer.purpose.symbol

    @property
    def center(self):
        return self.bbox_info.center

    @property
    def bbox_info(self):
        return self.shape.bbox_info.transform_copy(self.transformation)

    @property
    def hash_polygon(self):
        pts = np.array([self.shape.points])
        return np.sort([hashlib.sha1(p).digest() for p in pts])


class PolygonClipperAspects(__ClipperAspects__):
    """

    Examples
    --------
    """

    def __and__(self, other):
        from copy import deepcopy
        if self.layer == other.layer:
            s1 = self.shape.transform_copy(self.transformation)
            s2 = other.shape.transform_copy(other.transformation)
            shapes = s1.__and__(s2)
            elems = [Polygon(shape=s, layer=self.layer) for s in shapes]
            return elems
        return ElementalList([])

    def __sub__(self, other):
        if self.layer == other.layer:
            s1 = self.shape.transform_copy(self.transformation)
            s2 = other.shape.transform_copy(other.transformation)
            shapes = s1.__sub__(s2)
            elems = [Polygon(shape=s, layer=self.layer) for s in shapes]
            return elems
        return ElementalList([self])

    def __or__(self, other):
        if self.layer == other.layer:
            s1 = self.shape.transform_copy(self.transformation)
            s2 = other.shape.transform_copy(other.transformation)
            shapes = s1.__or__(s2)
            elems = [Polygon(shape=s, layer=self.layer) for s in shapes]
            return elems
        return ElementalList([self, other])


# class PolygonClipperAspects(__ClipperAspects__):
#     """

#     Examples
#     --------
#     """

#     def __and__(self, other):
#         from copy import deepcopy
#         if self.layer == other.layer:
#             shapes = self.shape.__and__(other.shape)
#             elems = [Polygon(shape=s, layer=self.layer) for s in shapes]
#             return elems
#         return ElementalList([])

#     def __sub__(self, other):
#         if self.layer == other.layer:
#             shapes = self.shape.__sub__(other.shape)
#             elems = [Polygon(shape=s, layer=self.layer) for s in shapes]
#             return elems
#         return ElementalList([self])

#     def __or__(self, other):
#         if self.layer == other.layer:
#             shapes = self.shape.__or__(other.shape)
#             elems = [Polygon(shape=s, layer=self.layer) for s in shapes]
#             return elems
#         return ElementalList([self, other])

