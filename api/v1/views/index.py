#!/usr/bin/python3
"""Modules"""
from flask import jsonify
from api.v1.views import app_views 

@app_views.route('/status', methods=['GET'])
def status():
    """function"""
    return jsonify({"status": "OK"})
