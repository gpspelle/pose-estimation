import os

path = '/mnt/hotstorage/Data/FDD/'
f = os.listdir(path + "Falls")
nf = os.listdir(path + "NotFalls")

for i in f:
    os.system(" python3 run_video.py --path " + path + "Falls/" + i + "/" + " --video " + path + "Falls/" + i + "/" + i + ".avi")

for i in nf:
    os.system(' python3 run_video.py --path ' + path + 'NotFalls/' + i + '/' + ' --video ' + path + 'NotFalls/' + i + '/' + i + '.avi')
