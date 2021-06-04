import allure
import logging
import requests
from urllib.parse import urljoin

logger = logging.getLogger('test')


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

    @allure.step('POST login with username: {username},  password: {password}')
    def post_login(self, username, password):

        location = '/login'
        url = self._make_url(location)

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        data = {
            'username': username,
            'password': password,
            'submit': 'Login'
        }

        logger.info(f'POST {data} with headers {headers} in {url}...')
        result = self.session.post(url, headers=headers, data=data, allow_redirects=False)
        logger.info(f'Response on post_login request got {result.status_code} status code, expected status codes were '
                    f'201 or 302.')
        self.cookies = result.headers['Set-Cookie'].split(';')[0]

        return result

    @allure.step('GET logout')
    def get_logout(self):

        location = '/logout'
        url = self._make_url(location)

        logger.info(f'GET request to {url}...')
        result = self.session.get(url)
        logger.info(f'Response on get_logout request got {result.status_code} status code, expected status code '
                    f'was 200.')

        return result

    @allure.step('POST add user with username: {username},  password: {password}, email: {email}')
    def post_add_user(self, username, password, email):

        location = '/api/add_user'
        url = self._make_url(location)

        data = {
            'username': username,
            'password': password,
            'email': email
        }

        logger.info(f'POST {data} in {url}...')
        result = self.session.post(url, headers=self.base_headers, json=data)
        logger.info(f'Response on post_add_user request got {result.status_code} status code, expected status code '
                    f'was 201 or 304.')

        return result

    @allure.step('GET del user {username}')
    def get_del_user(self, username):

        location = f'/api/del_user/{username}'
        url = self._make_url(location)

        logger.info(f'GET request to {url}...')
        result = self.session.get(url)
        logger.info(f'Response on get_del_user request got {result.status_code} status code, expected status code '
                    f'was 204 or 404.')

        return result

    @allure.step('GET block user {username}')
    def get_block_user(self, username):

        location = f'/api/block_user/{username}'
        url = self._make_url(location)

        logger.info(f'GET request to {url}...')
        result = self.session.get(url)
        logger.info(f'Response on get_block_user request got {result.status_code} status code, expected status code '
                    f'was 200 or 404.')

        return result

    @allure.step('GET unblock user {username}')
    def get_unblock_user(self, username):

        location = f'/api/accept_user/{username}'
        url = self._make_url(location)

        logger.info(f'GET request to {url}...')
        result = self.session.get(url)
        logger.info(f'Response on get_unblock_user request got {result.status_code} status code, expected status code '
                    f'was 200 or 404.')

        return result

    @allure.step('GET app status')
    def get_app_status(self):

        location = f'/status'
        url = self._make_url(location)

        logger.info(f'GET request to {url}...')
        result = self.session.get(url)
        logger.info(f'Response on get_app_status request got {result.status_code} status code, expected status code '
                    f'was 200.')

        return result
