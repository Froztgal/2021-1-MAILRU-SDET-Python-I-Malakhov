from dataclasses import dataclass
import data


@dataclass
class Company:
    name: str = None
    url: str = None
    id: int = None


class Builder:

    @staticmethod
    def create_company(name=None, url=None):
        if name is None:
            name = data.get_random_string()

        return Company(name=name)