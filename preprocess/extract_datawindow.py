import numpy as np
import os

# TODO: fix this script

##### load config instead of manaully defining these
modes = ['train', 'test']
n_splits = [1, 2, 3, 4, 5]
num_frames = 16
overlap = [1] # overlap factor
dss = [24]
dataset = 'egoexo'
#####

"""
This script creates data windows from the videos and saves them in a numpy array.
The data windows are saved as a list of lists, where each sublist is of the form [video_name, start_idx, downsample_rate].  
Every single frame from the video is used as a starting point for a data window, and the number of frames saved is used to determine the video length and to create the windows.

If dss = 32 and num_frames=16, then the window length is 16*32 = 512 frames at the original dataset FPS, but the window is downsampled by 32. EgoExo is at 30FPS, so the window is 16*32/30 = 17.06 seconds long.
"""

root = f'./data/{dataset}/'
frame_dir = f'./data/{dataset}/frames/'
sub_dir = ''

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
            for dat in train_split:
                vpath = os.path.join(frame_dir, dat)
                # TODO: fix below line. This just takes the first camera returned by os.listdir. For now it works because I only downloaded the egocentric view.
                vlen = len([f for f in os.listdir(vpath + '/' + os.listdir(vpath)[0]) if os.path.isfile(os.path.join(vpath, os.listdir(vpath)[0], f))]) # number of files in the video frames directory is the length of the video
                # print(int(num_frames * overlap[i] * dss[i]))
                start_idxs = np.arange(0, vlen, int(num_frames * overlap[i] * dss[i])) # 16 * 1 * 48 = 768
                for idx in start_idxs:
                    new_train_list.append([dat, idx, dss[i]])
        np.save(f'./data/{dataset}/splits/'+mode+f'_split{n_split}_nf{num_frames}_ol{overlap}_ds{dss}.npy',
                np.array(new_train_list))
