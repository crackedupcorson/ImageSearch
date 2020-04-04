import glob
from query import Query

def run():
    print("hello")
    search_params = {"estLocation": "Dublin", "tags": ""}
    query = Query()
    query.run(search_params)

def disp():
    for images in glob.iglob("compare3/*.jpg"):
        image = images[:-5]
        image = image[-12:]
        lat = image[:5]
        long = image[-5:]
        print(long, lat)


if __name__ == "__main__":
    run()