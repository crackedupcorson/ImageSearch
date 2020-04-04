import glob
import os

import FlickrQuery

class Query:

    def run(self, search_params):
        for image in glob.glob('original/*.jpg'):  # Get any images uploaded.
            # only one supported at the moment. future we can do more
            os.rename(image, 'original/origin.jpg')  # rename it to origin.jpg
            estimated_location = search_params["estimated_location"]


