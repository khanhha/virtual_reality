#!/usr/bin/python

### import guacamole libraries
import avango
import avango.gua


### import python libraries




class Scene:

    ## constructor
    def __init__(self,
        PARENT_NODE = None,
        ):


        self.scene_root = avango.gua.nodes.TransformNode(Name = "town")
        PARENT_NODE.Children.value.append(self.scene_root)        

        
        ## init scene geometries        
        _loader = avango.gua.nodes.TriMeshLoader() # get trimesh loader to load external meshes

        # water
        self.water_geometry = _loader.create_geometry_from_file("water_geometry", "data/objects/plane.obj", avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS)
        self.water_geometry.Transform.value = avango.gua.make_trans_mat(0.0,-0.35,0.0) * avango.gua.make_scale_mat(200.0)
        self.water_geometry.Material.value.set_uniform("Roughness", 0.4)
        self.scene_root.Children.value.append(self.water_geometry)

        # harbor
        self.town = _loader.create_geometry_from_file("town", "data/objects/medieval_harbour/town.obj", avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.LOAD_MATERIALS | avango.gua.LoaderFlags.MAKE_PICKABLE)
        self.town.Transform.value = avango.gua.make_scale_mat(7.5)
        self.scene_root.Children.value.append(self.town)

        self.apply_material_uniform(self.town, "Emissivity", 1.0)
        self.apply_material_uniform(self.town, "Metalness", 0.1)
        self.apply_material_uniform(self.town, "Roughness", 0.8)
        self.apply_backface_culling_flag(self.town, False)

        ## init scene light
        self.scene_light = avango.gua.nodes.LightNode(Name = "scene_light", Type = avango.gua.LightType.SPOT)
        self.scene_light.Color.value = avango.gua.Color(1.0, 1.0, 0.8)
        self.scene_light.Brightness.value = 40.0
        self.scene_light.Softness.value = 0.5 # exponent
        self.scene_light.Falloff.value = 0.1 # exponent
        self.scene_light.EnableShadows.value = True
        self.scene_light.ShadowMapSize.value = 2048
        #self.scene_light.ShadowOffset.value = 0.01
        self.scene_light.ShadowMaxDistance.value = 150.0
        self.scene_light.ShadowNearClippingInSunDirection.value = 0.1
        self.scene_light.Transform.value = avango.gua.make_trans_mat(0.0, 120.0, 40.0) * \
            avango.gua.make_rot_mat(-70.0,1,0,0) * \
            avango.gua.make_scale_mat(170)
        self.scene_root.Children.value.append(self.scene_light)
                        

    ## Recursively applies a material uniform to all TriMeshNodes below a given node.
    def apply_material_uniform(self, START_NODE, UNIFORM_NAME, UNIFORM_VALUE):
        if START_NODE.__class__.__name__ == "TriMeshNode":
            START_NODE.Material.value.set_uniform(UNIFORM_NAME, UNIFORM_VALUE)

        for child in START_NODE.Children.value:
            self.apply_material_uniform(child, UNIFORM_NAME, UNIFORM_VALUE)

    ## Recursively applies the backface culling flag to all TriMeshNodes below a given node.
    def apply_backface_culling_flag(self, START_NODE, BOOL):
        if START_NODE.__class__.__name__ == "TriMeshNode":
            START_NODE.Material.value.EnableBackfaceCulling.value = BOOL

        for child in START_NODE.Children.value:
            self.apply_backface_culling_flag(child, BOOL)