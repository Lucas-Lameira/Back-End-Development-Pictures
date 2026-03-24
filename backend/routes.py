from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))


######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200


######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)


######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture.get('id') == id:
            return jsonify(picture)
    
    return jsonify(message=f'picture {id} not found'), 404



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    request_data = request.get_json()

    new_picture_id = request_data.get('id')

    for picture in data:
        if picture.get('id') == new_picture_id:
            return jsonify(
                Message=f"picture with id {new_picture_id} already present"
            ), 302

    data.append(request_data)

    return jsonify(request_data), 201


######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    request_data = request.get_json()
    update_index = None

    for index, picture in enumerate(data):
        if id == picture.get('id'):
            update_index = index
            break
    
    if update_index is None:
        return {"message": "picture not found"}, 404
    
    data[update_index].update(request_data)

    return data[update_index], 200


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    delete_index = None

    for index, picture in enumerate(data):
        if id == picture.get('id'):
            delete_index = index
            break
    
    if delete_index is None:
        return {"message": "picture not found"}, 404
    
    data.pop(delete_index)

    return jsonify(), 204
