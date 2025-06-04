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
settings.DEFAULT_CAMERA = "sagittal2" # "sagittal2" for side view and "top_side" for top view

scene = Scene(title="", atlas_name='allen_mouse_25um', check_latest=False, screenshots_folder= "/Users/atenejonauskyte/EC_project_Image_analysis/single_neuron_data/density_maps")


# need to get only the axon puncta in cortical areas

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


all_areas = cortical_areas + subcortical_areas

# now actually filter the files to only have puncta for these regions

axon_ntype = soma_axon = [2,5,6] # axon Ntypes that will be used to filer the dataset to axon points only (2,5,6) for full axon, 6 for axon endpoints only

cortical_axon_coords =  [] # empty list to fill with coordinates



# get a list of nlsx files
path = Path(__file__).parent
list_of_files_full = glob.glob(str(path) + '/ENT*/*neurites.xlsx') # all the forlders must start with ENT and then the brain ID

# lists of neurons in different categories:

#### groupings based on original grouping (endpoints + visual inspection)
rsp = [
    "1135_13_", 
    "1135_7_", 
    "1135_9_", 
    "1849931_12_", 
    "1849931_4_", 
    "1849931_5_", 
    "1849931_6_"
]

orb = [
    "1056_10_", "1056_16_", "1056_17_", "1056_18_", "1056_19_", "1056_21_", "1056_30_",
    "1056_31_", "1056_32_", "1056_35_", "1056_37_", "1056_7_", "1056_8_", "1056_9_",
    "1057_17_", "1057_3_", "1057_4_", "1057_6_", "1057_7_", "1057_8_", "1057_9_",
    "1807141_14_", "1807141_16_", "1807141_17_", "1807141_20_", "1807141_25_", "1807141_26_",
    "1807141_31_", "1807141_32_", "1807141_36_", "1807141_37_", "1807141_38_", "1807141_39_",
    "1807141_8_", "1814612_13_", "1814612_14_", "1814612_17_", "1814612_22_",
    "1814612_5_", "1814612_6_", "1814612_8_", "1814612_9_", "1814612_23_"
]

rsp_orb = [
    "1056_1_", "1056_11_", "1056_15_", "1056_2_", "1056_24_", "1056_25_",
    "1056_27_", "1056_29_", "1056_3_", "1056_36_", "1056_4_", "1056_41_", "1056_5_", "1056_6_",
    "1057_13_", "1057_16_", "1057_2_", "1135_14_", "1135_16_", "1135_17_", "1135_5_",
    "1807141_15_", "1807141_7_", "1814612_4_", "1849931_10_", "1849931_13_", "1849931_14_",
    "1849931_7_", "1849931_9_"
]




##### groupings based on length and endpoint filtering


rsp_new = [
    "1135_7_",
    "1135_9_",
    "1849931_12_",
    "1849931_4_",
    "1849931_5_",
    "1849931_6_",
    "1849931_9_"
]

rsp_orb_new = [
    "1057_16_", "1135_14_", "1135_16_", "1849931_10_", "1849931_13_", "1849931_14_",
    "1056_15_", "1056_12_", "1056_13_", "1057_13_", "1056_29_", "1056_6_", "1056_1_",
    "1056_2_", "1056_24_", "1056_25_", "1056_26_", "1056_27_", "1056_3_", "1056_36_",
    "1056_5_", "1807141_15_", "1807141_7_", "1057_1_", "1057_2_", "1814612_4_",
    "1056_4_", "1135_5_"
]

orb_new = [
    "1056_30_", "1056_35_", "1056_8_", "1056_11_", "1056_41_", "1056_19_", "1056_21_", "1056_7_",
    "1057_6_", "1057_7_", "1057_17_", "1056_16_", "1056_17_", "1056_18_", "1056_32_", "1056_10_",
    "1056_31_", "1056_37_", "1056_9_", "1057_8_", "1057_9_", "1807141_14_", "1807141_16_",
    "1807141_17_", "1807141_20_", "1807141_25_", "1807141_26_", "1807141_31_", "1807141_36_",
    "1807141_37_", "1807141_38_", "1807141_39_", "1807141_8_", "1814612_17_", "1814612_22_",
    "1814612_5_", "1814612_6_", "1814612_8_", "1814612_9_", "1814612_23_", "1807141_13_",
    "1057_4_", "1057_3_", "1807141_32_", "1814612_13_", "1814612_14_", "1807141_10_"
]



##### groupings based on soma locaition in EC

mmec = [
    "1135_5_",
    "1135_7_",
    "1135_9_",
    "1849931_12_",
    "1849931_4_",
    "1849931_5_",
    "1849931_9_"
]
llec = [
    "1056_32_", "1056_10_", "1056_31_", "1056_37_", "1056_9_", "1057_8_", "1057_9_",
    "1807141_14_", "1807141_16_", "1807141_17_", "1807141_20_", "1807141_25_", "1807141_26_",
    "1807141_31_", "1807141_36_", "1807141_37_", "1807141_38_", "1807141_39_", "1807141_8_",
    "1814612_17_", "1814612_22_", "1814612_5_", "1814612_6_", "1814612_8_", "1814612_9_",
    "1814612_23_", "1807141_13_", "1807141_15_", "1807141_7_", "1057_1_"
]
intec = [
    "1056_30_", "1056_35_", "1056_8_", "1056_11_", "1056_41_", "1056_15_", "1056_12_", "1056_13_",
    "1056_19_", "1056_21_", "1056_7_", "1057_6_", "1057_7_", "1057_13_", "1849931_6_", 
    "1057_17_", "1056_29_", "1056_6_", "1057_16_", "1135_14_", "1135_16_", "1849931_10_", 
    "1849931_13_", "1849931_14_", "1056_1_", "1056_2_", "1056_24_", "1056_25_", "1056_26_", 
    "1056_27_", "1056_3_", "1056_36_", "1056_5_"
]


list_of_files = [p for p in list_of_files_full if any(neuron in p for neuron in rsp)] # change the last varaible to which neurons should be included in plotting (e.g.orb, rsp, rsp_orb etc.)

print((len(list_of_files) - len(orb))) # check if all neuron files are found (outcome should be 0)


for file in list_of_files:
    axon_points = pd.read_excel(file)
    axon_points_filtered = axon_points[axon_points['Ntype'].isin(axon_ntype)]
    #axon_points_filtered = axon_points_filtered[axon_points_filtered['Abbreviation'].astype(str).str.startswith(tuple(cortical_areas))] # select subcortical_areas or cortical_areas
    axon_points_filtered = axon_points_filtered[~axon_points_filtered['Abbreviation'].astype(str).str.startswith("ENT")] # select subcortical_areas or cortical_areas
    for index, row in axon_points_filtered.iterrows():
        x = row["x"] * 25
        y = row["y"] * 25
        z = row["z"] * 25
        coordinates = [x, y, z]
        cortical_axon_coords.append(coordinates)
    

cortical_axon_coords_np = np.array(cortical_axon_coords) # to create a numpy array which is accepted to Points 
#scene.add(Points(cortical_axon_coords_np, radius = 20)) # to add the points
scene.add(PointsDensity(cortical_axon_coords_np))


# hip = scene.add_brain_region("HIP",silhouette=True, alpha = 0.1)
# par = scene.add_brain_region( "PAR", silhouette=True, alpha = 0.1)
# post = scene.add_brain_region( "POST", silhouette=True, alpha = 0.1)
# pre = scene.add_brain_region( "PRE", silhouette=True, alpha = 0.1)
# sub = scene.add_brain_region("SUB", silhouette=True, alpha = 0.1)
# strd = scene.add_brain_region(  "STRd", silhouette=True, alpha = 0.1)
# strv =  scene.add_brain_region( "STRv",silhouette=True, alpha = 0.1)
# ctxsp = scene.add_brain_region( "CTXsp", silhouette=True, alpha = 0.1)
# scene.add_label(hip, "HIP") # adding brain region names
# scene.add_label(par, "PAR")
# scene.add_label(post, "POST")
# scene.add_label(pre, "PRE")
# scene.add_label(sub, "SUB")
# scene.add_label(strv, "STRd")
# scene.add_label(strd, "STRv")
# scene.add_label(ctxsp, "CTXsp")




scene.screenshot(name = "RSP (original, side, all, automatic radius)", zoom = 1.5, scale=2) # change name accordingly to what is being plotted

#scene.render()


##### testing the density plot function in vedo:


# create the point cloud
# pts = Points(cortical_axon_coords_np).color('k', 0.2)

# vol = pts.density(radius=300, compute_gradient=False).cmap('Dark2') # radius of local search can be specified (None=automatic)

# r = precision(vol.metadata['radius'], 2) # retrieve automatic/selected radius value
# vol.add_scalarbar3d(title=f'Density (counts in r_s ={r})', italic=1)
# show(vol, __doc__, axes=False).close()


#### check this out https://github.com/brainglobe/brainglobe-heatmap?tab=readme-ov-file
#⬇︎
#⬇︎
#⬇︎
#⬇︎ 
############### different kind of density maps ####################


# import brainglobe_heatmap as bgh

# area_values_orb = dict(
#   ACA = 2826.96745,
#   AI = 9989.305797,
#   #AMY = 20764.34475,
#   AUD = 2300.958927,
#   CLA = 2615.888561,
#   ECT = 5952.059023,
#   EP = 10841.61159,
#   FRP = 258.0150637,
#   GU = 1005.009709,
#   HIP = 3939.924995,
#   ILA = 2941.677966,
#   MO = 1633.76461,
#   OLF = 3814.276984,
#   ORB = 9257.486708,
#   PAR = 515.5617259,
#   PERI = 2888.865582,
#   PL = 3940.207054,
#   POST = 0,
#   PRE = 68.58961737,
#   PTLp = 26.58756421,
#   RSP = 0,
#   SS = 4018.43073,
#   STRd = 24697.26266,
#   STRv = 33163.14723,
#   SUB = 1681.196536,
#   TEa = 4225.972222,
#   VIS = 827.1315014+2406.358407,
#   VISC = 2422.073186
# )

# area_values_rsp = dict(
#   ACA = 7824.334986,
#   AI = 2396.182561,
#   #AMY = 1407.874907,
#   AUD = 7019.400787,
#   CLA = 67.50218619,
#   ECT = 2806.062647,
#   EP = 1287.162185,
#   FRP = 27.75543488,
#   GU = 0,
#   HIP = 3718.802645,
#   ILA = 172.3208794,
#   MO = 4905.631097,
#   OLF = 374.7361517,
#   ORB = 0,
#   PAR = 483.5625497,
#   PERI = 265.0186689,
#   PL = 1137.523262,
#   POST = 1281.060541,
#   PRE = 190.9135796,
#   PTLp = 2451.828628,
#   RSP = 15578.71481,
#   SS = 6521.487676,
#   STRd = 6790.735076,
#   STRv = 675.3244899,
#   SUB = 2930.626752,
#   TEa = 5071.104785,
#   VIS = 37518.25646 + 4658.592058,  # Summed VIS and VISpor
#   VISC = 1006.170871
# )

# area_values_orb_rsp = dict(
#   ACA = 10719.57815,
#   AI = 8386.797799,
#   #AMY = 11005.26309,
#   AUD = 3634.918118,
#   CLA = 1945.152601,
#   ECT = 3949.915468,
#   EP = 5117.222335,
#   FRP = 242.0034752,
#   GU = 506.7360204,
#   HIP = 4244.455584,
#   ILA = 1908.016318,
#   MO = 8931.012748,
#   OLF = 4901.731879,
#   ORB = 10320.45141,
#   PAR = 1268.705616,
#   PERI = 2326.228887,
#   PL = 2713.272594,
#   POST = 1654.955178,
#   PRE = 182.9121352,
#   PTLp = 1306.648093,
#   RSP = 17826.20954,
#   SS = 5812.334175,
#   STRd = 24484.8361,
#   STRv = 24825.58138,
#   SUB = 3604.461928,
#   TEa = 4897.900467,
#   VIS = 10782.36527 + 3133.169703,
#   VISC = 1637.343889
# )

# f = bgh.Heatmap(
#     area_values_rsp,
#     position=4000,
#     orientation="horizontal",
#     vmin=-0,
#     vmax=37519,
#     annotate_regions=False,
#     cmap = "YlGnBu",
#     format="2D",
# ).show()

# f = bgh.Heatmap(
#     area_values_rsp,
#     position=5000,
#     orientation="frontal",
#     vmin=-0,
#     vmax=37519,
#     annotate_regions=False,
#     cmap = "YlGnBu",
#     format="2D",
# ).show()

# planner = bgh.plan(
#     area_values_rsp,
#     position=5000,
#     orientation="frontal",  # orientation, or 'sagittal', or 'horizontal' or a tuple (x,y,z)
# ).show()
