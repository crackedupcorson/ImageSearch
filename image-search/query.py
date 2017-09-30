'''
Created on 28 Jan 2014
@author: Ciaran Corson
Query creates a search to find similar images to the one the user provides.
It does this by searching based on similarity of estimated location, date and time tags, and so forth.
Naturally, there is still room for improvement in this regard as the search could be and needs to be more effective than it currently is.
It still does however provide enough similar images(when a good search is made), to return a good result.
'''
import sys,string, math, time,datetime, socket,os,flickrapi,urllib,urllib2,json,shutil
from datetime import datetime 
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
from time import strptime, struct_time
from docutils.languages import da
from __builtin__ import str
from pygeocoder import Geocoder
import geopy
import glob
import shapely
from shapely import wkt as wkt
from shapely.geometry import point
from shapely.geometry.point import Point
from flickrapi.exceptions import FlickrError 
from _elementtree import ParseError
from httplib import BadStatusLine

image = "original/origin.jpg"
with open ("original/estLoc.txt", "r") as file1: #estimated location stored in text file
    estLocation=file1.read()
with open ("original/tags.txt","r") as file2: # search tags are stored in text file.
    relSearchTags=file2.read()
       
 #Using Geocoder to get a geocode to use in flickr.getGeo(to onlw download images near gps given)
centerLocation = Geocoder.geocode(estLocation) 
locationCoOrd = centerLocation.coordinates 
print(locationCoOrd)
#get a particular exif field       
def get_field (exif,field):
    for (k,v) in exif.items():
         if TAGS.get(k) == field:
            return v
try:
    for (k,v) in Image.open(image)._getexif().items(): #Kept in for testing purposes, and managing data
            print ('%s = %s' % (TAGS.get(k), v))
            img = Image.open(image)
            exif = img._getexif()
            fs="%Y:%m:%d %H:%M:%S" #date format
            datetime = get_field(exif,'DateTime')#Date Time
except AttributeError:
    print("no exif")
    datetime =datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(datetime)
    fs="%Y-%m-%d %H:%M:%S" #date format

   
#Steps for using datetime in search
dtime = strptime(datetime,fs) #1. Convert datetime to a usable format. Currently in string. 
atime =  str(time.strftime("%H", dtime))#2 Split time and date, getting the hours
adate = str(time.strftime("%B", dtime)) #3 Get the month

#Determine time of day from hour
if(12 > atime):
    timetag="morning"
if(12 < atime > 18):
    timetag="afternoon"
if(atime < 18):
    timetag="evening" 
    
#Determine season from month
if "November" in adate or "December" in adate or "January" in adate:
    dseason="Winter"
if "March" in adate or "February" in adate or "April" in adate:
    dseason="Spring"
if  "May" in adate or "June" in adate or "July" in adate:
    dseason="Summer"
if "August" in adate or "September" in adate or "October" in adate:
    dseason="Autumn"
###########################################################################
# Section for image query
# flickr information: 
# key: 73bd8fc4f4657de00e9f74dc75d1262a
# secret: 0a8620b19f669bd0
# flickr app address: www.flickr.com/services/apps/72157638043790766/   
###########################################################################
api_key = "73bd8fc4f4657de00e9f74dc75d1262a" # API key
secret = "0a8620b19f669bd0"                  # shared "secret"
try: #Try to search, (with an except fro FlickrErrors) (works like a try catch) 
    flickr = flickrapi.FlickrAPI(api_key, secret) #Search for photos
    for photo in flickr.walk(flickrKey = api_key,
                             ispublic="1", #Returns only public photos
                             media="photos",
                             #text=  #This parameter seriously limits results. DO NOT USE.
                             hasgeo ="1", #Hasgeo 1 = has gps tags, 0 = does not have gps tags
                             tags = relSearchTags, #Tags included (coming from tag.txt)
                             #geo_context = "0", #0 undefined, 1 indoors, 2 outdoors
                             #Problem with GeoContext, as it terminates search.
                             accuracy = "11", #Accuracy level, 10 being city
                             content_type = "1",
                             extras = "date_upload, views",
                             ):  
          photoid = photo.get("id") #Get the photo ID
          #1. Need to get the date attrib from photo, but doesn't come as standard, when searching. 
                #Photo is shown as id, farmid and serverid -> therefore the attrib for date needs to be generated else where?
                
                    #Does flickr have a "get attributes of photo?" Wont have exif, but does it have date taken
                    #Limiting the date of photo to when photo was taken really improves the quality of search.
                    #eg  datetaken = flickr.photos_getattrib()
                   
          photoLocation = flickr.photos_geo_getLocation(photo_id=photoid,accuracy="6") 
          lat2 = float(photoLocation[0][0].attrib["latitude"])
          long2 = float(photoLocation[0][0].attrib["longitude"])
          lat3 = round(lat2,6)#round down decimal places -> both  of these are used, concatenated to end of file name
          #(to get the address)
          long3 = round(long2,6)#round down decimal places -> 
          #flickr privacy setting means no exif data for gps, need to append it from info received from server.
          searchPoints = Point(lat2,long2)#Search points(used to see if picture is inside buffer)
          addr = lat3,long3 #Appended to end of link name.
          lat = int(locationCoOrd[0])
          long = int(locationCoOrd[1])
          originPoint = Point(lat,long)
          buff1 = originPoint.buffer(2)  #Width of buffer around centerLocation(estimated location)
          file_count = 0     
          #Check if any of the "photoLocation" photos are inside the buffer around center location.
          if searchPoints.within(buff1):
              results = flickr.photos_getSizes(api_key = api_key,photo_id=photoid,extras="url_o")  
              results1 = results.find("sizes").findall("size")[0].get('source') #Get the source for each link by photoid, returns thumbnail link
              urls = results1[:-6] + ".jpg" #Strip url of the _s at end, to give full image.
              link = urls[35:]#Remove the first 35 characters to make a suitable length name;
              info = flickr.photos_getInfo(api_key=api_key,photo_id=photoid)
              dateinfo = info.find("photo").find("dates").get("taken")
              fs1="%Y-%m-%d %H:%M:%S"
              try:
                  gdate = strptime(dateinfo,fs1)
                  gdate = str(time.strftime("%B", gdate))
              except ValueError as e:
                  print(e)
              if "November" in gdate or "December" in gdate or "January" in gdate:
                  gseason="Winter"
              if "March" in gdate or "February" in gdate or "April" in gdate:
                  gseason="Spring"
              if  "May" in gdate or "June" in gdate or "July" in gdate:
                  gseason="Summer"
              if "August" in gdate or "September" in gdate or "October" in gdate:
                  gseason="Autumn"
              if(gseason is dseason):
                  path, dirs, files = os.walk("compare/").next()
                  file_count = len(files)#Current amount of files in folder.
                  limit = 50 #Amount of files in folder(limiting how many to download)
                  print("FILE COUNT IS = TO:  ",file_count)
                  if file_count < limit: #if amount of files is less than limit, download next file(in loop) 
                      addr = str(addr)#Convert address to string.
                      link = link[:-4]#remove the jpg, 
                      link += addr #Append the address
                      link +=".jpg" #Append the jpg back on
                      urllib.urlretrieve(urls, r"compare/"+link) #retrieve URL and download it into /compare folder
                    
                      print("downloading picture: "+link)
                  else:
                      break
                  
          else:
            print("picture not within area",addr)
except (FlickrError,ParseError,BadStatusLine,socket.error,urllib2.URLError,socket,socket.gaierror) as e: 
    #exceptions found in search such as get address info failures(gai),socket connection erros and bad statuses
    print(e) #print the exception
    
#Once for loop has ended, either by force or prematurely, move to next process, feature matching.
execfile('featurematching.py')

                 
