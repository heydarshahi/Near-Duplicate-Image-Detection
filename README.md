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

* type="file", name="theimage" (the jpg or png file to add/search)
* name="request_query", value: "image" or "hash" or "id"
* name="request_id", value: ID of the added/searched image

## Modules & Functions
To be completed.
