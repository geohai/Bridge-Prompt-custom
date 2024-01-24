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
1. Place dataset into data folder
2. Define dataset class in datasets.py
3. Create config files in configs folder
4. Run preprocess/extract_dataawindow.py which saves the windows that the dataloader samples from for training/testing
5. 



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

### Modify Parameters
To adjust the parameters of the project, follow these steps:

1. Open the `<dataset-name>_ft.yml` file located in the `configs/<dataset-name>/` directory. This is the config file for preprocessing and training parameters.
2. Locate the section titled "Parameters".
3. Modify the values of the parameters according to your requirements.
4. Save the file.

### Common Errors
- RuntimeError(f"Input {texts[i]} is too long for context length {context_length}"). This means that the windows are likely too long. Longer windows means that there are more actions in these windows, which require longer textual descriptions. CLIP can handle a max of 77 words. Perhaps aim for no more than 6/7/8 actions per window. 
## Contributing

[Provide instructions on how to contribute to the project]

## License

[Specify the project's license]
