import os
import numpy as np
import matplotlib.pyplot as plt
import mpstool

NB_EXAMPLES=100

for folder in ["mps","real","gan"]:
    nb_file=0
    data = []
    for f in os.listdir(folder):
        nb_file+=1
        if nb_file==NB_EXAMPLES:
            break
        data.append(mpstool.img.Image.fromPng(os.path.join(folder,f)).asArray())
    data = np.array(data)
    print(folder, mpstool.stats.histogram(data))
