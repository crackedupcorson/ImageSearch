import datetime, os, flickrapi
from datetime import datetime

import requests
from shapely.geometry.point import Point
from PIL import Image
from PIL.ExifTags import TAGS
from time import strptime
import helpers


class FlickrQuery:

    def run(self, search_params):
        time_date = datetime
        estLocation = search_params['estLocation']
        relSearchTags = search_params['tags']
        image = search_params['image_path']
        google_location = self.get_coordinates(estLocation)
        self.get_date_exif(image, time_date)

        api_key = helpers.get_api_keys()["flickr_key"]
        secret = helpers.get_api_keys()["flickr_secret"]
        try:  # Try to search, (with an except fro FlickrErrors) (works like a try catch)
            flickr = flickrapi.FlickrAPI(api_key, secret)  # Search for photos
            id_list = []
            count = 0
            lat = google_location['lat']
            long = google_location['lng']
            originPoint = Point(lat, long)
            buffer_zone = originPoint.buffer(1.8, 1)
            min_upload_date  = helpers.get_mintime_in_millis(5)
            for photo in flickr.walk(flickrKey=api_key,
                                     ispublic="1",  # Returns only public photos
                                     media="photos",
                                     hasgeo="1",
                                     tags=relSearchTags,  # Tags included (coming from tag.txt)
                                     accuracy="12",  # 1 - 16. Higher number = more accurate
                                     content_type="1",
                                     extras="date_upload, views"
                                     ):
                photo_id = photo.get("id")  # Get the photo ID
                count += 1
                photoLocation = flickr.photos_geo_getLocation(photo_id=photo_id, accuracy="6")
                lat2 = float(photoLocation[0][0].attrib["latitude"])
                long2 = float(photoLocation[0][0].attrib["longitude"])
                lat3 = round(lat2, 6)
                long3 = round(long2, 6)
                search_point = Point(lat2, long2)
                address = lat3, long3
                if search_point.within(buffer_zone):
                    results = flickr.photos_getSizes(api_key=api_key, photo_id=photo_id, extras="url_o")
                    results1 = results.find("sizes").findall("size")[0].get('source')
                    urls = results1[:-6] + ".jpg"  # Strip url of the _s at end, to give full image.
                    link = urls[35:]  # Remove the first 35 characters to make a suitable length name;
                    compare_iterator = os.walk("compare/")
                    path, dirs, files = compare_iterator.__next__()
                    file_count = len(files)  # Current amount of files in folder.
                    limit = search_params['limit']
                    if file_count < limit:
                        self.download_image(address, file_count, link, urls, photo_id, id_list)
                    else:
                        break
        except Exception as e:
            # exceptions found in search such as get address info failures(gai),socket connection erros and bad statuses
            print(e)  # print the exception

    def get_date_exif(self, image, time_date):
        try:
            for (k, v) in Image.open(image)._getexif().items():  # Kept in for testing purposes, and managing data
                print('%s = %s' % (TAGS.get(k), v))
                img = Image.open(image)
                exif = img._getexif()
                fs = "%Y:%m:%d %H:%M:%S"  # date format
                picture_date = helpers.get_field(exif, 'DateTime')  # Date Time
        except AttributeError:
            print("no date found in exif metadata")
            picture_date = time_date.now().strftime("%Y-%m-%d %H:%M:%S")
            print(picture_date)

    def download_image(self, address, file_count, link, urls, photo_id, id_list):
        if photo_id not in id_list:
            address = str(address)  # Convert address to string.
            link = link[:-4]  # remove the jpg,
            link += address  # Append the address
            link += ".jpg"  # Append the jpg back on
            print("downloading picture from {}: ".format(urls))
            response = requests.get(urls, stream=True)
            if response.status_code == 200:
                with open("compare/flickr_comparison_image_{}.jpg".format(file_count), 'wb+') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
            id_list.append(photo_id)

    def get_coordinates(self, estLocation):
        location = helpers.is_estimated_location_saved(estLocation)
        return location
