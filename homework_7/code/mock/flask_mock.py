import settings
import threading
from flask import Flask, jsonify, request


app = Flask(__name__)
SURNAME_DATA = {}


@app.route('/get_surname/<name>', methods=['GET'])
def get_user_surname(name):
    if surname := SURNAME_DATA.get(name):
        return jsonify(surname), 200
    else:
        return jsonify(f'Surname for user {name} not fount'), 404


@app.route('/put_surname/<name>', methods=['GET'])
def put_user_surname(name):
    if name in SURNAME_DATA.keys():
        SURNAME_DATA[name] = 'new_surname'
        return jsonify(name, SURNAME_DATA[name]), 200
    else:
        return jsonify(f'User {name} not fount'), 404


@app.route('/delete_surname/<name>', methods=['GET'])
def delete_user_surname(name):
    if name in SURNAME_DATA.keys():
        del SURNAME_DATA[name]
        return jsonify(name), 200
    else:
        return jsonify(f'User surname not fount for {name}'), 404


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.Mock.HOST,
        'port': settings.Mock.PORT
    })
    server.start()
    return server


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_mock()
    return jsonify(f'OK, exiting'), 200
