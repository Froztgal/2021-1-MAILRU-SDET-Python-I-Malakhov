import data
import pytest
from tests_api.base import ApiBase


class CompanyBase(ApiBase):

    @pytest.fixture(scope='function')
    def company(self):
        name = data.get_random_string()
        company_id = self.api_client.post_create_company(name=name)
        yield company_id
        self.api_client.post_delete_company(company_id)
        self.api_client.get_check_company(company_id)


@pytest.mark.API
class TestCompany(CompanyBase):

    @pytest.mark.API
    def test_company_creation(self, company):
        assert self.api_client.get_check_company(company) == 200


@pytest.mark.API
class TestSegments(ApiBase):

    @pytest.mark.API
    def test_segment_creation(self):
        name = data.get_random_string()
        res = self.api_client.post_create_segment(name)
        assert self.api_client.get_check_segment(res) == 200

    @pytest.mark.API
    def test_segment_creation(self):
        name = data.get_random_string()
        res = self.api_client.post_create_segment(name)
        assert self.api_client.get_check_segment(res) == 200
        assert self.api_client.post_delete_segment(res) == 200
