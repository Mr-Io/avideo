import os
import shutil

import cv2

# modifiable user parameters
file = "video.MOV"

delete_previous = True

min_t = None
max_t = None

# non user parameters

path_o = "out"
path_i = "in"


# delete previous output directory
if delete_previous:
    try:
        shutil.rmtree(path_o) #ignore_errors=True
    except FileNotFoundError as e:
        print("ERROR REMOVING '/OUT' DIRECTORY:", e)
os.makedirs("out", exist_ok=True)

# capture images
video = cv2.VideoCapture(os.path.join(path_i, file))
success, frame = video.read()
while(success):
    tframe = video.get(cv2.CAP_PROP_POS_MSEC)
    if ((not min_t) or tframe >= min_t) and  ((not max_t) or tframe <= max_t):
        cv2.imwrite(os.path.join(path_o, f"{file}_{tframe:.2f}.png"), frame)
    success, frame = video.read()

    
