#!/usr/bin/python3
"""app"""

from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_app(exception):
    """request"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 page"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    """Main"""
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
    