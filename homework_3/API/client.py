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

    def post_create_company(self, name):

        location = '/api/v2/campaigns.json'
        url = self._make_url(location)

        headers = {'X-CSRFToken': self.session.cookies.get('csrftoken')}

        data = '{"name": "' + f'{name}", ' + """
                    "conversion_funnel_id":null,"objective":"traffic",
                    "enable_offline_goals":false,"targetings":{
                    "split_audience":[1,2,3,4,5,6,7,8,9,10],"sex":["male",
                    "female"],"age":{"age_list":[0,12,13,14,15,16,17,18,19,
                    20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,
                    39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,
                    58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75],
                    "expand":true},"geo":{"regions":[188]},
                    "interests_soc_dem":[],"segments":[],"interests":[],
                    "fulltime":{"flags":["use_holidays_moving",
                    "cross_timezone"],"mon":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,
                    14,15,16,17,18,19,20,21,22,23],"tue":[0,1,2,3,4,5,6,7,8,
                    9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],"wed":[0,1,
                    2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,
                    23],"thu":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,
                    18,19,20,21,22,23],"fri":[0,1,2,3,4,5,6,7,8,9,10,11,12,
                    13,14,15,16,17,18,19,20,21,22,23],"sat":[0,1,2,3,4,5,6,7,
                    8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],"sun":[0,
                    1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,
                    23]},"pads":[102643],"mobile_types":["tablets",
                    "smartphones"],"mobile_vendors":[],"mobile_operators":[
                    ]},"age_restrictions":null,"date_start":null,
                    "date_end":null,"autobidding_mode":"second_price_mean",
                    "budget_limit_day":null,"budget_limit":null,
                    "mixing":"fastest","utm":null,"enable_utm":true,
                    "price":"17.11","max_price":"0","package_id":961,
                    "banners":[{"urls":{"primary":{"id":14570324}},
                    "textblocks":{},"content":{"image_240x400":{
                    "id":8652017}},"name":""}]}
                    """

        result = self.session.post(url, headers=headers, json=json.loads(data))

        return json.loads(result.content.decode('utf-8'))['id']

    def get_check_company(self, company_id):

        location = f'/api/v2/campaigns/{company_id}.json'
        url = self._make_url(location)

        headers = {'X-CSRFToken': self.session.cookies.get('csrftoken')}

        result = self.session.get(url, headers=headers)

        return result.status_code

    def post_delete_company(self, company_id):

        location = '/api/v2/campaigns/mass_action.json'
        url = self._make_url(location)

        headers = {'X-CSRFToken': self.session.cookies.get('csrftoken')}

        data = [{"id": company_id, "status": "deleted"}]

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
            'relations': [{'object_type': 'remarketing_player',
                           'params': {'type': 'positive', 'left': 365,
                                      'right': 0}}]
        }

        result = self.session.post(url, headers=headers, json=data)
        self._response_check(result)
        return json.loads(result.content.decode('utf-8'))['id']

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
