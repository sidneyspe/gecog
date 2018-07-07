import sys
import os
import shutil
import cv2
import math
import numpy as np
import glob

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
    for x in range(len(entries)):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template = cv2.cvtColor(entries[x], cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, method)
        loc = np.where( res >= threshold)
        amountPoint = 0
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), COLORS[x], 2)
            amountPoint +=1
        info.append((threshold,x,amountPoint)) # THRESHOLD, LABEL_INDICE, AMOUNT OF POINTS FIND
    return img_rgb, info

def printResult (meth, output):
    print "USING %s METHOD \n" % (meth)
    for out in output:
    	print "THRESHOLD: %s\t" % (out[0][0])
    	for i in range(len(out)):
    		print "LABEL: %s\t AMOUNT: %s" % (str(out[i][1]), str(out[i][2]))
    	print "\n"

def printCSV (meth, output):
    print " \t0\t1\t2"
    for out in output:
        print "%s\t%s\t%s\t%s" % (str(out[0][0]),str(out[0][2]), str(out[1][2]), str(out[2][2]))
