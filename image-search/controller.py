import glob
import os

from PIL import Image
from PIL.ExifTags import TAGS

from query import Query
from featurematching import FeatureMatching
from histrogramcomparison import HistogramComparison


def get_tags():
    if get_name() is not "" or get_name() is None:
        return "bar,pub,pints,cafe,westbury,{},{}".format(get_name(), get_location())
    else:
        return "bar,pub,pints,cafe,{}".format(get_location())


def get_name():
    return "grogans"


def does_photo_contain_gps_exif():
    image = get_tags()['image_path']
    try:
        for (k, v) in Image.open(image)._getexif().items():  # Kept in for testing purposes, and managing data
            print('%s = %s' % (TAGS.get(k), v))
            img = Image.open(image)

    except AttributeError:
        pass


def get_location():
    return "South William Street, Dublin"


def clean_folders():
    files = glob.glob('compare/*')  # Delete all images in comparison folders(compare, compare2 and compare 3)
    for f in files:
        os.remove(f)
    files = glob.glob('compare2/*')  # Delete all images in comparison folders(compare, compare2 and compare 3)
    for f in files:
        os.remove(f)
    files = glob.glob('compare3/*')  # Delete all images in comparison folders(compare, compare2 and compare 3)
    for f in files:
        os.remove(f)


def get_limit():
    return 600


def run():
    clean_folders()
    search_params = {"estLocation": get_location(), "tags": get_tags(), "limit": get_limit()}
    query = Query()
    query.run(search_params)
    fm = FeatureMatching()
    fm.compare_photos()
    hc = HistogramComparison()
    hc.run()


def display():
    for images in glob.iglob("compare3/*.jpg"):
        image = images[:-5]
        image = image[-12:]
        lat = image[:5]
        long = image[-5:]
        print(long, lat)


if __name__ == "__main__":
    run()
