#!/usr/bin/python3
"""  application"""
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """status"""
    return (jsonify({"status": "OK"}))


@app_views.route("/stats", strict_slashes=False)
def stats():
    """ objects"""
    objs_dict = storage.all()
    count_dict = {}

    classes = [Amenity, City, Place, Review, State, User]

    for i in classes:
        count = storage.count(i)

        if count == 0:
            continue
        if i == Amenity:
            count_dict["amenities"] = count

        elif i == City:
            count_dict["cities"] = count

        elif i == Place:
            count_dict["places"] = count

        elif i == Review:
            count_dict["reviews"] = count

        elif i == State:
            count_dict["states"] = count

        elif i == User:
            count_dict["users"] = count

    return (jsonify(count_dict))
