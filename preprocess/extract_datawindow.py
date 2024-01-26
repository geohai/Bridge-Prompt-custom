import numpy as np
import os
import json
# TODO: fix this script

##### TODO: load config instead of manaully defining these
modes = ['train', 'test']
n_splits = [1, 2, 3, 4, 5]
num_frames = 16
overlap = [1] # overlap factor (proportion of overlap -> 0.5=50% overlap)
dss = [24]
dataset = 'egoexo'

# #####
# num_frames = 16
# overlap = [1, 1] # overlap factor (proportion of overlap -> 0.5=50% overlap)
# dss = [24, 32]
# dataset = '50salads'
# ####

"""
This script creates data windows from the videos and saves them in a numpy array.
The data windows are saved as a list of lists, where each sublist is of the form [video_name, start_idx, downsample_rate].  
Every single frame from the video is used as a starting point for a data window, and the number of frames saved is used to determine the video length and to create the windows.

If dss = 32 and num_frames=16, then the window length is 16*32 = 512 frames at the original dataset FPS, but the window is downsampled by 32. Ego (Aria) is at 30FPS, so the window is 16*32/30 = 17.06 seconds long.
"""

root = f'./data/{dataset}/'
frame_dir = f'./data/{dataset}/frames/'
path_to_vlen = f'./preprocess/v_vlen_{dataset}.json'
sub_dir = ''

with open(path_to_vlen, 'r') as json_file:
    vlen_mapping = json.load(json_file)

for n_split in n_splits:
    print(f'Split: {n_split}')
    for mode in modes:
        txt_path = 'splits/' + mode + '.split' + str(n_split) + '.bundle'
        train_split = []
        with open(os.path.join(root, txt_path), 'r') as f:
            for line in f.readlines():
                line = line.strip('\n')
                line = line.split('.')[0]
                train_split.append(line)
        new_train_list = []
        for i in range(len(dss)):
            print('Interval: ', int(num_frames * overlap[i] * dss[i]))
            for dat in train_split:
                vpath = os.path.join(frame_dir, dat)
                # TODO: fix below line. This just takes the first camera returned by os.listdir. For now it works because I only downloaded the egocentric view.
                if dataset == 'egoexo':
                    vlen = len([f for f in os.listdir(vpath + '/' + os.listdir(vpath)[0]) if os.path.isfile(os.path.join(vpath, os.listdir(vpath)[0], f))]) # number of files in the video frames directory is the length of the video
                    if vlen == 0:
                        continue
                else:
                    vlen = len([f for f in os.listdir(vpath) if os.path.isfile(os.path.join(vpath, f))])

                if vlen != vlen_mapping[dat] and dataset != '50salads':
                    print(f'Vlen does not match for {dat}.')
                    print(f'Number of frames in dir: {vlen}')
                    print(f'Number of frames in json: {vlen_mapping[dat]}')
                    raise ValueError
                
                # print(int(num_frames * overlap[i] * dss[i]))
                start_idxs = np.arange(0, vlen, int(num_frames * overlap[i] * dss[i])) # 16 * 1 * 24 = 768
                
                for idx in start_idxs:
                    new_train_list.append([dat, idx, dss[i]])

                print(f'Number of frames in dir: {vlen} | Last idx: {start_idxs[-1]} | Diff: {vlen - start_idxs[-1]}')
    
        np.save(f'./data/{dataset}/splits/'+mode+f'_split{n_split}_nf{num_frames}_ol{overlap}_ds{dss}.npy',
                np.array(new_train_list))
