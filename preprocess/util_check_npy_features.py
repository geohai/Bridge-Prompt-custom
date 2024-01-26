import numpy as np
import os
import json
import sys
from utils.errors import *
np.set_printoptions(threshold=sys.maxsize)
# Specify the file path

dataset = 'egoexo'
dataset = '50salads'

# # video_name = "fair_cooking_07_2" #"minnesota_cooking_030_2
# video_name = "rgb-01-2"
# path = f'/home/juro4948/gravit/Bridge-Prompt/data/{dataset}/features_dir/{dataset}_vit_features_splt1/'
# files = os.listdir(path)
# video_files = [f for f in files if video_name in f and f.endswith('.npy')]
# print('Number of npy files:', len(video_files))

# # Load the np file
# count_feats = 0
# for file_path in video_files:
#     data = np.load(os.path.join(path, file_path))

#     # Print the shape of the data
#     print("Shape:", data.shape)
#     count_feats += data.shape[0]

# # Load the JSON file
# json_file_path = f'/home/juro4948/gravit/Bridge-Prompt/preprocess/v_vlen_{dataset}.json'
# with open(json_file_path, 'r') as json_file:
#     json_data = json.load(json_file)

# # Print the loaded JSON data
# print(f'Num total: {count_feats}')
# print("vlen:", json_data[video_name])


## for split npy index files
# path = f'./data/{dataset}/splits/train_split1_nf16_ol[1]_ds[24].npy'
# path = 'data/egoexo/action_descriptions_id/30fps/iiith_cooking_08_1.npy'
path = 'data/50salads/splits/exfm_nf32.npy'
data = np.load(path, allow_pickle=True)
# Print the shape of the data
print(data)
print("Shape:", data.shape)


# # for reading labels
# print()
# selected_elements = data[768:1080 + 1]
# print(selected_elements)

# # Load the JSON file
# json_file_path = f'data/{dataset}/mapping_adj.json'
# with open(json_file_path, 'r') as json_file:
#     json_data = json.load(json_file)
# l = list(selected_elements)
# newl = [json_data[str(lab)] for lab in l]
# print(newl)

# for uniquel in set(newl):
#     print(uniquel, newl.count(uniquel))
    