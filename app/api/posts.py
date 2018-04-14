# -*- coding: utf-8 -*-
from flask import request, abort, jsonify

from app import app, db
from app.models import User, EcgDate


@app.route('/api/v1.0/users', methods=['POST'])
def create_user():
    # print(request.json)
    # TODO login from api
    if not request.json or 'name' not in request.json:
        abort(400)
    worker = DbWorker()
    new_user = worker.add_new_user(request.json['name'],
                                   request.json.get('description', None))
    return jsonify({'user': new_user}), 201


@app.route('/api/v1.0/ecg_data', methods=['POST'])
def add_ecg_data():
    if not request.json or 'data' not in request.json or \
            'email' not in request.json or \
            'password' not in request.json:
        abort(400)
    user = db.session.query(User).filter_by(
        email=request.json['email']).one()
    if not user.check_password(request.json['password']):
        abort(401)
    '''
    xs = list(map(int, request.json['data'].split()[::2]))
    for i in range(1, len(xs)):
        xs[i] += xs[i - 1]
    ys = list(map(int, request.json['data'].split()[1::2]))
    ys = list(map(lambda y: math.log(y - 1000) - 1, ys))
    values = list(zip(xs, ys))
    '''

    db.session.add(
        EcgDate(
            data=request.json['data'],
            user_id=user.id
        )
    )
    db.session.commit()
    return "OK", 201