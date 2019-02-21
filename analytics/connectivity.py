import os
import numpy as np
import matplotlib.pyplot as plt
import mpstool
import sys

NB_EXAMPLES=100

try:
    FOLDER_NAME = sys.argv[1]
except:
    print("Correct usage : python3 connectivity.py <Balls|F42A|Sand_deposit|Channels>")

if FOLDER_NAME in {"Balls", "F42A"}:
    for folder in ["real","gan"]: #"mps"
        print("Computing stats for {} samples".format(folder))
        path = os.path.join(FOLDER_NAME,folder)
        nb_file = len(os.listdir(path))
        connectivity_X = {}
        connectivity_Y = {}
        connectivity_Z = {}
        for file in os.listdir(path):
            file_path = os.path.join(path,file)
            nb_file+=1
            image = mpstool.img.Image.fromVox(file_path)
            image.threshold(thresholds=[127],values=[0,255])
            connX = mpstool.connectivity.get_function(image, axis=0)
            connY = mpstool.connectivity.get_function(image, axis=1)
            connZ = mpstool.connectivity.get_function(image, axis=2)
            connectivity_X = { k: connectivity_X.get(k, 0) + connX.get(k, 0) for k in set(connX) }
            connectivity_Y = { k: connectivity_Y.get(k, 0) + connY.get(k, 0) for k in set(connY) }
            connectivity_Z = { k: connectivity_Z.get(k, 0) + connZ.get(k, 0) for k in set(connZ) }

        connectivity_X = {k: connectivity_X.get(k,0)/nb_file for k in connectivity_X.keys()}
        connectivity_Y = {k: connectivity_Y.get(k,0)/nb_file for k in connectivity_Y.keys()}
        connectivity_Z = {k: connectivity_Z.get(k,0)/nb_file for k in connectivity_Z.keys()}
        categories = mpstool.connectivity.get_categories(image)
        plt.plot(connectivity_X[0])
        plt.plot(connectivity_Y[0])
        plt.plot(connectivity_Z[0])

        plt.title(folder)
        plt.legend(["X", "Y", "Z"])
        plt.xlabel('distance (pixels)')
        plt.ylabel('connectivity along X axis')
        plt.show()


elif FOLDER_NAME=="Channels":
    pass

elif FOLDER_NAME=="Sand_deposit":
    pass
