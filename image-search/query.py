import glob
import os
from FlickrQuery import FlickrQuery


class Query:
    def run(self, search_params):
        for image in glob.glob('original/*.jpg'):  # Get any images uploaded.
            # only one supported at the moment. future we can do more
            os.rename(image, 'original/origin.jpg')  # rename it to origin.jpg
            search_params.update({"image_path": 'original/origin.jpg'})
            fq = FlickrQuery()
            fq.run(search_params)
