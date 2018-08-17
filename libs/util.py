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
from math import *

COLORS = [(255,0,0),(0,255,0),(0,0,255)]

def distance (x1, y1, x2, y2):
    return sqrt( (x2 - x1)**2 + (y2 - y1)**2 )

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
    img2 = img.copy()
    info = []
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    allPoints = []
    for x in range(len(entries)):
        template = cv2.cvtColor(entries[x], cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, method)
        loc = np.where( res >= threshold)
        print "\nENTRY %s" % (x)
        points = []
        amoutOfRemovedPoints = 0 ## cont of points removed
        newPoints = []
        pts = zip(*loc[::-1]) ##concat points
        pts = sorted(pts, key=lambda x: x[0]) ## sort the points of x
        for i in range(0, len(pts) -1):
            dist = floor(distance(pts[i][1],pts[i][0],pts[i+1][1],pts[i+1][0]))
            if ( dist > 100): ## condition to point is separeted of other point
                points.append(pts[i])
            else:
                amoutOfRemovedPoints +=1 ## increment cont of points removed

        points = sorted(points, key=lambda x: x[1]) ## sort the points of y
        for i in range(0, len(points) -1):
            dist = floor(distance(points[i][1],points[i][0],points[i+1][1],points[i+1][0]))
            if ( dist > 100):
                cv2.rectangle(img_rgb, points[i], (points[i][0] + w, points[i][1] + h), COLORS[x], 2)
                newPoints.append(points[i])
                allPoints.append(points[i])

            else:
                amoutOfRemovedPoints +=1

        print "POINTS: %s" % (len(newPoints))
        info.append((threshold,x,len(newPoints))) # THRESHOLD, LABEL_INDICE, AMOUNT OF POINTS FIND
        print "REMOVED %s\n" % (amoutOfRemovedPoints)

    allPoints = sorted(allPoints, key=lambda x: x[1])
    print "ALL POINTS FINDED"
    print allPoints
    print "\n"
    lineNumber = 0
    amountFinded = 0

    print "AMOUNT OF POINTS FINDED BY EACH LINE"
    for i in range (1, len(allPoints) ):
        # dist = floor(distance(allPoints[i][1],allPoints[i][1],allPoints[i+1][0],allPoints[i+1][1]))
        # print dist
        if ( (allPoints[i][1] > (allPoints[i-1][1] + 50))):
            print "Line: %s = %s" % (lineNumber+1,  amountFinded+1)
            lineNumber+=1
            amountFinded = 0

            # cv2.rectangle(img2, allPoints[i], (allPoints[i][0] + w, allPoints[i][1] + h), COLORS[2], 2)
            # height, width = img2.shape[:2]
            # res = cv2.resize(img2,(width/3, height/3), interpolation = cv2.INTER_CUBIC)
            # cv2.imshow("example", res)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        else:
            amountFinded+=1

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

def printHistogram (img_gray):
    hist = cv2.calcHist([img_gray],[0],None,[256],[0,256])
    print "#Histogram"
    print "Color;Amount"
    for i in range(len(hist)):
    	print "%s;%s" % (i, int(hist[i]))
