import json

def c_bbox(east, south, north, west):

    bbox = {
        "east": east,
        "south": south,
        "north": north,
        "west": west,
    }


    polygon = [
        [bbox["west"], bbox["south"]],
        [bbox["west"], bbox["north"]],
        [bbox["east"], bbox["north"]],
        [bbox["east"], bbox["south"]],
        [bbox["west"], bbox["south"]]
    ]

    return [polygon]
