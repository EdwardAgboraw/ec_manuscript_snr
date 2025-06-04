from pathlib import Path

import pandas as pd

import glob

import os


from brainrender import Scene , actors, settings, actor, camera, cameras
from brainrender.actors import Neuron, Points, Point


settings.SHADER_STYLE = "ambient"
settings.SHOW_AXES = False
settings.DEFAULT_CAMERA = "top_side"

path = Path(__file__).parent
scene = Scene(title="", atlas_name='allen_mouse_25um', screenshots_folder=path)

mouseID = "1814612"
neuronNR = "23"
neuron_file_path = "/Users/atenejonauskyte/EC_project_Image_analysis/single_neuron_data/ENT" + mouseID + "/" + mouseID + "_" + neuronNR + ".swc"
neuron = Neuron(neuron_file_path, neurite_radius=0.5, soma_radius = 1, invert_dims=False, color="black", alpha=1)
neuron.scale([25,25,25])
scene.add(neuron)



scene.add_brain_region("ORBvl",  color="red", alpha = 0.2)
scene.add_brain_region("ORBm",  color="blue", alpha = 0.2)
scene.add_brain_region("ORBl",  color="pink", alpha = 0.2)
scene.add_brain_region("RSP" , color="purple", alpha = 0.2)
scene.add_brain_region("AON", color="yellow", alpha = 0.2)
scene.add_brain_region("MO", color="black", alpha = 0.2)
scene.add_brain_region("VIS", alpha = 0.2)
#scene.add_brain_region("SS", color="orange", alpha = 0.2)

scene.render()
