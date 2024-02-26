#!/usr/bin/python3
""" a script that starts a Flask web application """
from flask import Flask, blueprints, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

HBNB_API_HOST = os.getenv('HBNB_API_HOST')
HBNB_API_PORT = os.getenv('HBNB_API_PORT')


if HBNB_API_HOST is None:
    HBNB_API_HOST = '0.0.0.0'
if HBNB_API_PORT is None:
    HBNB_API_PORT = 5000


app = Flask(__name__)
app.register_blueprint(app_views)
cros = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ error 404  """
    status = {"error": "Not found"}
    return jsonify(status), 404


if __name__ == '__main__':
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)