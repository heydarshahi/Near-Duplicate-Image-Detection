from sanic import Sanic, response
from sanic.response import json, file, text, html, stream, file_stream
from image_helper import initialize_bktree, process_image, add_image\
                        , find_hash, find_hash_by_id, find_duplicates, persist_hash_tree, get_hash_from_request
from sanic_validation import validate_json
import os
from dotenv import load_dotenv

add_schema = {'content-type': {'allowed': ['koe'], 'required': True, 'empty': False},
              'request_id': {'required': True}}

load_dotenv()

initialize_bktree()
print('bktree initialized')

app = Sanic()

@app.route("/")
async def test(request):
    return text("send a post request to /image directory.")


@app.route("/html")
async def handle_image_request(request):

    return html(open('files/html_view.html').read())


# files
@app.post("/image/add/")
@validate_json(add_schema)
async def post_file_add(request):

    request_by, request_id, image_hash = get_hash_from_request(request)

    if image_hash is None:
        return json({"received": False, "description": "ID not existing"})

    add_res = add_image(image_hash, request_id)

    if add_res == "existing_id":
        return json({"received": False, "description": "existing ID"})

    return json({'received': True, 'hash': image_hash})


@app.post("/image/search/")
async def post_file_search(request):
    request_by, request_id, image_hash = get_hash_from_request(request)
    duplicates = find_duplicates(image_hash, os.getenv("DISTANCE", "15"))

    return json({"query image hash": image_hash, "duplicate_count": len(duplicates),
                 "duplicate id list": duplicates})


@app.listener('before_server_stop')
async def notify_server_stopping(app, loop):
    print('Server shutting down!')
    persist_hash_tree()
    print('hash tree persisted.')




if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", "8000"))
