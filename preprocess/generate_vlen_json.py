import os
import json

dataset = 'egoexo'
root = f'./data/{dataset}/'
frame_dir = f'./data/{dataset}/frames/'
sub_dir = ''

video_lengths = {}  # dictionary to store video_session and vlen

for video_session in os.listdir(frame_dir):
    vpath = os.path.join(frame_dir, video_session)
    cameras = os.listdir(vpath)

    # TODO: update. This is a hack to get the only camera view. Need to adapt for multiple camera views.
    ego = cameras[0]

    vlen = len(os.listdir(os.path.join(vpath, ego))) # number of files in the video frames directory is the length of the video

    video_lengths[video_session] = vlen  # TODO: def change this too

print(video_lengths)   

with open(f'./preprocess/v_vlen_{dataset}.json', 'w') as f: # TODO: may have to change filename to include the view
    json.dump(video_lengths, f)
    
