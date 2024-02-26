#!/usr/bin/python3
""" view """
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from api.v1.views import app_views
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Retrieves """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    place_list = []
    for place in city.places:
        place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place  """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Creates """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    data['city_id'] = city_id
    instance = Place(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ Updates """
    data = request.get_json()

    if data is None:
        error_dict = {"error": "Not a JSON"}
        return jsonify(error_dict), 400

    single_place = storage.get("Place", place_id)

    if single_place is None:
        abort(404)

    if 'description' in data:
        setattr(single_place, 'description', data['description'])

    if 'number_rooms' in data:
        setattr(single_place, 'number_rooms', data['number_rooms'])

    if 'number_bathrooms' in data:
        setattr(single_place, 'number_bathrooms', data['number_bathrooms'])

    if 'max_guest' in data:
        setattr(single_place, 'max_guest', data['max_guest'])

    if 'price_by_night' in data:
        setattr(single_place, 'price_by_night', data['price_by_night'])

    if 'latitude' in data:
        setattr(single_place, 'latitude', data['latitude'])

    if 'longitude' in data:
        setattr(single_place, 'longitude', data['longitude'])

    if 'amenity_ids' in data:
        setattr(single_place, 'amenity_ids', data['amenity_ids'])

    setattr(single_place, 'name', data['name'])
    single_place.save()
    storage.save()

    return jsonify(single_place.to_dict())
