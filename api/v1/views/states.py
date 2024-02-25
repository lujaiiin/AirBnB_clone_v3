#!/usr/bin/python3
"""Modules"""
from flask import Blueprint, request, jsonify
from models import State, db

states_bp = Blueprint('states', __name__)

@states_bp.route('/states', methods=['GET'])
def get_states():
    states = State.query.all()
    return jsonify([state.to_dict() for state in states])

@states_bp.route('/states/<int:state_id>', methods=['GET'])
def get_state(state_id):
    state = State.query.get(state_id)
    if state is None:
        return jsonify({'error': 'State not found'}),   404
    return jsonify(state.to_dict())

@states_bp.route('/states/<int:state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = State.query.get(state_id)
    if state is None:
        return jsonify({'error': 'State not found'}),   404
    db.session.delete(state)
    db.session.commit()
    return jsonify({}),   200

@states_bp.route('/states', methods=['POST'])
def create_state():
    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}),   400
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}),   400
    new_state = State(name=data['name'])
    db.session.add(new_state)
    db.session.commit()
    return jsonify(new_state.to_dict()),   201

@states_bp.route('/states/<int:state_id>', methods=['PUT'])
def update_state(state_id):
    state = State.query.get(state_id)
    if state is None:
        return jsonify({'error': 'State not found'}),   404
    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}),   400
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    db.session.commit()
    return jsonify(state.to_dict()),   200
