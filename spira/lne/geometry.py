import os
import spira
import pygmsh
import meshio
import inspect

from spira.core.lists import ElementList
# from spira.gdsii.utils import numpy_to_list
from spira import param
from spira.lne.mesh import Mesh
from spira.core.initializer import ElementalInitializer


class __Geometry__(ElementalInitializer):

    def __init__(self, lcar, **kwargs):

        ElementalInitializer.__init__(self, **kwargs)

        self.extrude = []
        self.volume = []

        self.geom = pygmsh.opencascade.Geometry(
            characteristic_length_min=lcar,
            characteristic_length_max=lcar
        )

        self.geom.add_raw_code('Mesh.Algorithm = {};'.format(self.algorithm))
        self.geom.add_raw_code('Coherence Mesh;')

        self.mesh = None

    def __surfaces__(self):
        surfaces = []
        for e in self.elements:
            if isinstance(e, pygmsh.built_in.plane_surface.PlaneSurface):
                surfaces.append(e)
        return surfaces


class GeometryAbstract(__Geometry__):

    _ID = 0

    name = param.StringField()
    layer = param.IntegerField()
    dimension = param.IntegerField(default=2)
    algorithm = param.IntegerField(default=6)
    polygons = param.ElementListField()
    # gmsh_elements = param.ElementListField()

    create_mesh = param.DataField(fdef_name='create_meshio')
    elements = param.DataField(fdef_name='create_pygmsh_elements')

    def __init__(self, lcar=0.01, **kwargs):
        super().__init__(lcar=lcar, **kwargs)

    def create_meshio(self):
        """
        Generates a GMSH mesh, which is saved in the `debug` folder.

        Arguments
        ---------
        mesh : dict
            Dictionary containing all the necessary mesh information.
        """

        if len(self.__surfaces__()) > 1:
            self.geom.boolean_union(self.__surfaces__())

        directory = os.getcwd() + '/debug/gmsh/'
        mesh_file = '{}{}.msh'.format(directory, self.name)
        geo_file = '{}{}.geo'.format(directory, self.name)
        vtk_file = '{}{}.vtu'.format(directory, self.name)

        if not os.path.exists(directory):
            os.makedirs(directory)

        mesh_data = pygmsh.generate_mesh(self.geom,
                                         verbose=False,
                                         dim=self.dimension,
                                         prune_vertices=False,
                                         remove_faces=False,
                                         geo_filename=geo_file)

        mm = meshio.Mesh(*mesh_data)

        meshio.write(mesh_file, mm)
        meshio.write(vtk_file, mm)

        # params = {
        #     'name': self.name,
        #     'layer': spira.Layer(number=self.layer),
        #     'points': [mesh_data[0]],
        #     'cells': [mesh_data[1]],
        #     'point_data': [mesh_data[2]],
        #     'cell_data': [mesh_data[3]],
        #     'field_data': [mesh_data[4]]
        # }

        # return params

        return mesh_data

    def create_pygmsh_elements(self):
        print('number of polygons {}'.format(len(self.polygons)))

        height = 0.0
        holes = None

        elems = ElementList()
        for ply in self.polygons:
            for i, points in enumerate(ply.polygons):
                pp = numpy_to_list(points, height, unit=10e-9)
                surface_label = '{}_{}_{}_{}'.format(ply.gdslayer.number,
                                                     ply.gdslayer.datatype,
                                                     GeometryAbstract._ID, i)
                gp = self.geom.add_polygon(pp, lcar=1.0,
                                           make_surface=True,
                                           holes=holes)
                self.geom.add_physical_surface(gp.surface, label=surface_label)
                elems += [gp.surface, gp.line_loop]
                GeometryAbstract._ID += 1

        return elems

    def extrude_surfaces(self, geom, surfaces):
        """ This extrudes the surface to a 3d volume element. """

        for i, surface in enumerate(surfaces):
            width = float(self.width) * scale

            ex = self.geom.extrude(surface, [0, 0, width])

            unique_id = '{}_{}'.format(polygons._id, i)

            volume = self.geom.add_physical_volume(ex[1], unique_id)

            self.extrude.append(ex[1])
            self.volume.append(volume)

    def geom_holes(self):
        """
        Create a list of gmsh surfaces from the mask polygons
        generated by the gdsii package.

        Arguments
        ---------
        surfaces : list
            list of pygmsh surface objects.
        """

        print('number of polygons {}'.format(len(self.e.polygons)))

        dim = 2
        height = 0.0
        material_stack = None

        for i, points in enumerate(self.e.polygons):
            if dim == 3:
                height = self.vertical_position(material_stack)

            pp = numpy_to_list(points, height, unit=self.e.unit)

            gp = geom.add_polygon(pp, lcar=1.0, make_surface=true)

            line_loops.append(gp.line_loop)

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        return self

    def flatten(self):
        return [self]

    def commit_to_gdspy(self, cell):
        pass

    def transform(self, transform):
        return self


class Geometry(GeometryAbstract):
    pass
