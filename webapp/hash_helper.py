from PIL import Image
import imagehash


def compute_hash(img, hashsize=16, mode='dhash'):
    img_resized = img.resize((hashsize, hashsize + 1), Image.ANTIALIAS)

    if mode == 'dhash':
        hashed_img = imagehash.dhash(img_resized)
    elif mode == 'phash':
        hashed_img = imagehash.phash(img_resized)
    elif mode == 'average':
        hashed_img = imagehash.average_hash(img_resized)
    elif mode == 'whash':
        hashed_img = imagehash.whash(img_resized)

    return hashed_img


