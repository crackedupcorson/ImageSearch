'''
Created on 3 Mar 2014
Controller class starts process and cleans up the environment before it commences.
Cleans up environment by deleting content in folders.

@author: Ciaran
'''
import shutil
import glob
import os,cv2

for image in glob.glob('original/*.jpg'): #Get any images uploaded.
                                        #(maximum one in this folder usually.
    os.rename(image,'original/origin.jpg') #rename it to origin.jpg
files = glob.glob('compare/*') #Delete all images in comparison folders(compare, compare2 and compare 3)
for f in files:
    os.remove(f)
files2 = glob.glob('compare2/*')
for f2 in files2:
    os.remove(f2)
files3 = glob.glob('compare3/*')
for f3 in files3:
    os.remove(f3)
files4 = glob.glob('C:/xampp/htdocs/fyp/images/*') #Delete all content from apache folder that will display images to user
for f4 in files4:
    os.remove(f4)
                  
execfile('query.py') #Start the next part in process.
def disp():
    for images in glob.iglob("compare3/*.jpg"):
        image = images[:-5] #parse details from image name
        image = image[-12:]
        lat = image[:5]
        long = image[-5:]
        print(lat)
        
