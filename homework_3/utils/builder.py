import data
from dataclasses import dataclass


@dataclass
class Company:
    name: str = None
    url_id: int = None
    img_id: int = None
    company_id: int = None


class Builder:

    @staticmethod
    def create_company(api_client, name=None, url_id=None, img_id=None, img_path=None):

        if name is None:
            name = data.get_random_string()

        if url_id is None:
            url_id = api_client.get_url_company(ad_url='https://target.my.com/campaign/new')

        if img_id is None:
            img_id = api_client.post_upload_image_company(path=img_path)

        return Company(name=name, url_id=url_id, img_id=img_id)
