# import numpy as np

# from .variables import *

# from spira.core.descriptor import DataField
# from spira.core.descriptor import FunctionField
# from spira.core.descriptor import DataFieldDescriptor
# from spira.core.param.restrictions import RestrictType


# # def CoordField(**kwargs):
# #     from spira.yevon.geometry.coord import Coord
# #     if 'default' not in kwargs:
# #         kwargs['default'] = Coord(0,0)
# #     R = RestrictType(Coord)
# #     return DataFieldDescriptor(restrictions=R, **kwargs)
    

# # def TransformationField(name='noname', number=0, datatype=0, **kwargs):
# #     from spira.core.transformation import Transform
# #     # if 'default' not in kwargs:
# #     #     kwargs['default'] = Layer(name=name, number=number, datatype=datatype, **kwargs)
# #     R = RestrictType(Transform)
# #     return DataFieldDescriptor(restrictions=R, **kwargs)


# def LayerField(name='noname', number=0, datatype=0, **kwargs):
#     from spira.yevon.layer import Layer
#     if 'default' not in kwargs:
#         kwargs['default'] = Layer(name=name, number=number, datatype=datatype, **kwargs)
#     R = RestrictType(Layer)
#     return DataFieldDescriptor(restrictions=R, **kwargs)


# def ColorField(red=0, green=0, blue=0, **kwargs):
#     from spira.yevon.visualization.color import Color
#     if 'default' not in kwargs:
#         kwargs['default'] = Color(red=0, green=0, blue=0, **kwargs)
#     R = RestrictType(Color)
#     return DataFieldDescriptor(restrictions=R, **kwargs)


# def LabelField(position=[[], []], **kwargs):
#     from spira.yevon.gdsii.label import Label
#     if 'default' not in kwargs:
#         kwargs['default'] = Label(position=position)
#     R = RestrictType(Label)
#     return DataFieldDescriptor(restrictions=R, **kwargs)


# def PortField(midpoint=[0, 0], **kwargs):
#     # from spira.yevon.gdsii.port import Port
#     from spira.yevon.geometry.ports.port import Port
#     if 'default' not in kwargs:
#         kwargs['default'] = Port(midpoint=midpoint)
#     R = RestrictType(Port)
#     return DataFieldDescriptor(restrictions=R, **kwargs)


# def TermField(midpoint=[0, 0], **kwargs):
#     from spira.yevon.gdsii.term import Term
#     if 'default' not in kwargs:
#         kwargs['default'] = Terminal(midpoint=midpoint)
#     R = RestrictType(Term)
#     return DataFieldDescriptor(restrictions=R, **kwargs)


# def ShapeField(points=[], doc='', **kwargs):
#     from spira.yevon.geometry.shapes.shape import Shape
#     if 'default' not in kwargs:
#         kwargs['default'] = Shape(points, doc=doc)
#     R = RestrictType(Shape)
#     return DataFieldDescriptor(restrictions=R, **kwargs)


# # def CellField(name=None, elementals=None, ports=None, library=None, **kwargs):
# #     from spira.yevon.gdsii.cell import Cell
# #     if 'default' not in kwargs:
# #         kwargs['default'] = Cell(name=name, elementals=elementals, library=library)
# #     R = RestrictType(Cell)
# #     return DataFieldDescriptor(restrictions=R, **kwargs)


# def PurposeLayerField(name='', datatype=0, symbol='', **kwargs):
#     from spira.yevon.rdd.layer import PurposeLayer
#     if 'default' not in kwargs:
#         kwargs['default'] = PurposeLayer(name=name, datatype=datatype, symbol='')
#     R = RestrictType(PurposeLayer)
#     return DataFieldDescriptor(restrictions=R, **kwargs)


# def PhysicalLayerField(layer=None, purpose=None, **kwargs):
#     from spira.yevon.rdd.layer import PhysicalLayer
#     if 'default' not in kwargs:
#         kwargs['default'] = PhysicalLayer(layer=layer, purpose=purpose)
#     R = RestrictType(PhysicalLayer)
#     return DataFieldDescriptor(restrictions=R, **kwargs)


# def PolygonField(shape=[[], []], **kwargs):
#     from spira.yevon.gdsii.polygon import Polygon
#     if 'default' not in kwargs:
#         kwargs['default'] = Polygon(shape=shape)
#     R = RestrictType(Polygon)
#     return DataFieldDescriptor(restrictions=R, **kwargs)
    

# def DesignRuleField(shape=[[], []], **kwargs):
#     from spira.lrc.rules import __DesignRule__
#     R = RestrictType(__DesignRule__)
#     return DataFieldDescriptor(restrictions=R, **kwargs)


# class ElementalListField(DataFieldDescriptor):
#     from spira.core.elem_list import ElementList
#     __type__ = ElementList

#     def __init__(self, default=[], **kwargs):
#         kwargs['default'] = self.__type__(default)
#         kwargs['restrictions'] = RestrictType([self.__type__])
#         super().__init__(**kwargs)

#     def __repr__(self):
#         return ''

#     def __str__(self):
#         return ''

#     def call_param_function(self, obj):
#         f = self.get_param_function(obj)
#         value = f(self.__type__())
#         if value is None:
#             value = self.__type__()
#         obj.__store__[self.__name__] = value
#         return value


# # class MidPointField(DataFieldDescriptor):
# #     from spira.yevon.geometry.coord import Coord
# #     __type__ = Coord

# #     def __init__(self, default=Coord(0,0), **kwargs):
# #         if isinstance(default, self.__type__):
# #             kwargs['default'] = [default.x, default.y]
# #         elif isinstance(default, (list, set, tuple, np.ndarray)):
# #             kwargs['default'] = default
# #         super().__init__(**kwargs)

# #     def get_stored_value(self, obj):
# #         value = obj.__store__[self.__name__]
# #         if not isinstance(value, (list, set, tuple, np.ndarray)):
# #             raise ValueError('Correct MidPoint type to retreived.')
# #         return list(value)

# #     def __set__(self, obj, value):
# #         if isinstance(value, self.__type__):
# #             value = self.__type__()
# #         elif isinstance(value, (list, set, tuple, np.ndarray)):
# #             value = self.__type__(value[0], value[1])
# #         else:
# #             raise TypeError("Invalid type value of {} (expected {}), but received {}".format(self.__class__, self.__type__,  type(value)))

# #         obj.__store__[self.__name__] = [value.x, value.y]


# class PointArrayField(DataFieldDescriptor):
#     import numpy as np
#     __type__ = np.array([])

#     def call_param_function(self, obj):
#         f = self.get_param_function(obj)
#         value = f([])
#         if value is None:
#             value = self.__operations__([])
#         else:
#             value = self.__operations__(value)
#         obj.__store__[self.__name__] = value
#         return value 
#         # if (value is None):
#         #     value = self.__process__([])
#         # else:
#         #     value = self.__process__([c.to_nparray() if isinstance(c, Coord) else c for c in value])
#         # return value 

#     def __operations__(self, points):
#         return points

#     # def __process__(self, points):
#     def __operations__(self, points):
#         from spira.yevon.geometry.shapes.shape import Shape
#         if isinstance(points, Shape):
#             return array(points.points)
#         elif isinstance(points, (list, np.ndarray)):
#             if len(points):
#                 element = points[0]
#                 if isinstance(element, (np.ndarray, list)):
#                     points_as_array = np.array(points, copy=False)
#                 else:
#                     points_as_array = np.array([(c[0], c[1]) for c in points])
#                 return points_as_array
#             else:
#                 return np.ndarray((0, 2))
#         # elif isinstance(points, Coord2):
#         #     return array([[points.x, points.y]])
#         # elif isinstance(points, tuple):
#         #     return array([[points[0], points[1]]])
#         else:
#             raise TypeError("Invalid type of points in setting value of PointsDefinitionProperty: " + str(type(points))) 

#     def __set__(self, obj, points):
#         obj.__store__[self.__name__] = points
        
#     # def __deepcopy__(self, memo):
#     #     from copy import deepcopy
#     #     return deepcopy(obj)
    

# # class PortListField(DataFieldDescriptor):
# #     from spira.core.port_list import PortList
# #     __type__ = PortList

# #     def __init__(self, default=[], **kwargs):
# #         kwargs['default'] = self.__type__(default)
# #         kwargs['restrictions'] = RestrictType([self.__type__])
# #         super().__init__(**kwargs)

# #     def __repr__(self):
# #         return ''

# #     def __str__(self):
# #         return ''

# #     def call_param_function(self, obj):
# #         f = self.get_param_function(obj)
# #         value = f(self.__type__())
# #         if value is None:
# #             value = self.__type__()
# #         obj.__store__[self.__name__] = value
# #         return value
