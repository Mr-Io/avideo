import os
import shutil
import subprocess


from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import cv2

# USER PARAMETERS
delete_previous = True
audio_analysis = True
video_analysis = True
file = "sprint_30m.MOV"

# video
min_t = 9e3
max_t = 11e3

# audio
min_s = 4400
max_s = 5000

# NON USER PARAMETERS
path_o = "out"
path_i = "in"
audio_path = os.path.join(path_o, f"{file}_audio.wav")

# audio
AMP_MIN = -32768
AMP_MAX = 32767
AMP_DET = 10000


# delete previous output directory
if delete_previous:
    try:
        shutil.rmtree(path_o) #ignore_errors=True
    except FileNotFoundError as e:
        print("ERROR REMOVING '/OUT' DIRECTORY:", e)
os.makedirs("out", exist_ok=True)

# VIDEO ANALYSIS
if video_analysis:
    video = cv2.VideoCapture(os.path.join(path_i, file))
    success, frame = video.read()
    framerate = video.get(cv2.CAP_PROP_FPS)
    while(success and max_t > min_t):
        tframe = video.get(cv2.CAP_PROP_POS_MSEC)
        if ((not min_t) or tframe >= min_t) and  ((not max_t) or tframe <= max_t):
            cv2.imwrite(os.path.join(path_o, f"{file}-{framerate}fps_{tframe:.1f}.png"), frame)
        success, frame = video.read()

# AUDIO ANALYSIS
if audio_analysis:
    # extract audio file from video file
    command = f"{os.path.join("ffmpeg", "bin", "ffmpeg.exe")} -i {os.path.join(path_i, file)} -ac 1 -vn {audio_path}"
    subprocess.run(command, shell=True)

    # read audio file
    samplerate, data = wavfile.read(audio_path)
    tms = np.arange(len(data)) / (samplerate/1000)

    # detect first point of amplitude > 10000
    i = np.argmax(abs(data[min_s*(samplerate//1000): max_s*(samplerate//1000)]) > AMP_DET) + min_s*(samplerate//1000)
    ti = tms[i]

    # plot audio file
    fig, ax = plt.subplots(nrows=2, figsize=(12, 6))
    ax[0].plot(tms, data)
    ax[1].plot(tms, data)
    ax[0].vlines(min_s, AMP_MIN, AMP_MAX, colors="k")
    ax[0].vlines(max_s, AMP_MIN, AMP_MAX, colors="k")
    ax[1].set_xlim(min_s, max_s)
    ax[1].vlines(ti, AMP_MIN, AMP_MAX, colors="k")

    ax[0].set_title(f"{ti}")

    plt.show()

