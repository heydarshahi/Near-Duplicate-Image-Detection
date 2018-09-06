from sanic import Sanic
from sanic.response import json, file, text, html, stream, file_stream
from image_helper import *
import os

app = Sanic()

initialize_bktree()
print('bktree initialized')


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

@app.post("/image")
def post_file_json(request):
    print('file received...')
    print('--')
    file_parameters = {}
    request_type = request.form.get('request_type')  # "add" or "search"
    request_by = request.form.get('request_query')  # "hash" or "image"

    if request_by == "hash":
        image_hash = request.form.get("hash")

    elif request_by == "image":
        test_file = request.files.get('theimage')
        file_parameters = {
            'body': test_file.body,
            'name': test_file.name,
            'type': test_file.type,
        }
        image = process_image(test_file, request_type)
        image_hash = find_hash(image)

    if request_type == "add":
        add_image(image_hash, test_file.name)
        return json({'received': True, 'file_names': file_parameters['name'], 'hash': image_hash})

    elif request_type == "search":
        distance = request.form.get("distance")
        duplicates = find_duplicates(image_hash, distance)
        # duplicates_result_html = image_to_html(test_file.name, duplicates)
        # return html(duplicates_result_html)
        return json({"query image": test_file.name, "duplicate_count": len(duplicates),
                     "duplicate file list": duplicates})

# forms

@app.route("/form")
def post_json(request):
    return json({"received": True, "form_data": request.form, "test": request.form.get('test')})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
