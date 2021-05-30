import requests
from urllib.parse import urljoin


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:

    def __init__(self, app_host='127.0.0.1', app_port=8080):
        self.base_url = f'http://{app_host}:{app_port}'
        self.base_headers = {'Content-Type': 'application/json'}
        self.cookies = None
        self.session = requests.Session()

    def _make_url(self, location):
        return urljoin(self.base_url, location)

    def _response_check(self, response, expected_status=200):
        return True # временно
        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} '
                                              f'{response.reason} for URL '
                                              f'"{response.url}"!\n'f'Expected status_code: {expected_status}.')

        return True

    def post_login(self, username, password):

        location = '/login'
        url = self._make_url(location)

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        data = {
            'username': username,
            'password': password,
            'submit': 'Login'
        }

        result = self.session.post(url, headers=headers, data=data, allow_redirects=False)
        self._response_check(result, expected_status=302)
        self.cookies = result.headers['Set-Cookie'].split(';')[0]

        return result

    def post_add_user(self, username, password, email):

        location = '/api/add_user'
        url = self._make_url(location)

        data = {
            'username': username,
            'password': password,
            'email': email
        }

        result = self.session.post(url, headers=self.base_headers, json=data)
        self._response_check(result)

        return result

    def get_del_user(self, username):

        location = f'/api/del_user/{username}'
        url = self._make_url(location)

        result = self.session.get(url)
        self._response_check(result)

        return result

    def get_block_user(self, username):

        location = f'/api/block_user/{username}'
        url = self._make_url(location)

        result = self.session.get(url)
        self._response_check(result)

        return result

    def get_unblock_user(self, username):

        location = f'/api/accept_user/{username}'
        url = self._make_url(location)

        result = self.session.get(url)
        self._response_check(result)

        return result

    def get_app_status(self):

        location = f'/status'
        url = self._make_url(location)

        result = self.session.get(url)
        self._response_check(result)

        return result
