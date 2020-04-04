import glob
import os

import FlickrQuery



def disp():
    for images in glob.iglob("compare3/*.jpg"):
        image = images[:-5]  # parse details from image name
        image = image[-12:]
        lat = image[:5]
        long = image[-5:]
        print(long, lat)