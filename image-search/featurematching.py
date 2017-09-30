#Code reproduced with permission of OpenCV tutorials.
# Link  ->
# By
# Example 
#Code has been edited to work with multiple images in a for loop.
import numpy as np
import cv2
from matplotlib import pyplot as plt
import glob
import os
import shutil,gc

MIN_MATCH_COUNT = 40 #Min amount of keypoints matched, for image considered to be alike.

img1 = cv2.imread('original/origin.jpg',0)          # queryImage
for image in glob.iglob("compare/*.jpg"): 
	#START OF CODE REPRODUCED WITH PERMISSION OF OPENCV TUTORIALS.
    #print(image)
    img2 = cv2.imread(image) # comparison images
    
    # Initiate SIFT detector
    sift = cv2.SIFT()
    
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    
    
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 2)
    search_params = dict(checks = 250) #higher the check, better the precision
    
    #Flann (Fast Library for Approximate Nearest Neighbors)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    
    matches = flann.knnMatch(des1,des2,k=2) #Uses K-nearest neighbour
    
    # store all the good matches with regards to Lowe's ratio test. (David Lowe being the creator of SIFT)
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    #If the amount of matches is greater than the minimal match count(accepted amount of matches)
    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    
        M, mask = cv2.findHomography(src_pts,dst_pts,0,5.0)#Find homography
        matchesMask = mask.ravel().tolist()
    
        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)
    
        img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
    
    else:
        print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT) #Not enough matches to be considered a success.
        matchesMask = None
    #Create the parameters for the draw parameters(between photos)
    draw_params = dict(matchColor = (255,0,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)
    #Draw the matches.
    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
	#END OF CODE REPRODUCED WITH PERMISSION OF OPENCV TUTORIALS
    print(len(good))#Print the amount of matches. If there's a lot,
    amount = len(good)
    if amount >= MIN_MATCH_COUNT: #if the matches are more than (this can be altered, 
		#after a bit of testing to determine the lowest it performs well at)
        gc.collect() #Collect garbage, freeing image variable from process.(seems to be stuck if this isn't called)	
        dest = 'compare2/' #Destination is compare2, folder used in the next process.(Histogram comparison)
        shutil.copy(image, dest)#Copty image to compare2/
        
#Once feature matching has removed features which do not match uploaded image, move onto histogram compari
execfile('histrogramcomparison.py')