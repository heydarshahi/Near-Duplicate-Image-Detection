from sanic import Sanic, response
from sanic.response import json, file, text, html, stream, file_stream
from image_helper import initialize_bktree, process_image, add_image\
                        , find_hash, find_hash_by_id, find_duplicates, persist_hash_tree
import os
from dotenv import load_dotenv


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


@app.get("/html/<filename>")
async def handle_files(request, filename):
    file_list = os.listdir('images/')
    if filename in file_list:
        return await file("images/" + filename)
    return text("file name not founds")


# files

@app.post("/image/<request_type>/")
async def post_file_json(request, request_type):
    print('file received...')
    print('--')
    file_parameters = {}
    # request_type = request.form.get('request_type')  # "add" or "search"
    request_by = request.form.get('request_query')  # "hash" or "image"
    request_id = request.form.get('request_id')

    if request_by == "hash":
        image_hash = request.form.get("hash")

    elif request_by == "image":
        test_file = request.files.get('theimage')
        image = process_image(test_file, request_type)
        image_hash = find_hash(image)

    elif request_by == "id":
        image_hash = find_hash_by_id(request_id)
        if image_hash is None:
            return json({"received": False, "description": "ID not existing"})

    if request_type == "add":
        add_res = add_image(image_hash, request_id)

        if add_res == "existing_id":
            return json({"received": False, "description": "existing ID"})

        return json({'received': True, 'hash': image_hash})

    elif request_type == "search":
        # distance = request.form.get("distance")
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
