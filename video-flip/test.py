import sys

import numpy as np


print("start python")
print(sys.argv)
print(sys.argv[-1])

import os
import ffmpeg

filePath= os.path.abspath("../camp.mp4")
videoNames= os.path.basename(filePath)
newVideoNames= videoNames.split('.')[0]+ "-flip2."+ videoNames.split('.')[-1]
outputPath= filePath.replace(videoNames,newVideoNames)

# 設定ffmpeg的路徑(環境變數)
os.environ['PATH'] += ';'+os.path.abspath(os.path.dirname(__file__)+'/static/ffmpeg/')


# ffmpeg.input(filePath).output(outputPath, **{'metadata:s:v:0': 'rotate=90'}).run()
ffmpeg.input(filePath).output(outputPath, **{'vf': 'transpose=1,transpose=1'}).run()
# ffmpeg.input(filePath).output(outputPath, **{'display_rotation': '90'}).run()






# os.system("pause")
