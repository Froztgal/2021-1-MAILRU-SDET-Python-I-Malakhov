import pytest
from utils.builder import Builder


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, credentials):
        self.builder = Builder()
        self.api_client = api_client
        if self.authorize:
            self.api_client.post_login(*credentials)
