import os
import numpy as np
import matplotlib.pyplot as plt
import mpstool
import sys

try:
    TI_FOLDER = sys.argv[1]
except:
    print("Correct usage : `python3 histo_vario.py <TI_folder>`")


#Creates four polar axes, and accesses them through the returned array
fig, axes = plt.subplots(1, 4)

# Print the three histograms for mps, gan and real image
for i,folder in enumerate([os.path.join(TI_FOLDER,x) for x in ["real","mps","gan"]]):
    data = []
    title = "\n".join(folder.split("/"))
    for f in os.listdir(folder):
        if '.gslib' in f:
            img = mpstool.img.Image.fromGslib(os.path.join(folder,f))
        elif '.png' in f:
            img = mpstool.img.Image.fromPng(os.path.join(folder,f))
        elif '.vox' in f:
            img = mpstool.img.Image.fromVox(os.path.join(folder,f))
        else:
            raise Exception("Data file not recognized : {} . \
                            Only able to read png, vox and gslib \
                            file formats".format(f))
        img.normalize()
        data.append((img.asArray()+1)*0.5) # normalize in [0,1], not in [-1,1]

    data = np.array(data)
    histo = mpstool.stats.histogram(data)

    # aggregate values
    histo["other"]=0.
    for v in list(histo.keys()):
        if v not in [0., 1., "other"]:
            histo["other"]+=histo[v]
            del histo[v]
    print(folder, histo)

    axes[i].bar([0,1,2], [histo[0.], histo["other"], histo[1.]], tick_label=["0", "other", "1"])
    axes[i].set_title(title)
    axes[i].set_ylim([0,1])


# print the fourth histogram for thresholded Gan
data = []
title = " - ".join(folder.split("/"))+"\nthresholded"
for f in os.listdir(os.path.join(TI_FOLDER,"gan")):
    if '.gslib' in f:
        img = mpstool.img.Image.fromGslib(os.path.join(folder,f))
    elif '.png' in f:
        img = mpstool.img.Image.fromPng(os.path.join(folder,f))
    elif '.vox' in f:
        img = mpstool.img.Image.fromVox(os.path.join(folder,f))
    else:
        raise Exception("Data file not recognized : {} . \
                        Only able to read png, vox and gslib \
                        file formats".format(f))
    img.normalize()
    img.threshold([0],[0,1])
    data.append(img.asArray())

data = np.array(data)
histo = mpstool.stats.histogram(data)

# aggregate values
histo["other"]=0.
for v in list(histo.keys()):
    if v not in [0., 1., "other"]:
        histo["other"]+=histo[v]
        del histo[v]
print(title, histo)

axes[3].bar([0,1,2], [histo[0.], histo["other"], histo[1.]], tick_label=["0", "other", "1"])
axes[3].set_title(title)
axes[3].set_ylim([0,1])

plt.show()
