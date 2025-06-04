from pathlib import Path

import pandas as pd

import glob

import os



def create_swc_file (axon_original):
    soma_axon = [1,2,5,6]
    neuron_soma_axon = axon_original[axon_original["Ntype"].isin(soma_axon)]
    neuron_soma_axon.loc[:, "Ntype"] = neuron_soma_axon["Ntype"].replace(5, 2)
    neuron_soma_axon.loc[:, "Ntype"] = neuron_soma_axon["Ntype"].replace(6, 2)
    neuron_soma_axon_final = neuron_soma_axon.iloc[:, [0, 1, 3, 4, 5, 6, 7]]
    return neuron_soma_axon_final

# need to extract neuron number from the file name:
def get_neuron_number(file_path):
    filename = os.path.basename(file_path)
    digits = ''.join(char for char in filename if char.isdigit())
    return digits



cortical_areas = [
   "FRP", "MO1", "MO2/3", "MO5", "MO6a", "MO6b", "MOp", "MOs", "SS", "GU", "VISC", "AUD", 
    "VIS1", "VIS2/3", "VIS4", "VIS5", "VIS6a", "VIS6b", 
    "VISal", "VISam", "VISl1", "VISl2/3", "VISl4", "VISl5" , "VISl6",
    "VISp1", "VISp2/3", "VISp4", "VISp5", "VISp6",
    "VISpl", "VISpm", 
    "VISli", "VISpor", 
    "ACA", "PL", "ILA", "ORB", "AI", "RSP", "VISa1", "VISa2/3", "VISa4", "VISa5", "VISa6", 
    "VISrl", "TEa",
    "PERI", "ECT", "ENT"
]
cortical_areas = set(cortical_areas)

soma_axon = [1,2,5,6]

# get a list of nlsx files
path = Path(__file__).parent
list_of_files = glob.glob(str(path) + '/ENT1056/*trans_new.xlsx') # all the forlders must start with ENT and then the brain ID
neurons =["26"]

list_of_files = [p for p in list_of_files if any(neuron in p for neuron in neurons)]
print(list_of_files)

for file in list_of_files:
    print(file)
    neuron_points = pd.read_excel(file)
    # remove dendrite points
    neuron_points = neuron_points[neuron_points["Ntype"].isin(soma_axon)]
    
    cortical_axons = pd.DataFrame(columns=neuron_points.columns)

    # first need to identify an endpoint
    neuron_points['Abbreviation'] = neuron_points['Abbreviation'].astype(str)
    for i in neuron_points.index:
        if neuron_points.loc[i,'Ntype'] == 6 and any(neuron_points.loc[i, 'Abbreviation'].startswith(area) for area in cortical_areas):
            # add the row to the cortical_axons dataframe
            cortical_axons.loc[len(cortical_axons)] = neuron_points.loc[i, : ]
            node_ID = neuron_points.loc[i,'Nparentid']
            axon_node = 2
            # we go to the parent of the node and check if it's Ntype 2 we keep going back untill we arrive at a branch point or Soma
            while axon_node == 2:
                # we find an index of the row that has node_ID in NO columns
                index = neuron_points[neuron_points['NO'] == node_ID].index
                # reasing the node_ID to its Nparentid
                node_ID = neuron_points.loc[index[0],'Nparentid']
                # add the row to the cortical_axons dataframe
                cortical_axons.loc[len(cortical_axons)] = neuron_points.loc[index[0], : ]
                # set axon_node to Ntype of the row
                axon_node = neuron_points.loc[index[0],'Ntype']




    # now that we have a list of points from endpoint to their branching point we need to fill in the rest of missing axons
    # to do that we need to go from the branching point up till the next branching point or soma (whichever comes first)

    added_nodes = set(cortical_axons["NO"])

    for i in cortical_axons.index:
        if cortical_axons.loc[i, 'Ntype'] == 5:  # If it's a branching point
            node_ID = cortical_axons.loc[i, 'Nparentid']
            axon_node = 5  # Assume it's still axon
            visited_nodes = set()  # Track visited nodes to prevent cycles

            while axon_node != 1:  # Stop when reaching soma
                # Find the index of the row where NO == node_ID
                index = neuron_points[neuron_points['NO'] == node_ID].index
                if index.empty:  # If no index is found, break to prevent infinite loops
                    print(f"Warning: Parent ID {node_ID} not found. Breaking loop.")
                    break

                if node_ID in visited_nodes:  # Prevent cyclic references
                    print(f"Warning: Detected cycle at node {node_ID}. Breaking loop.")
                    break

                visited_nodes.add(node_ID)  # Mark node as visited

                if node_ID not in added_nodes:  # Avoid adding duplicate nodes
                    cortical_axons.loc[len(cortical_axons)] = neuron_points.loc[index[0], :]
                    added_nodes.add(node_ID)

                # Move up to the parent
                node_ID = neuron_points.loc[index[0], 'Nparentid']
                axon_node = neuron_points.loc[index[0], 'Ntype']  # Update type to check if it's the soma

                if pd.isna(node_ID):  # If node_ID is missing, stop
                    print("Warning: Reached NaN parent ID. Breaking loop.")
                    break

    cortical_axons = cortical_axons.drop_duplicates(subset=['NO']) # remove duplicate nodes
    neuron_number = str(get_neuron_number(file)) # get the number of the neuron
    path_parts = file.split('/') # split the path into all its component and extract the folder
    folder = path_parts[-2]
    cortical_axons.to_csv(str(path) + "/" + str(folder) + "/" + str(neuron_number) + "_cortical_axon.csv")
    create_swc_file(cortical_axons).to_csv(str(path) + "/" + str(folder) + "/" + str(neuron_number) + "_cortical_axon.swc", sep=" ", index=False, header=False)





