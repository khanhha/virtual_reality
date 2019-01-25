#!/usr/bin/python

### import guacamole libraries
import avango
import avango.gua
import avango.script


class Inputs(avango.script.Script):

    ## input fields
    sf_pointer_button = avango.SFBool()
    sf_pointer_tracking_mat = avango.gua.SFMatrix4()
    
    mf_dof_steering = avango.MFFloat()
    
    sf_technique_button0 = avango.SFBool()
    sf_technique_button1 = avango.SFBool()
    sf_technique_button2 = avango.SFBool()
    sf_technique_button3 = avango.SFBool()
    sf_toggle_technique_button = avango.SFBool()

    sf_reset_button = avango.SFBool()


    ## Default constructor.
    def __init__(self):
        self.super(Inputs).__init__()


    def init_projection_setup(self, POINTER_TRACKING_STATION, POINTER_DEVICE_STATION, KEYBOARD_STATION):
    
        ## init sensors
        self.pointer_tracking_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.pointer_tracking_sensor.Station.value = POINTER_TRACKING_STATION
        self.pointer_tracking_sensor.ReceiverOffset.value = avango.gua.make_trans_mat(0.0,0.0,-0.05)
        
            
        self.pointer_device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.pointer_device_sensor.Station.value = POINTER_DEVICE_STATION
        
        self.keyboard_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.keyboard_sensor.Station.value = KEYBOARD_STATION
        
        
        self.steeringInput = SpacemouseSteeringInput()
        self.steeringInput.my_constructor("gua-device-spacemouse")

        
        ### init field connections
        self.sf_pointer_button.connect_from(self.pointer_device_sensor.Button0)
        self.sf_pointer_tracking_mat.connect_from(self.pointer_tracking_sensor.Matrix)

        self.mf_dof_steering.connect_from(self.steeringInput.mf_dof)

        self.sf_technique_button0.connect_from(self.keyboard_sensor.Button16)
        self.sf_technique_button1.connect_from(self.keyboard_sensor.Button17)
        self.sf_technique_button2.connect_from(self.keyboard_sensor.Button18)
        self.sf_technique_button3.connect_from(self.keyboard_sensor.Button19)        
        self.sf_reset_button.connect_from(self.keyboard_sensor.Button14)
        

    def init_hmd_setup(self, TRACKING_NAME_BASE, VIEWING_SETUP):

        ## init sensors
        self.hmd_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.hmd_sensor.Station.value = TRACKING_NAME_BASE + "-0"

        self.controller1_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.controller1_sensor.Station.value = TRACKING_NAME_BASE + "-1"

        self.steeringInput = ViveSteeringInput()
        self.steeringInput.my_constructor(TRACKING_NAME_BASE + "-1")
              

        ### init field connections
        self.sf_pointer_button.connect_from(self.controller1_sensor.Button4)
        self.sf_pointer_tracking_mat.connect_from(self.controller1_sensor.Matrix)
        
        self.mf_dof_steering.connect_from(self.steeringInput.mf_dof)
        
        self.sf_toggle_technique_button.connect_from(self.controller1_sensor.Button2)
        
        self.sf_reset_button.connect_from(self.controller1_sensor.Button1)


        ## init Vive-Controller visulization
        _loader = avango.gua.nodes.TriMeshLoader()
        
        self.controller_geometry = _loader.create_geometry_from_file("controller_geometry", "data/objects/vive_controller/vive_controller.obj", avango.gua.LoaderFlags.LOAD_MATERIALS)
        self.controller_geometry.Material.value.set_uniform("Roughness", 0.8)
        self.controller_geometry.Material.value.set_uniform("ColorMap", "data/objects/vive_controller/onepointfive_texture.png")
        self.controller_geometry.Transform.connect_from(self.controller1_sensor.Matrix)

        VIEWING_SETUP.navigation_node.Children.value.append(self.controller_geometry)





class MultiDofInput(avango.script.Script):

    ### fields ###
    
    ## output fields
    mf_dof = avango.MFFloat()
    mf_dof.value = [0.0,0.0,0.0,0.0,0.0,0.0] # init 6 channels

  
    ### functions
    def filter_channel(self, VALUE, OFFSET, MIN, MAX, NEG_THRESHOLD, POS_THRESHOLD):
        VALUE = VALUE - OFFSET
        MIN = MIN - OFFSET
        MAX = MAX - OFFSET

        if VALUE > 0:
            _pos = MAX * POS_THRESHOLD * 0.01

            if VALUE > _pos: # above positive threshold
                VALUE = min( (VALUE - _pos) / (MAX - _pos), 1.0) # normalize interval
            else: # below positive threshold
                VALUE = 0

        elif VALUE < 0:
            _neg = MIN * NEG_THRESHOLD * 0.01

            if VALUE < _neg:
                VALUE = max( (VALUE - _neg) / abs(MIN - _neg), -1.0)
            else: # above negative threshold
                VALUE = 0
          
        return VALUE


class SpacemouseSteeringInput(MultiDofInput):
 
    def my_constructor(self, DEVICE_STATION):

        ### resources ###

        ## init device sensors
        self.device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.device_sensor.Station.value = DEVICE_STATION

        ## init callback triggers
        self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)


    ### callback functions ###    
  
    def frame_callback(self): # evaluated every frame            
        _x = self.device_sensor.Value0.value
        _y = self.device_sensor.Value1.value * -1.0
        _z = self.device_sensor.Value2.value
        _rx = self.device_sensor.Value3.value
        _ry = self.device_sensor.Value4.value * -1.0
        _rz = self.device_sensor.Value5.value

        #print(_x, _y, _z, _rx, _ry, _rz)
        
        if _x != 0.0:
            _x = self.filter_channel(_x, 0.0, -350.0, 350.0, 3, 3)
        
        if _y != 0.0:
            _y = self.filter_channel(_y, 0.0, -350.0, 350.0, 3, 3)
          
        if _z != 0.0:
            _z = self.filter_channel(_z, 0.0, -350.0, 350.0, 3, 3)
            
        if _rx != 0.0:
            _rx = self.filter_channel(_rx, 0.0, -350.0, 350.0, 8, 8)
         
        if _ry != 0.0:
            _ry = self.filter_channel(_ry, 0.0, -350.0, 350.0, 8, 8)
        
        if _rz != 0.0:
            _rz = self.filter_channel(_rz, 0.0, -350.0, 350.0, 8, 8)
         
        self.mf_dof.value = [_x,_y,_z,_rx,_ry,_rz,0.0] # propagate input via field connection



class ViveSteeringInput(MultiDofInput):
 
    def my_constructor(self, DEVICE_STATION):

        ### resources ###

        ## init device sensors
        self.device_sensor = avango.daemon.nodes.DeviceSensor(DeviceService = avango.daemon.DeviceService())
        self.device_sensor.Station.value = DEVICE_STATION

        ## init callback triggers
        self.frame_trigger = avango.script.nodes.Update(Callback = self.frame_callback, Active = True)


    ### callback functions ###      
    def frame_callback(self): # evaluated every frame
        _z = self.device_sensor.Value3.value        
        
        self.mf_dof.value = [0.0,0.0,-_z,0.0,0.0,0.0] # propagate input via field connection
                
