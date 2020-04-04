'''
Created on 3 Feb 2014
Code reproduced with permission of OpenCV official tutorials.
link ->
Code has been edited to work with multiple images in a for loop.s
@author: Ciaran
'''
import cv2
import numpy as np
import time
import os,math
import glob,gc,shutil
from PIL import Image
from matplotlib import pyplot as plt
import display
#from query import file_count
total = 0
rootdir ='compare2/' #Files end up in this folder after clearing the feature mathching test. Only matches get this far.
#Start of code reproduced with permission of OpenCV tutorials.
im1 = cv2.imread("original/origin.jpg") 
b1,g1,r1 = cv2.split(im1)
h1 = np.zeros((300,256,3))
bins1 = np.arange(256).reshape(256,1)
color1 = [ (255,0,0),(0,255,0),(0,0,255)] 
for item1,col1 in zip([b1,g1,r1],color1):
        hist_item1 = cv2.calcHist([item1],[0],None,[256],[0,255]) #calculate histogram for each image.
        cv2.normalize(hist_item1,hist_item1,0,255,cv2.NORM_MINMAX)
        hist1=np.int32(np.around(hist_item1))
        pts = np.column_stack((bins1,hist1))
        cv2.polylines(h1,[pts],False,col1)
for images in glob.glob("compare2/*.jpg"):
    im2=cv2.imread(images)
    b,g,r = cv2.split(im2)
    h = np.zeros((300,256,3))
    bins = np.arange(256).reshape(256,1) # np.arange returns evenly spaced values within a given interval, 
    color = [ (255,0,0),(0,255,0),(0,0,255) ] #Color array for each image
    for item,col in zip([b,g,r],color):
        hist_item = cv2.calcHist([item],[0],None,[256],[0,255]) #calculate histogram for each image.
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        pts = np.column_stack((bins,hist))
        cv2.polylines(h,[pts],False,col)
    base_test1 = cv2.compareHist(hist_item,hist_item1,0)#4 methods (0-3) #0 works best
	#end of code reproduce with permission of OpenCV tutorials.
    if 0.4 > base_test1: #0.4 allows for a 40% difference, which after testing is the most suitable range.
        pc = round(base_test1,3) #Round base_test to 3 decimal places
        pc = pc * 100 #Convert PC to a percent
        pc = pc / 1
        pc = str(pc)
        if ("-" in pc): #remove the - symbol from the result.s
            pc = pc.replace("-","")
        pc1 = float(pc)
        pc1 = 100-pc1
        pc = str(pc1)
        images1 = images[:-4]
        images1 = images1 + pc
        images1 = images1 + ".jpg"
        os.rename(images, images1)
        gc.collect()
        dest = 'compare3/' #Compare 3 folder
        shutil.copy(images1, dest)
        path, dirs, files = os.walk("compare3/").next()
        file_count1 = len(files) #File count on folders, used to calculate % average for all images combined.
        total = total + pc1
        avg = total/file_count1
        avg = round(avg)
        print(total,"and ",avg)
        display.disp(pc1)





        