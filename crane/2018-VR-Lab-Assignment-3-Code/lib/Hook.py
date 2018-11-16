#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua
import avango.script
from avango.script import field_has_changed


class Hook(avango.script.Script):

    ## declaration of fields
    sf_mat = avango.gua.SFMatrix4()
 
    # constructor
    def __init__(self):
        self.super(Hook).__init__()

    def my_constructor(self,
        PARENT_NODE = None,
        SIZE = 0.1,
        TARGET_LIST = [],
        ):

        ## external references        
        self.TARGET_LIST = TARGET_LIST
        
        # ToDo: init scenegraph node(s) here
        # ...
        #print('hello khanh')        
        _loader = avango.gua.nodes.TriMeshLoader() # get trimesh loader to load external tri-meshes
        self.hook_node = avango.gua.nodes.TransformNode(Name = "hinge{0}_node".format(str(0)))
        PARENT_NODE.Children.value.append(self.hook_node) 

        self.hook_geometry = _loader.create_geometry_from_file("hook{0}_geometry".format(str(1)), "data/objects/sphere.obj", avango.gua.LoaderFlags.DEFAULTS)
        self.hook_geometry.Transform.value = avango.gua.make_scale_mat(SIZE, SIZE, SIZE)
        self.hook_geometry.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,1.0,1.0,1.0))
        self.hook_node.Children.value.append(self.hook_geometry )   

        self.sf_mat.connect_from(self.hook_node.WorldTransform)

    @field_has_changed(sf_mat)
    def sf_mat_changed(self):
        _pos = self.sf_mat.value.get_translate() # world position of hook
        
        #print('sf_mat_changed(self)')

        for _node in self.TARGET_LIST: # iterate over all target nodes
            _bb = _node.BoundingBox.value # get bounding box of a node
            #print(_node.Name.value, _bb.contains(_pos))
            
            if _bb.contains(_pos) == True: # hook inside bounding box of this node
                _node.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,0.0,0.0,0.85)) # highlight color
            else:
                _node.Material.value.set_uniform("Color", avango.gua.Vec4(1.0,1.0,1.0,1.0)) # default color
       
