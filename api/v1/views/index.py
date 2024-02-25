#!/usr/bin/python3
"""Modules"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """function"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    """get stats fun"""
    response = {}
    CY = {
	    "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
            }
    for i, k in CY.items():
        response[k] = storage.count(i)
    return jsonify(response)
