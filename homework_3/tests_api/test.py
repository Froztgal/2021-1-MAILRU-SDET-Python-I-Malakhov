import os
import data
import pytest
from tests_api.base import ApiBase
from utils.builder import Builder as CompanyBuilder


class CompanyBase(ApiBase):

    @pytest.fixture(scope='function')
    def file_path_img(self, repo_root):
        return os.path.join(repo_root, 'ui', 'test_img.jpg')

    @pytest.fixture(scope='function')
    def file_path_json(self, repo_root):
        return os.path.join(repo_root, 'API', 'company_template.json')

    @pytest.fixture(scope='function')
    def company(self, file_path_img, file_path_json):
        new_company = CompanyBuilder().create_company(self.api_client, img_path=file_path_img)
        new_company.company_id = self.api_client.post_create_company(new_company, path_json=file_path_json)
        yield new_company
        self.api_client.post_delete_company(new_company)
        self.api_client.get_check_company(new_company)


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
