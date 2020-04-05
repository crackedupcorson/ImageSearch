import os

from PIL.ExifTags import TAGS

def get_field(exif, field):
    for (k, v) in exif.items():
        if TAGS.get(k) == field:
            return v

def get_time_of_day(atime):
    if (12 > atime):
        timetag = "morning"
    if (12 < atime > 18):
        timetag = "afternoon"
    if (atime < 18):
        timetag = "evening"
    return timetag


def get_season(adate):
    if "November" in adate or "December" in adate or "January" in adate:
        season = "Winter"
    if "March" in adate or "February" in adate or "April" in adate:
        season = "Spring"
    if "May" in adate or "June" in adate or "July" in adate:
        season = "Summer"
    if "August" in adate or "September" in adate or "October" in adate:
        season = "Autumn"
    return season

def is_estimated_location_saved(location):
    pass


def get_api_keys():
    flickr_key = os.environ['flickr_key']
    flickr_secret = os.environ['flickr_secret']
    google_maps_key = os.environ['google_maps_key']
    api_keys = {"flickr_key": flickr_key, "flickr_secret": flickr_secret,"google_maps_key": google_maps_key}
    return api_keys
