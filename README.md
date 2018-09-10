# similar-image-detection
simple near-duplicate detection

## Description
This is a simple near-duplicate detection web app based on image-hash algorithm and BK-Tree data structure.


As webapp.py is run, `initialize_bktree()` is called, the BK-Tree is initialized from
__files/hashlist.txt__.


### Run Server
Run `webapp.py` to initialize server. Open a browser and navigate to "0.0.0.0:8000/html" 
for a simple client demonstration. 
You can also send POST messages using Postman or Advanced REST Client. The message type 
should be __multipart/form-data__ and the parameters should be:

- type="file", name="theimage" (the jpg or png file to add/search)
- name="request_query", value: "image" or "hash" or "id"
- name="request_id", value: ID of the added/searched image

## Modules & Functions

- **webapp.py**: Main function that sets up a Sanic web server. Functions include:

    - _post_file_json()_: Two routes are handled by this function:
        - **/image/add**: a post request (as described in the Description part) should be sent, to add
        new images. Adding should be by image and id. **Returns** a json file with status "file received"
         or "existing ID".
        - **/image/search**: to search for an image by id or image. **Returns** a json file with a list
        of duplicate IDs. 
        
    - _notify_server_stopping(app, loop)_: This is called before server stops to persist the added hashes
    by calling _image_helper.persist_hash_tree()_
        
- **image_helper.py**: This module consists of all the background adding and searching functions. 
Functions include:

    - _initialize_bktree()_: Reads previously saved hashes from _/files/hashlist.txt_ and builds a 
    BK-Tree of **Img(hash, id)** object. Img is also a collection.
    
    - _process_image(file)_: Returns a Pillow.Image object from a file.
    
    - _find_hash(image)_: Gets an Image and returns its hash using the function in module **hash_helper**
    
    - _find_hash_by_id(id)_: Gets an ID and searches in `id_hash_dict` dictionary which contains all id-hash
    tuples.
    
    - _add_image(image_hash, id)_: Creates an **Img**, checks if the ID is existing, then adds to the `hash_tree` and `id_hash_dict` variables.
    
    - _find_duplicates(image_hash, distance)_:  Searches the `hash_tree` for images whose hashes are from
    from hamming distance of at most `distance` from the query hash. 
    
    - _mydistance(img1, img2)_: Takes two **Img** object and returns the hamming distance of their hashes.
    
    - _persist_hash_tree()_: Saves `id_hash_dict` into _/files/hashlist.txt_ file.
    
        
- **hash_helper.py**
This is for computing the hash of an image using **imagehash** library.