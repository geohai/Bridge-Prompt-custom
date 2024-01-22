import os
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', default='breakfast')
parser.add_argument('--vpath', default='./data/breakfast/breakfast_videos/')
parser.add_argument('--fpath', default='./data/breakfast/frames/')
args = parser.parse_args()

path = args.vpath
output = args.fpath

file_suffix = ['*.mp4', '*.avi', '*.webm']
files = []

fps = '15'
if args.dataset == '50salads':
    fps = '30'

print(path)

for s in file_suffix:
    files.extend(glob.glob(os.path.join(path, '**', s), recursive=True))
print(files)
files_prefix = os.path.commonprefix(files)
files_prefix = files_prefix.rsplit('/', 1)[0]
file_names = [os.path.relpath(f, path) for f in files]

print(file_names)
for video in file_names:
    if not os.path.exists(os.path.join(output, video).rsplit('.', 1)[0]):
        os.makedirs(os.path.join(output, video).rsplit('.', 1)[0], exist_ok=True)
        cmd = "ffmpeg -i " + os.path.join(path, video) + " -vsync vfr -r " + fps + " " +\
              os.path.join(output, video).rsplit('.', 1)[0] + "/img_%05d.jpg"
        print(cmd)
        os.system(cmd)
