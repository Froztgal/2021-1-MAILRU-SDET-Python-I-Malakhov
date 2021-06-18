import json
from flask import Flask, request

app = Flask(__name__)

MOCK_HOST = '0.0.0.0'
MOCK_PORT = 8083
VK_DATA = {}


@app.route('/vk_id/<username>', methods=['GET'])
def get_vk_id_by_username(username):
    if username in VK_DATA.keys():
        return json.dumps({'vk_id': VK_DATA[username]}), 200, {'Content-Type': 'application/json;'}
    else:
        return json.dumps({}), 404, {'Content-Type': 'application/json;'}


@app.route('/vk_id_add/<username>', methods=['POST'])
def post_add_vk_id_by_username(username):
    new_vk_id = request.get_json()['vk_id']
    if username in VK_DATA.keys():
        return f'vk_id: {VK_DATA[username]} for user {username} already exists!', 304
    else:
        VK_DATA[username] = new_vk_id
        return f'vk_id: {new_vk_id} for user {username} added!', 201


@app.route('/vk_id_del/<username>', methods=['GET'])
def get_del_vk_id_by_username(username):
    if username in VK_DATA.keys():
        del VK_DATA[username]
        return f'{username}\'s, vk_id deleted!', 204
    else:
        return f'{username}\'s, vk_id not exists!', 404


@app.route('/shutdown')
def shutdown():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()
    return 'The server shutdown completed!', 200


if __name__ == '__main__':
    app.run(debug=True, host=MOCK_HOST, port=MOCK_PORT)
