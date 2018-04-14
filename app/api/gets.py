# -*- coding: utf-8 -*-
from flask import jsonify

from app import app


@app.route('/api/v1.0/ecg_data', methods=['GET'])
def get_user():
    return jsonify({'user': 'pidor'})
