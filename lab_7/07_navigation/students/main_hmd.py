#!/usr/bin/python3

## import avango-guacamole libraries
import avango
import avango.gua


## import framework libraries
from lib.Navigation import NavigationManager
from lib.Inputs import Inputs
from lib.Scene import Scene
from lib.ViveViewingSetup import ViveViewingSetup
from lib.UdpReceiver import UdpReceiver

## import python libraries
import builtins


def start():
    scenegraph = avango.gua.nodes.SceneGraph(Name = "scenegraph")
    builtins.SCENEGRAPH = scenegraph

    # init scene
    scene = Scene(PARENT_NODE = scenegraph.Root.value)

    ## create viewing platform
    viewingSetup = ViveViewingSetup(PARENT_NODE = scenegraph.Root.value,
                                    SCENEGRAPH = scenegraph,
                                    BLACK_LIST = ["invisible"]
                                    )

    inputs = Inputs()
    inputs.init_hmd_setup(TRACKING_NAME_BASE = "vive-sensor", VIEWING_SETUP = viewingSetup)


    ## init navigation techniques
    navigationManager = NavigationManager()
    navigationManager.my_constructor(
        SCENEGRAPH = scenegraph,
        VIEWING_SETUP = viewingSetup,
        INPUTS = inputs,
        )


    ## create UdpReceiver to listen for incoming control commands
    udp_receiver = UdpReceiver('127.0.0.1', 7070, handle_message)

    # print complete scenegraph
    print_graph(scenegraph.Root.value)

    # Start application/render loop
    viewingSetup.run(locals(), globals())


def handle_message(MESSAGE):
    try:
        eval(MESSAGE)
    except:
        print("Error parsing command: " + MESSAGE)
        import sys
        print(sys.exc_info())


def print_graph(root_node):
  stack = [(root_node, 0)]
  while stack:
    node, level = stack.pop()
    print("│   " * level + "├── {0} <{1}>".format(
      node.Name.value, node.__class__.__name__))
    stack.extend(
      [(child, level + 1) for child in reversed(node.Children.value)])


if __name__ == '__main__':
    start()
