# How to adjust to custom dataset

## Project

[Provide a brief description of the project]

## Table of Contents

- [Instructions](#instructions)
- [Configuration](#configuration)
- [Parameters](#parameters)
- [Complex Variables](#complex-variables)
- [Contributing](#contributing)
- [License](#license)

## Instructions
NOTE: These work for when there is 1 view in each video folder. TODO: adapt the code to multiple views and handling that. 
#### Preprocessing
1. Place dataset into data folder. See 50salads folder for contents and organization.
2. Define dataset class in datasets.py. (This is done for EgoExo.)
3. Create config files in configs folder. (This is done for EgoExo.)
4. Create splits. Run preprocess/generate_splits.py 
5. The dataset needs a vlen file, placed in preprocess/. This is a json that contains the number of frames corresponding to each video sample, formatted like; {"rgb-06-1": 9701, "rgb-06-2": 8236}. Create vlen file: run preprocess/generate_vlen_json.py. Make sure to update the parameters in the script.
6. Run preprocess/extract_datawindow.py which saves the windows that the dataloader samples from for training/testing. Run this for each split (modify the split parameters inn the script. TODO: read in <dataset>_exfm.yaml to change the splits.)
#### Train model
7. Train the model on each split using the following (this takes about 2-2.5 hours for each split when using 2 NVIDIA RTX A6000 (each with 50 GB RAM)): 
    - bash scripts/run_train.sh ./configs/egoexo/egoexo_ft.yaml

#### Extract features with the trained model
8. Extract features from splits. -> Run python extract_frame_features.py --config ./configs/(dataset_name)/(dataset_name)_exfm.yaml --dataset (dataset_name)
9. Next, combine features for each video with `python preprocess/combine_features.py`. Run for each split by modifying the feat_name variable in this file. Output features are saved in data/<dataset_name>/features_dir/<dataset_name>_vit_features_splt<i>/combined_feat/
    -    At this stage we have trained BrP on each train split of the dataset and extracted features from each corresponding test split.

#### Evaluate on same dataset (still figuring this out)
--Note: It appears that their evaluation code is for ordinal action recognition for the gtea dataset, so we have to write our code in order to actually do this.--
BrP is not meant as a backbone action segmentation model, but if we want to see its performance, this is how:
10. Create a <dataset_name>_test.yaml config file if there is not one already.
11. Run `bash scripts/run_test.sh ./configs/<dataset_name>/<dataset_name>_test.yaml``

## To use with GraViT we need to move the splits over
1. Make a dataset dir in GraViT/data/annotations/<dataset_name>
2. 


## Configuration

[Explain any configuration steps required for the project]

## Parameters

### Description
There are certain key parameters for training Bridge-Prompt properly on a dataset. These parameters are mostly in the configs/<dataset-name>/ directories. 
TODO: We are working on migrating all these parameters to the config files because some of them are hard-coded (extract_datawindow.py, text_prompt.py).

### Key Parameters and Notes
- num_frames: The window size (num_frames interacts with downsampled frame rate).
- ol: overlap rate. This is the overlap rate between every two neighboring windows. The more overlap, the more windows that are generated. If ol=2, then the last 2 frames of the previous window are included in the next window (before downsampling).
- ds: downsampling rate. I believe that this is the rate that the each window is downsampled from the original fps. For example, if ds=2, then every 2nd frame is sampled while others are dropped. A smaller ds value gives finer temporal granularity but larger runtime. Heuristically selected according to the dataset characteristics. Long windows will have less information about each action, while short windows will not contain enough actions. The authors mixed long and short windows (for GTEA), and we could look into this.
- Note that ol and ds are lists and must be the same length. If multiple elements are in the lists, this means that windows of different sizes and overlaps were created.
- Note: if num_frames is set to 16 and dss is set to 48, it means that every data window will contain 16 frames, but those 16 frames will be selected with a spacing of 48 frames between each frame. In other words, it's 16 frames after downsampling every 48 frames of the original video.
- max_act: Cap the maximum number of actions within each window (defined by num_frames). If this is exceeded, an error will occur.

- The maximum number of words in a prompt is 77. This is capped by the backbone CLIP model. 

## My modifications
This is not comprehensive but just a way for me to keep track of major changes to the original BrP code.
- 1/25/2024: I realized that even though my clips at the moment are 10 seconds long, some of them appear to contain 10+ actions. This is very weird in theory. Upon inspection, I think we need to remove 'none' as an action. Pasting an example below:
['none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'Get cucumber', 'none', 'none', 'none', 'none', 'none', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'Get onions', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'Get tomato', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'Wash cucumber', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'Wash onions', 'none', 'Wash tomato']

Wash cucumber 48
Wash onions 19
Get cucumber 28
Wash tomato 1
Get tomato 66
Get onions 25
none 126

### Modify Parameters
To adjust the parameters of the project, follow these steps:

1. Open the `<dataset-name>_ft.yml` file located in the `configs/<dataset-name>/` directory. This is the config file for preprocessing and training parameters.
2. Locate the section titled "Parameters".
3. Modify the values of the parameters according to your requirements.
4. Save the file.

### Common Errors
- RuntimeError(f"Input {texts[i]} is too long for context length {context_length}"). This means that the windows are likely too long. Longer windows means that there are more actions in these windows, which require longer textual descriptions. CLIP can handle a max of 77 words. Perhaps aim for no more than 6/7/8 actions per window. 


## Contributing

1. EgoExo is different from the existing datasets because there are multiple views. The work I have done on this repo is to adapt it to the egocentric view (1 view per video name). How to handle multiple views? I think we need to change the data save structure from this: data/egoexo/frames/<video-name>/<view-name>/img_<i>.jpg to this: data/egoexo/frames/<view-name>/<video-name>/img_<i>.jpg
2. Modify preprocess/extract_datawindow.py to read config file and remove manual parameters.

## License

[Specify the project's license]
