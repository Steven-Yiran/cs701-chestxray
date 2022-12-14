"""
Split data into positive and negative classes
"""
import torchxrayvision as xrv
import os
import sys
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import pandas as pd


DATA_DIR_PATH = "/storage/yirans/chestxray/covid-chestxray-dataset"
DEFAULT_TARGET_PATH = "/storage/yirans/chestxray/training_data_dir"
IMG_EXT=".jpg"
COVID_LABEl_IDX = 3
IMG_DIM = 128


def load_dataset(dir_path):
    imgPath = os.path.join(dir_path, "images")
    csvPath = os.path.join(dir_path, "metadata.csv")
    dataset = xrv.datasets.COVID19_Dataset(imgpath=imgPath, csvpath=csvPath)
    return dataset

def show_sample(dataset):
    # dataloader example: https://colab.research.google.com/drive/1A-gIZ6Xp-eh2b4CGS6BHH7-OgZtyjeP2
    sample = dataset[0]
    print(pd.Series(dict(zip(dataset.pathologies, sample["lab"]))))
    plt.imsave("demo.png", sample["img"][0], cmap="gray")


def split_dataset(dir_path, dataset):
    positive_scan_paths, negative_scan_paths = [], []
    for i in range(len(dataset)):
        label = dataset[i]["lab"][COVID_LABEl_IDX]
        fpath = os.path.join(
            dir_path,
            dataset.csv.iloc[i]["folder"],
            dataset.csv.iloc[i]["filename"]
        )
        if int(label) == 1:
            positive_scan_paths.append(fpath)
        else:
            negative_scan_paths.append(fpath)
    return positive_scan_paths, negative_scan_paths


def read_img_file(path):
    """read as greyscale image"""
    im = Image.open(path).convert("L")
    return im


def process_scan(path):
    """Read and resize Image object"""
    image = read_img_file(path)
    image = image.resize((IMG_DIM, IMG_DIM))
    return image


def main():
    dataset = load_dataset(DATA_DIR_PATH)
    # show_sample(dataset)
    positive_scan_paths, negative_scan_paths = split_dataset(DATA_DIR_PATH, dataset)

    positive_scans = [process_scan(path) for path in positive_scan_paths]
    negative_scans = [process_scan(path) for path in negative_scan_paths]

    # store locally
    positive_dir = os.path.join(DEFAULT_TARGET_PATH, "CovidScanData/positive")
    negative_dir = os.path.join(DEFAULT_TARGET_PATH, "CovidScanData/negative")

    for i, im in enumerate(positive_scans):
        fpath = os.path.join(positive_dir, "pos_"+str(i).zfill(3)+IMG_EXT)
        im.save(fpath)
    for i, im in enumerate(negative_scans):
        fpath = os.path.join(negative_dir, "pos_"+str(i).zfill(3)+IMG_EXT)
        im.save(fpath)
    print(f"COVID samples: {len(positive_scan_paths)}, Non-COVID samples: {len(negative_scan_paths)}")
    print(f"Processed data stored at {DEFAULT_TARGET_PATH}")


if __name__ == "__main__":
    main()