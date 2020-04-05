import glob
import os

from query import Query


def get_tags():
    return "bar,pub"


def get_location():
    return "Dublin city"


def clean_folders():
    files = glob.glob('compare/*')  # Delete all images in comparison folders(compare, compare2 and compare 3)
    for f in files:
        os.remove(f)


def run():
    clean_folders()
    search_params = {"estLocation": get_location(), "tags": get_tags()}
    query = Query()
    query.run(search_params)


def display():
    for images in glob.iglob("compare3/*.jpg"):
        image = images[:-5]
        image = image[-12:]
        lat = image[:5]
        long = image[-5:]
        print(long, lat)


if __name__ == "__main__":
    run()
