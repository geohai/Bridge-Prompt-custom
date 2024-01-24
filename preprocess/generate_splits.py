import argparse
import yaml
import os
import numpy as np

if __name__ == "__main__":
    global args, best_prec1
    global global_step
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-cfg', default='./configs/egoexo/egoexo_ft.yaml')
    parser.add_argument('--log_time', default='')
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # Load the array of video names
    files = np.array(os.listdir(f"./data/{config['data']['dataset']}/frames/"))

    # Define the path to save the splits
    splits_dir = f"./data/{config['data']['dataset']}/splits"
    if not os.path.exists(splits_dir):
        os.makedirs(splits_dir)

    # Split the files into 5 equal-sized splits
    splits = np.array_split(files, 5)

    # Save the splits as the train splits
    for i, split in enumerate(splits):
        split_file_path = os.path.join(splits_dir, f'train.split{i+1}.bundle')

        with open(split_file_path, "w") as split_file:
            split_file.write("\n".join(split))

    # Now save test splits (all files not in the train split are in the corresponding test split)
    for i, split in enumerate(splits):
        test_split = files[~np.isin(files, split)]
        split_file_path = os.path.join(splits_dir, f'test.split{i+1}.bundle')
        with open(split_file_path, "w") as split_file:
            split_file.write("\n".join(test_split))

    print(f"Split {i+1} saved to {split_file_path}")
