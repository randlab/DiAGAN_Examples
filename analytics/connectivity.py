import os
import numpy as np
import matplotlib.pyplot as plt
import mpstool
import sys

NB_EXAMPLES=100

try:
    FOLDER_NAME = sys.argv[1]
except:
    print("Correct usage : python3 connectivity.py <Balls|F42A|Houthuys|Strebelle>")

for folder in ["mps","real","gan"]:
    nb_file=0
    connectivity_X = {}
    connectivity_Y = {}
    for file in os.listdir(folder):
        nb_file+=1
        print(nb_file)
        image = mpstool.img.Image.fromPng(os.path.join(folder,file))
        image.threshold(thresholds=[127],values=[0,255])
        connX = mpstool.connectivity.get_function(image, axis=1)
        connectivity_X = { k: connectivity_X.get(k, 0) + connX.get(k, 0) for k in set(connX) }
        connY = mpstool.connectivity.get_function(image, axis=0)
        connectivity_Y = { k: connectivity_Y.get(k, 0) + connY.get(k, 0) for k in set(connY) }
        if nb_file==NB_EXAMPLES:
            break
    connectivity_X = {k: connectivity_X.get(k,0)/nb_file for k in connectivity_X.keys()}
    connectivity_Y = {k: connectivity_Y.get(k,0)/nb_file for k in connectivity_Y.keys()}
    print(connectivity_X)
    categories = mpstool.connectivity.get_categories(image)
    for category in categories:
        plt.plot(connectivity_X[category])
    plt.title(folder)
    plt.legend(categories)
    plt.xlabel('distance (pixels)')
    plt.ylabel('connectivity along X axis')
    plt.show()

    categories = mpstool.connectivity.get_categories(image)
    for category in categories:
        plt.plot(connectivity_Y[category])
    plt.legend(categories)
    plt.xlabel('distance (pixels)')
    plt.ylabel('connectivity along Y axis')
    plt.show()
