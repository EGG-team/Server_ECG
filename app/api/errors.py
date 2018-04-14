# -*- coding: utf-8 -*-
from flask import jsonify, make_response

from app import app


@app.errorhandler(400)
def bad_request(error):
    print(error)
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(error):
    print(error)
    return make_response(jsonify({'error': 'Not Found'}), 404)
