import json
import requests
from urllib.parse import urljoin


class ResponseErrorException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class InvalidLoginException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.auth_url = 'https://auth-ac.my.com/auth'
        self.session = requests.Session()

    def _make_url(self, location):
        return urljoin(self.base_url, location)

    def _response_check(self, response, expected_status=200, jsonify=True):

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} '
                                              f'{response.reason} for URL '
                                              f'"{response.url}"!\n'f'Expected status_code: {expected_status}.')

        if jsonify:
            json_response = response.json()
            if json_response.get('bStateError'):
                error = json_response.get('bErrorMsg', 'Unknown')
                raise ResponseErrorException(f'Request "{response.url}" '
                                             f'return error "{error}"!')
        return True

    def post_login(self, user, password):

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://target.my.com/'
        }

        data = {
            'email': user,
            'password': password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login'
                        '%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }

        result = self.session.post(self.auth_url, headers=headers, data=data)
        self._response_check(result, jsonify=False)
        self.get_token()

        return result

    def get_token(self):

        location = '/csrf/'
        url = self._make_url(location)

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        result = self.session.get(url, headers=headers)
        self._response_check(result, jsonify=False)

    def get_url_company(self, ad_url):

        location = '/api/v1/urls/'
        url = self._make_url(location)

        data = {'url': ad_url}

        result = self.session.get(url, params=data)
        self._response_check(result)

        return result.json()['id']

    def post_upload_image_company(self, path):

        location = '/api/v2/content/static.json'
        url = self._make_url(location)

        headers = {'X-CSRFToken': self.session.cookies.get('csrftoken')}

        files = {"file": open(path, "rb")}

        result = self.session.post(url, headers=headers, files=files)
        self._response_check(result)

        img_id = result.json()['id']

        location = '/api/v2/mediateka.json'
        url = self._make_url(location)

        data = {
            "description": "test_img.jpg",
            "content": {"id": img_id}
        }

        self.session.post(url, headers=headers, json=data)

        return img_id

    def post_create_company(self, company, path_json):

        location = '/api/v2/campaigns.json'
        url = self._make_url(location)

        headers = {'X-CSRFToken': self.session.cookies.get('csrftoken')}

        with open(path_json, 'r') as f:
            data = json.loads(f.read())

        data['name'] = company.name
        data['banners'][0]['content']['image_240x400']['id'] = company.img_id
        data['banners'][0]['urls']['primary']['id'] = company.url_id

        result = self.session.post(url, headers=headers, json=data)
        self._response_check(result)

        return result.json()['id']

    def get_check_company(self, company):

        location = f'/api/v2/campaigns/{company.company_id}.json'
        url = self._make_url(location)

        headers = {'X-CSRFToken': self.session.cookies.get('csrftoken')}

        result = self.session.get(url, headers=headers)

        return result.status_code

    def post_delete_company(self, company):

        location = '/api/v2/campaigns/mass_action.json'
        url = self._make_url(location)

        headers = {'X-CSRFToken': self.session.cookies.get('csrftoken')}

        data = [{"id": company.company_id, "status": "deleted"}]

        result = self.session.post(url, headers=headers, json=data)
        self._response_check(result, expected_status=204, jsonify=False)

        return result.status_code

    def post_create_segment(self, name):

        location = '/api/v2/remarketing/segments.json'
        url = self._make_url(location)

        headers = {'X-CSRFToken': self.session.cookies.get('csrftoken')}

        data = {
            'logicType': "or",
            'name': name,
            'pass_condition': 1,
            'relations': [{'object_type': 'remarketing_player', 'params': {'type': 'positive', 'left': 365,
                                                                           'right': 0}}]
        }

        result = self.session.post(url, headers=headers, json=data)
        self._response_check(result)
        return result.json()['id']

    def get_check_segment(self, segment_id):

        location = f'/api/v2/remarketing/segments/{segment_id}/relations.json'
        url = self._make_url(location)

        headers = {'X-CSRFToken': self.session.cookies.get('csrftoken')}

        result = self.session.get(url, headers=headers)

        return result.status_code

    def post_delete_segment(self, segment_id):

        location = '/api/v1/remarketing/mass_action/delete.json'
        url = self._make_url(location)

        headers = {'X-CSRFToken': self.session.cookies.get('csrftoken')}

        data = [{"source_id": segment_id, "source_type": "segment"}]

        result = self.session.post(url, headers=headers, json=data)
        self._response_check(result)

        return result.status_code
