#!/usr/bin/python3
"""Modules"""
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retye"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review_list = []
    for review in place.reviews:
        review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """fof"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ Createing """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    data = request.get_json()
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    data['place_id'] = place_id
    instance = Review(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """ Updateing """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id',
                       'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
