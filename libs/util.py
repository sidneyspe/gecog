import sys
import os
import shutil
import cv2
import math
import numpy as np
import glob
import sys
import os
from matplotlib import pyplot as plt

COLORS = [(255,0,0),(0,255,0),(0,0,255)]


def makeFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def drawRectangle(img, rectangle):
    x, y, w, h = rectangle
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

def rectImg(img, rectangle):
    x, y, w, h = rectangle
    imgCopy = img.copy()
    imgOut = imgCopy[y:y+h, x:x+w]
    return imgOut

def checarVizinhos(ponto, ultimoValor):
    if ((ultimoValor != ponto and ultimoValor < ponto -3) or (ultimoValor != ponto and ultimoValor > ponto +3)):
        return True
    else:
        return False

def extractImgs(img, coord):
	entries = []
	for x in range(len(coord)):
	    imgX = rectImg(img, coord[x])
	    entries.append(imgX)
	return entries

def templateMatching (method, threshold, img, entries):
    img_rgb = img.copy()
    info = []
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_gray = cv2.equalizeHist(img_gray)
    # img_rgb = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    for x in range(len(entries)):
        template = cv2.cvtColor(entries[x], cv2.COLOR_BGR2GRAY)

        # template = cv2.equalizeHist(template)

        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, method)
        loc = np.where( res >= threshold)
        amountPoint = 0
        print "\nENTRY %s" % (x)
        lista = []
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), COLORS[x], 2)
            lista.append(pt)
            amountPoint +=1
        info.append((threshold,x,amountPoint)) # THRESHOLD, LABEL_INDICE, AMOUNT OF POINTS FIND

        # setLocX = set(loc[0])
        # setLocY = set(loc[1])
        #
        # # print "(%s,%s)" % (pt[0], pt[1]),
        # print sorted(setLocX)
        # print len(setLocX)
        # print sorted(setLocY)
        # print len(setLocY)

        # lista.sort(key=lambda tup: tup[1])  # sorts in place
        setLocX = set(lista)
        print sorted(setLocX)
        print len(setLocX)

    return img_rgb, info

def printResult (meth, output):
    print "USING %s METHOD \n" % (meth)
    for out in output:
    	print "THRESHOLD: %s\t" % (out[0][0])
    	for i in range(len(out)):
    		print "LABEL: %s\t AMOUNT: %s" % (str(out[i][1]), str(out[i][2]))
    	print "\n"

def printCSV (meth, output):
    print "\nUSING THRESHOLD 230 AND GLAUSSIAN BLUR (5,5)\t\t\t"
    print " \t0\t1\t2"
    for out in output:
        print "%s\t%s\t%s\t%s" % (str(out[0][0]),str(out[0][2]), str(out[1][2]), str(out[2][2]))
    print "\n"

def threshold(threshold, img):
    imgOut = img.copy()
    w, h = img.shape[::-1]

    for i in range(0, h):
        for j in range(0, w):
            if (imgOut[i][j] >= threshold): imgOut[i][j] = 255

    return imgOut
