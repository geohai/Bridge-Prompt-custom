import numpy as np
import os
import glob
import pandas as pd
import json
## TO enable error messages ##
import sys
sys.path.append('utils/')
from errors import *
##############################

dataset = 'egoexo'
feat_name = 'egoexo_vit_features_splt1'

# dataset = '50salads'
# feat_name = '50salads_vit_features_splt1'

feat_root = './data/'+dataset+'/features_dir/'+feat_name
final_dir = 'combined_feat'
final_root = os.path.join(feat_root, final_dir)
feats = glob.glob(feat_root + '/*')
feats = [x for x in feats if x.endswith('.npy')]
if not os.path.exists(final_root):
    os.mkdir(final_root)

with open("./preprocess/v_vlen_" + dataset + ".json", 'r') as f:
    v_vlen = json.load(f)
df = pd.DataFrame(feats, columns=['paths'])
df['vid'] = [d.rsplit('/', 1)[1].rsplit('_', 1)[0] for d in df.paths]
df['ind'] = [d.rsplit('_', 1)[1][:-4] for d in df.paths]
df['ind'] = df['ind'].astype(int)

for name, group in df.groupby('vid'):
    group.sort_values('ind', inplace=True)
    print(group)
    vlen = v_vlen[name]
    print(f'VLEN: {vlen}')
    result = np.zeros((vlen, 768))
    for index, row in group.iterrows():
        # print(f'Second: {group.index[-1]}')
        if row.ind == 0:
            continue
        tfeat = np.load(row.paths)
        print(f'Path: {row.paths}, Shape: {tfeat.shape}')
        if index == group.index[-1]:
            diff = vlen - row.ind
            # print('Last window. I am removing this for now because there are actually no features here. This may causes problems when we have multiple window sizes rather than just 1. Take a look later if there is a bug.')
            # print(tfeat[:diff, :].shape)
            # print(result[row.ind:, :].shape)
            # print(row.ind)
            # result[row.ind:, :] = tfeat[:diff, :] # Julia commented this out
            
        else:
            result[row.ind:row.ind + 16, :] = tfeat  # 16 this should match num_frames
            # print(result[row.ind:row.ind + 16, :].shape)
    np.save(os.path.join(final_root, name + '.npy'), result)
    print(name + ' is combined.')

raise_error('FYI -- just raising this error so I know to come back to it. \n I am removing this for now because there are actually no features here. This is an issue where the dataset class ignores the last window if is a is smaller length than the num_frames. \
            This is proving to be an issue with EgoExo.\n This may causes problems when we have multiple window sizes rather than just 1. Take a look later if there is a bug.')