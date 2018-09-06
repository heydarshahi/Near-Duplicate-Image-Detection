import pybktree
from hash_helper import compute_hash
from PIL import Image
import glob
import collections
import os

hash_tree = []
Img = None
ID = 0


def initialize_bktree():
    global hash_tree, Img, ID
    hash_tree = []
    Img = collections.namedtuple('Img', 'hash filename id')
    ID = 0
    cnt = 0
    hash_list = []

    try:
        img_list = glob.glob('images/*.png')
        img_list=img_list + glob.glob('images/*.jpg')
        for filename in img_list:
            img = Image.open(filename)
            hashed = compute_hash(img, mode='dhash')

            hash_list.append(Img(int(str(hashed), 16), filename, cnt))
            cnt = cnt + 1

    except IOError:
        print('IOError')
        pass

    hash_tree = pybktree.BKTree(mydistance, hash_list)


def process_image(file, action):
    imgstring = file.body
    # print(image)

    filename = 'images/' + file.name
    with open(filename, 'wb') as f:
        f.write(imgstring)
        f.close()

    res = Image.open(filename)
    if action == "search":
        os.remove(filename)
    return res


def find_hash(img):
    hash_string = str(compute_hash(img))
    return hash_string


def add_image(image_hash):
    global ID, Img, hash_tree
    hash_tree.add(Img(int(image_hash, 16), ID, ID))
    print("image with hash " + image_hash + " added to hash_tree")
    ID = ID + 1


def find_duplicates(image_hash, distance):
    global Img, hash_tree
    duplicates = []
    duplicate_hashes = hash_tree.find(Img(int(str(image_hash), 16), 'gg', 'gg'), int(distance))

    for j in range(0, len(duplicate_hashes)):
        duplicates.append(duplicate_hashes[j][1].filename)

    return duplicates


def mydistance(a, b):
    return pybktree.hamming_distance(a.hash, b.hash)


# return html form to show duplicates
def image_to_html(filename, duplicates):
    start = """<!DOCTYPE html><html>
    <head>
        <meta charset="UTF-8">
        <title>Duplicates Result</title>
    </head>

    <body style="text-align: center">

    <h1>Your Image</h1>
    <img src="images/""" + str(filename) + """"><br><br>
    <h1>Duplicates</h1>
    """

    duplicates_html = ""
    for duplicate_image in duplicates:
        duplicates_html = duplicates_html + """<img src=" """ + str(duplicate_image) + """"> """


    ending = """</body>
    </html>"""

    return str(start+duplicates_html+ending)