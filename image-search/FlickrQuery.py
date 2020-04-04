import  time, datetime, os, flickrapi
from datetime import datetime
from pygeocoder import Geocoder
from shapely.geometry.point import Point
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
from time import strptime, struct_time
import helpers


class FlickrQuery:

    def run(self, search_params):
        time_date = datetime
        estLocation = search_params['estLocation']
        relSearchTags = search_params['tags']
        image = search_params['image_path']
        centerLocation = Geocoder.geocode(estLocation)
        locationCoOrd = centerLocation.coordinates
        try:
            for (k, v) in Image.open(image)._getexif().items():  # Kept in for testing purposes, and managing data
                print('%s = %s' % (TAGS.get(k), v))
                img = Image.open(image)
                exif = img._getexif()
                fs = "%Y:%m:%d %H:%M:%S"  # date format
                pictureDate = helpers.get_field(exif, 'DateTime')  # Date Time
        except AttributeError:
            print("no exif")
            pictureDate = time_date.now().strftime("%Y-%m-%d %H:%M:%S")
            print(datetime)
            fs = "%Y-%m-%d %H:%M:%S"  # date format

        # Steps for using datetime in search
        dtime = strptime(pictureDate, fs)  # 1. Convert datetime to a usable format. Currently in string.

        # Determine time of day from hour
        timetag = helpers.get_time_of_day(str(time.strftime("%H", dtime)))

        # Determine season from month
        original_photo_season = helpers.get_season(str(time.strftime("%B", dtime)))
        ###########################################################################
        # Section for image query
        # flickr information: 
        # key: 73bd8fc4f4657de00e9f74dc75d1262a
        # secret: 0a8620b19f669bd0
        # flickr app address: www.flickr.com/services/apps/72157638043790766/   
        ###########################################################################
        api_key = "73bd8fc4f4657de00e9f74dc75d1262a"  # API key
        secret = "0a8620b19f669bd0"  # shared "secret"
        try:  # Try to search, (with an except fro FlickrErrors) (works like a try catch)
            flickr = flickrapi.FlickrAPI(api_key, secret)  # Search for photos
            for photo in flickr.walk(flickrKey=api_key,
                                     ispublic="1",  # Returns only public photos
                                     media="photos",
                                     # text=  #This parameter seriously limits results. DO NOT USE.
                                     hasgeo="1",  # Hasgeo 1 = has gps tags, 0 = does not have gps tags
                                     tags=relSearchTags,  # Tags included (coming from tag.txt)
                                     # geo_context = "0", #0 undefined, 1 indoors, 2 outdoors
                                     # Problem with GeoContext, as it terminates search.
                                     accuracy="11",  # Accuracy level, 10 being city
                                     content_type="1",
                                     extras="date_upload, views",
                                     ):
                photoid = photo.get("id")  # Get the photo ID
                # 1. Need to get the date attrib from photo, but doesn't come as standard, when searching.
                # Photo is shown as id, farmid and serverid -> therefore the attrib for date needs to be generated else where?

                # Does flickr have a "get attributes of photo?" Wont have exif, but does it have date taken
                # Limiting the date of photo to when photo was taken really improves the quality of search.
                # eg  datetaken = flickr.photos_getattrib()

                photoLocation = flickr.photos_geo_getLocation(photo_id=photoid, accuracy="6")
                lat2 = float(photoLocation[0][0].attrib["latitude"])
                long2 = float(photoLocation[0][0].attrib["longitude"])
                lat3 = round(lat2,
                             6)  # round down decimal places -> both  of these are used, concatenated to end of file name
                # (to get the address)
                long3 = round(long2, 6)  # round down decimal places ->
                # flickr privacy setting means no exif data for gps, need to append it from info received from server.
                searchPoints = Point(lat2, long2)  # Search points(used to see if picture is inside buffer)
                addr = lat3, long3  # Appended to end of link name.
                lat = int(locationCoOrd[0])
                long = int(locationCoOrd[1])
                originPoint = Point(lat, long)
                buffer_zone = originPoint.buffer(2)  # Width of buffer around centerLocation(estimated location)
                file_count = 0
                # Check if any of the "photoLocation" photos are inside the buffer around center location.
                if searchPoints.within(buffer_zone):
                    results = flickr.photos_getSizes(api_key=api_key, photo_id=photoid, extras="url_o")
                    results1 = results.find("sizes").findall("size")[0].get('source')
                    urls = results1[:-6] + ".jpg"  # Strip url of the _s at end, to give full image.
                    link = urls[35:]  # Remove the first 35 characters to make a suitable length name;
                    info = flickr.photos_getInfo(api_key=api_key, photo_id=photoid)
                    dateinfo = info.find("photo").find("dates").get("taken")
                    request_date_format = "%Y-%m-%d %H:%M:%S"
                    try:
                        request_date = strptime(dateinfo, request_date_format)
                    except ValueError as e:
                        print(e)
                    comparison_photo_season = helpers.get_season(str(time.strftime("%B", request_date)))
                    if (comparison_photo_season is original_photo_season):
                        path, dirs, files = os.walk("compare/").next()
                        file_count = len(files)  # Current amount of files in folder.
                        limit = 50  # Amount of files in folder(limiting how many to download)
                        print("FILE COUNT IS = TO:  ", file_count)
                        if file_count < limit:  # if amount of files is less than limit, download next file(in loop)
                            addr = str(addr)  # Convert address to string.
                            link = link[:-4]  # remove the jpg,
                            link += addr  # Append the address
                            link += ".jpg"  # Append the jpg back on
                            print("downloading picture from {}: ".format(link))
                        else:
                            break

                else:
                    print("picture not within area", addr)
        except (Exception) as e:
            # exceptions found in search such as get address info failures(gai),socket connection erros and bad statuses
            print(e)  # print the exception



