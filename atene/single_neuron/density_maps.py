import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

import pandas as pd

import glob

import os

from vedo import *

from brainrender import Scene , actors, settings, actor, camera, cameras
from brainrender.actors import Neuron, Points, Point, PointsDensity

# in brainrender scene.py file set inset=False to remove little brain icon at the bottom of the scene
settings.CHECK_FOR_UPDATES = False
settings.SHOW_AXES = False
settings.SHADER_STYLE = "ambient"

# isocortical areas
cortical_areas = [
   "FRP", "MO1", "MO2/3", "MO5", "MO6a", "MO6b", "MOp", "MOs", "SS", "GU", "VISC", "AUD", 
    "VIS1", "VIS2/3", "VIS4", "VIS5", "VIS6a", "VIS6b", 
    "VISal", "VISam", "VISl1", "VISl2/3", "VISl4", "VISl5" , "VISl6",
    "VISp1", "VISp2/3", "VISp4", "VISp5", "VISp6",
    "VISpl", "VISpm", 
    "VISli", "VISpor", 
    "ACA", "PL", "ILA", "ORB", "AI", "RSP", "VISa1", "VISa2/3", "VISa4", "VISa5", "VISa6", 
    "VISrl", "TEa",
    "PERI", "ECT"
]



subcortical_areas = ["HPF", "CA1", "CA2", "CA3", "DG", "PAR", "POST", "PRE", "SUB",
                     "ACB", "FS", "OT" , "STR", "CP", "CLA", "EPv", "EPd", "LA", "BLA","BMA", "OLF"]




# lists of neurons in different categories:

# RSP and ORB projecting neurons (original grouping based on visual inspection)
rsp_orb = [
    "1056_1", "1056_11", "1056_15", "1056_2", "1056_24", "1056_25",
    "1056_27", "1056_29", "1056_3", "1056_36", "1056_4", "1056_41", "1056_5", "1056_6",
    "1057_13", "1057_16", "1057_2", "1135_14", "1135_16", "1135_5",
    "1807141_15", "1807141_7", "1814612_4", "1849931_10", "1849931_13", "1849931_14",
    "1849931_7", "1849931_9"
] + [
    "1849929_30",
    "1849929_7",
    "1849929_21",
    "1849929_5",
    "1849929_35",
    "1849929_28"
]
# RSP projecting neurons 
rsp = [
    "1135_13",
    "1135_7",
    "1135_9",
    "1849931_12",
    "1849931_4",
    "1849931_5",
    "1849931_6"
] + [
    "1849929_29",
    "1849929_34",
    "1849929_24",
    "1849929_33",
    "1849929_37",
    "1849929_20",
    "1849929_32",
    "1849929_22",
    "1849929_26",
    "1849929_31",
    "1849929_16"
]

# ORB projecting neurons
orb = [
    "1056_10", "1056_16", "1056_17", "1056_18", "1056_19", "1056_21", "1056_30", "1056_31",
    "1056_32", "1056_35", "1056_37", "1056_7", "1056_8", "1056_9", "1057_17", "1057_3",
    "1057_4", "1057_6", "1057_7", "1057_8", "1057_9", "1807141_14", "1807141_16", "1807141_17",
    "1807141_20", "1807141_25", "1807141_26", "1807141_31",  "1807141_36",
    "1807141_37", "1807141_38", "1807141_39", "1807141_8", "1814612_13", "1814612_14",
    "1814612_17", "1814612_22", "1814612_5", "1814612_6", "1814612_8", "1814612_9", "1814612_23"
]

# grouping based on endpoinbt count and axon length (no 29)
groupings = {
    "orb": [
        '1056_41_', '1056_31_', '1056_35_', '1056_32_', '1056_18_', '1056_21_', '1056_12_', '1056_16_',
        '1056_11_', '1056_8_', '1056_10_', '1056_9_', '1056_17_', '1056_13_', '1056_37_', '1056_19_',
        '1056_7_', '1056_30_', '1057_8_', '1057_6_', '1057_7_', '1057_3_', '1057_4_', '1057_9_', '1057_17_',
        '1807141_7_', '1807141_38_', '1807141_16_', '1807141_36_', '1807141_25_', '1807141_26_', '1807141_31_',
        '1807141_8_', '1807141_37_', '1807141_20_', '1807141_13_', '1807141_17_', '1807141_39_', '1807141_10_',
        '1807141_14_', '1814612_8_', '1814612_6_', '1814612_5_', '1814612_23_', '1814612_9_', '1814612_13_', '1814612_17_', '1814612_14_'
    ],
    "rsp_orb": [
        '1056_2_', '1056_6_', '1056_25_', '1056_1_', '1056_5_', '1056_15_', '1056_29_', '1056_24_', '1056_4_',
        '1056_3_', '1056_27_', '1057_16_', '1057_1_', '1057_2_', '1057_13_', '1807141_15_', '1814612_4_',
        '1849931_10_', '1849931_14_', '1849931_13_', '1135_16_', '1135_5_', '1135_14_'
    ],
    "rsp": [
        '1849931_12_', '1849931_4_', '1849931_9_', '1849931_6_', '1849931_5_', '1135_9_', '1135_7_'
    ]
}




# get all the neurite files with all neuron puncta coordinates
path = Path(__file__).parent
list_of_files_full = glob.glob(str(path) + '/ENT*/*neurites.xlsx') # all the forlders must start with ENT and then the brain ID


# need to make 12 different plots with these variables: sagittal2/top_side, endpoint/all axon, isocortical/all areas

def density_map (camera_angle, axon_part, areas, group):
    """
    The function to automaticaly generate 12 different plots for each condition
    camera_angle can be "sagittal2" or "top_side"
    axon_part can be "full_axon"  or "endpoints"
    areas can be "all_areas" or "isocortex"
    group can be "orb", "rsp", "rsp_orb"
    """
    settings.DEFAULT_CAMERA = camera_angle
    scene = Scene(title="", atlas_name='allen_mouse_25um', check_latest=False, screenshots_folder= "/Users/atenejonauskyte/EC_project_Image_analysis/single_neuron_data/density_maps")
    if axon_part == "full_axon":
        axon_ntype = [2,5,6]
    elif axon_part== "endpoints":
        axon_ntype = [6]
    list_of_files = [p for p in list_of_files_full if any(neuron in p for neuron in groupings[group])] # change the last varaible to which neurons should be included in plotting (e.g.orb, rsp, rsp_orb etc.)
    print((len(list_of_files) - len(groupings[group]))) # check if all neuron files are found (outcome should be 0)


    cortical_axon_coords =  [] # empty list to fill with coordinates
    for file in list_of_files:
        axon_points = pd.read_excel(file)
        print(file)
        axon_points_filtered = axon_points[axon_points['Ntype'].isin(axon_ntype)]
        
        
        if areas == "all_areas":
            axon_points_filtered = axon_points_filtered[~axon_points_filtered['Abbreviation'].astype(str).str.startswith("ENT")] 
        elif areas == "isocortex":
            axon_points_filtered = axon_points_filtered[axon_points_filtered['Abbreviation'].astype(str).str.startswith(tuple(cortical_areas))] 
        
        for index, row in axon_points_filtered.iterrows():
            x = row["x"] * 25
            y = row["y"] * 25
            z = row["z"] * 25
            coordinates = [x, y, z]
            cortical_axon_coords.append(coordinates)
        
    cortical_axon_coords_np = np.array(cortical_axon_coords) # to create a numpy array which is accepted to Points 
    #scene.add(Points(cortical_axon_coords_np, radius = 20)) # to add the points
    scene.add(PointsDensity(cortical_axon_coords_np, colors = "cividis"))

    name = group + " (" + areas + ", " + axon_part + ", " + camera_angle + ")"
    #scene.screenshot(name = name, zoom = 1.5, scale=2) # change name accordingly to what is being plotted
    scene.render()

    
density_map("sagittal2","full_axon","all_areas","orb") 
density_map("sagittal2","full_axon","all_areas","rsp")
density_map("sagittal2","full_axon","all_areas","rsp_orb")

density_map("top_side","full_axon","all_areas","orb") 
density_map("top_side","full_axon","all_areas","rsp")
density_map("top_side","full_axon","all_areas","rsp_orb")

density_map("sagittal2","endpoints","all_areas","orb")
density_map("sagittal2","endpoints","all_areas","orb")
density_map("sagittal2","endpoints","all_areas","orb")

density_map("top_side","endpoints","all_areas","orb") 
density_map("top_side","endpoints","all_areas","rsp")
density_map("top_side","endpoints","all_areas","rsp_orb")



density_map("sagittal2","full_axon","isocortex","orb") 
density_map("sagittal2","full_axon","isocortex","rsp")
density_map("sagittal2","full_axon","isocortex","rsp_orb")

density_map("top_side","full_axon","isocortex","orb") 
density_map("top_side","full_axon","isocortex","rsp")
density_map("top_side","full_axon","isocortex","rsp_orb")

density_map("sagittal2","endpoints","isocortex","orb")
density_map("sagittal2","endpoints","isocortex","orb")
density_map("sagittal2","endpoints","isocortex","orb")

density_map("top_side","endpoints","isocortex","orb") 
density_map("top_side","endpoints","isocortex","rsp")
density_map("top_side","endpoints","isocortex","rsp_orb")



##### testing the density plot function in vedo:


# create the point cloud
# pts = Points(cortical_axon_coords_np).color('k', 0.2)

# vol = pts.density(radius=300, compute_gradient=False).cmap('Dark2') # radius of local search can be specified (None=automatic)

# r = precision(vol.metadata['radius'], 2) # retrieve automatic/selected radius value
# vol.add_scalarbar3d(title=f'Density (counts in r_s ={r})', italic=1) # add the scale bar
# show(vol, __doc__, axes=False).close()


