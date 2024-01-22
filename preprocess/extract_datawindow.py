import numpy as np
import os

# TODO: fix this script

##### load config instead of manaully defining these
modes = ['train', 'test']
n_split = 1
num_frames = 16
overlap = [1]
dss = [48]
dataset = 'egoexo'
#####

"""
This script creates data windows from the videos and saves them in a numpy array.
"""

root = f'./data/{dataset}/'
frame_dir = f'./data/{dataset}/frames/'
sub_dir = ''

for mode in modes:
    if dataset == 'egoexo':
        txt_path = f'splits/split{n_split}.txt'
    else:
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
            print(vpath)
            print(os.listdir(vpath))
            print(vlen)
            # print(int(num_frames * overlap[i] * dss[i]))
            start_idxs = np.arange(0, vlen, int(num_frames * overlap[i] * dss[i]))
            for idx in start_idxs:
                new_train_list.append([dat, idx, dss[i]])
    np.save(f'./data/{dataset}/splits/'+mode+f'_split{n_split}_nf{num_frames}_ol{overlap}_ds{dss}.npy',
            np.array(new_train_list))
