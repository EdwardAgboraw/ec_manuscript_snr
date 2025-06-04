import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

import pandas as pd

import glob

import os

from vedo import Text3D

from brainrender import Scene , actors, settings, actor, camera, cameras
from brainrender.actors import Neuron, Points, Point

settings.CHECK_FOR_UPDATES = False
settings.SHADER_STYLE = "flat"



settings.SHADER_STYLE = "ambient"
settings.SHOW_AXES = False
settings.DEFAULT_CAMERA = "top"


# function extracted from Brainrender source code to plot the ID of the soma
def add_label(
    point_actor,
    cord,
    size=50,
    color=None
):
   
    cord[0], cord[2] = cord[2], cord[0]
    cord = cord * np.array([-1, -1, 1])
    
    new_actors = []
    color = point_actor.color
    label = point_actor.name
    txt = Text3D(
            label, cord, s=size, c="black", depth=0.1
            )
    new_actors.append(txt.rotate_x(180).rotate_y(180))

    return new_actors


# RSP and ORB projecting neurons from ORB injection group
rsp_orb_orb_inj = [
    "1807141_7",
    "1807141_15",
    "1056_15",
    "1056_4",
    "1056_41",
    "1057_16",
    "1056_11",
    "1056_27",
    "1056_2",
    "1056_25",
    "1056_29",
    "1057_2",
    "1056_1",
    "1056_6",
    "1056_3",
    "1056_5",
    "1057_13",
    "1056_24",
    "1056_36",
    "1056_26",
    "1056_22",
    "1056_34",
    "18146612_4"
]

# RSP and ORB projecting neurons from RSP injection group
rsp_orb_rsp_inj = [
    "1135_16",
    "1135_17",
    "1849931_7",
    "1849931_9",
    "1849931_10",
    "1849931_13",
    "1849931_14"
]

# RSP projecting neurons 
rsp = [
    "1135_7",
    "1135_9",
    "1135_13",
    "1849931_4",
    "1849931_5",
    "1849931_6",
    "1849931_12"
]

# ORB projecting neurons
orb = [
    "1057_4",
    "1056_18",
    "1057_6",
    "1056_7",
    "1056_31",
    "1056_35",
    "1057_8",
    "1057_7",
    "1057_3",
    "1057_17",
    "1056_9",
    "1056_32",
    "1056_21",
    "1056_16",
    "1056_10",
    "1056_17",
    "1057_9",
    "1056_19",
    "1056_8",
    "1056_30",
    "1056_37",
    "1807141_14",
    "1807141_25",
    "1807141_26",
    "1807141_38",
    "1807141_39",
    "1807141_20",
    "1807141_36",
    "1807141_37",
    "1807141_8",
    "1807141_32",
    "1807141_31",
    "1807141_17",
    "1807141_16",
    "18146612_5",
    "18146612_6",
    "18146612_8",
    "18146612_9",
    "18146612_13",
    "18146612_14",
    "18146612_17",
    "18146612_22"
]


# set the scene with allen mouse atlas
scene = Scene(title="", atlas_name='allen_mouse_25um', check_latest=False)

#get the file with all soma coordinates
soma_file = pd.read_csv("/Users/atenejonauskyte/EC_project_Image_analysis/single_neuron_data/all_soma_coordinates.csv")


# go over each of the neuron soma and extract the coordinates
for index, soma in soma_file.iterrows():

    x_soma = soma["x"]
    y_soma = soma["y"]
    z_soma = soma["z"]
    
    coordinates = [x_soma, y_soma, z_soma]

    soma_id = soma["ID"]

    # prol soma with colours based on the group the neuron belongs to
    if soma_id in rsp_orb_orb_inj:
        colour = "#E6C366"
        soma_plot = actors.Point(coordinates, color=colour, radius=30, name = soma_id[-6:-1])
        soma_number = add_label(point_actor = soma_plot, cord = coordinates)
        scene.add(soma_plot)
        #scene.add(*soma_number)

    if soma_id in rsp_orb_rsp_inj:
        colour = "#E6C366"
        soma_plot = actors.Point(coordinates, color=colour, radius=30, name = soma_id[-6:-1])
        soma_number = add_label(point_actor = soma_plot, cord = coordinates)
        scene.add(soma_plot)
        #scene.add(*soma_number)
     
       
    elif soma_id in orb:
        colour = "#EA4FA2"
        soma_plot = actors.Point(coordinates, color=colour, radius=30, name = soma_id[-6:-1])
        soma_number = add_label(point_actor = soma_plot, cord = coordinates)
        scene.add(soma_plot)
        #scene.add(*soma_number)
    
    elif soma_id in rsp:
        colour = "#49A2C9"
        soma_plot = actors.Point(coordinates, color=colour, radius=30, name = soma_id[-6:-1])
        soma_number = add_label(point_actor = soma_plot, cord = coordinates)
        scene.add(soma_plot)
        #scene.add(*soma_number)
        
    

    

# add entorhinal cortex, medial and lateral
#scene.add_brain_region("ENT",  alpha=0.09, color="grey")
scene.render()
