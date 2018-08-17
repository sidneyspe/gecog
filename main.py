import sys
import os
sys.path.append(os.path.abspath("libs/"))
from util import *

IMAGE_NAME = "entry/bigImage.jpg"
# COORD = [(345,245,20,20),(377,245,20,20),(407,245,20,20)] # Small Image
COORD = [(683,485,50,50),(749,485,50,50),(811,485,50,50)] # Big Image
METHODS = ['cv2.TM_CCOEFF_NORMED']
THRESHOLDS = [0.97]
RESULT_FOLDER = "RESULT/"

img = cv2.imread(IMAGE_NAME, 1)

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

printHistogram(img_gray)


#
# img_gray = threshold(230, img_gray )
# img = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
# img = cv2.GaussianBlur(img,(5,5),0)
#
# entries = extractImgs(img, COORD)
# output = []
#
# for meth in METHODS:
# 	makeFolder(RESULT_FOLDER + meth)
# 	for threshold in THRESHOLDS:
# 		method = eval(meth)
# 		out, info = templateMatching (method, threshold, img, entries)
#
# 		FOLDER = RESULT_FOLDER + meth
# 		makeFolder(FOLDER)
#
# 		FILE = FOLDER + "/" + str(threshold) + '_output.png'
# 		cv2.imwrite(FILE, out)
#
# 		output.append(info)
#
# 	# print "------------------"
# 	printCSV(meth, output)
# 	# print "------------------"
