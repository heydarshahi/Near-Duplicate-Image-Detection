import pybktree
from hash_helper import compute_hash
from PIL import Image
import collections
import os

hash_tree = []
Img = None
id_hash_dict = {}


# TODO hash_list should be persisted
def initialize_bktree():
    global hash_tree, Img
    Img = collections.namedtuple('Img', 'hash id')
    hash_list = []
    hash_tree = pybktree.BKTree(mydistance, hash_list)


# TODO process image without file system (with StringIO)
def process_image(file, action):
    imgstring = file.body
    # print(image)

    filename = "images/" + file.name
    if action == "search":
        filename = "images/uploaded/" + file.name

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


def find_hash_by_id(id):
    global id_hash_dict
    res = id_hash_dict.get(id)
    return res


def add_image(image_hash, id):
    global Img, hash_tree, id_hash_dict

    if id in id_hash_dict:
        return "existing_id"

    id_hash_dict[id] = image_hash
    hash_tree.add(Img(int(image_hash, 16), id))
    print("image with id " + id + " and hash " + image_hash + " added to hash_tree")


def find_duplicates(image_hash, distance):
    global Img, hash_tree
    duplicates = []
    duplicate_hashes = hash_tree.find(Img(int(str(image_hash), 16), 0), int(distance))

    for j in range(0, len(duplicate_hashes)):
        duplicates.append(duplicate_hashes[j][1].id)

    return duplicates


def mydistance(a, b):
    return pybktree.hamming_distance(a.hash, b.hash)
