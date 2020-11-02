'''
imports
'''
from pathlib import Path
from matplotlib import pyplot as plt
import os
import numpy as np
from tqdm import tqdm


'''
# used to generate the PosixPath variables for various common paths
# only works if the calling file exists in the root directory, that is, can access the folder data_project
'''
def data_paths():
    ROOT_DIR = Path('')

    PATH_DATA_PROJECT = ROOT_DIR/'data_project'

    PATH_TRAIN = PATH_DATA_PROJECT/'train'
    PATH_TEST = PATH_DATA_PROJECT/'test'

    PATH_TRAIN_IMG = PATH_TRAIN/'img'
    PATH_TRAIN_MASK = PATH_TRAIN/'mask'
    PATH_TEST_IMG = PATH_TEST/'img'
    PATH_TEST_MASK = PATH_TEST / 'mask'
    
    return PATH_TRAIN_IMG, PATH_TRAIN_MASK, PATH_TEST_IMG, PATH_TEST_MASK


'''
used to plot the image, and the mask side by side, and also the prediction, if any
index: int, img: np.ndarray, mask: np.ndarray, pred: np.ndarray
'''
def plot_img_mask(index, img, mask, pred=None):    
    if pred == None:
        fig, (ax1, ax2) = plt.subplots(1,2, figsize=(14,7))
        ax1.imshow(img)
        ax2.imshow(mask)
    else:
        fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(21,7))
        ax1.imshow(img)
        ax2.imshow(mask)
        ax3.imshow(pred)
    
    print("Index: {}".format(index))
    plt.show()


'''    
used to obtain all the filenames in a given directory as a list
path: PosixPath
'''
def get_fnames(path):
    fnames = next(os.walk(path))[2]
    fnames.sort()
    return fnames


'''
used to reconstruct a numpy array representation of an image from raveled .npy files
npy_path: PosixPath, img_height: int=224, img_width: int=224
'''
def rebuild_npy(npy_path, img_height=224, img_width=224):
    img_npy = np.load(npy_path)
    img_channel = int(len(img_npy)/img_height/img_width)
    
    # if img_channel == 1:
    #     return img_npy.reshape(img_height, img_width)
    # elif img_channel == 3:
    #     return img_npy.reshape(img_height, img_width, img_channel)
    # else:
    #     print("cannot rebuild numpy array")
    #     return
            
    return img_npy.reshape(img_height, img_width, img_channel)


'''
used to generate X_train, Y_train, X_test, Y_test as numpy arrays, from their .npy files
'''
def generate_train_test():
    paths = data_paths()
    data = [[], [], [], []]

    for index, path in tqdm(enumerate(paths), total=len(paths)):
        fnames = get_fnames(path)
        
        for fname in tqdm(fnames[:20], total=len(fnames[:20])):
            npy = rebuild_npy(path / fname)
            data[index].append(npy)

        data[index] = np.array(data[index])
    
    X_train, Y_train, X_test, Y_test = data[0], data[1], data[2], data[3]
    return (X_train, Y_train, X_test, Y_test)