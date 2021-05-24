import pytest
from myparser import my_parser
from mysql.builder import MySQLBuilder
from mysql.models import CountReq, TypeReq, MostCommon, Biggest4xx, Top5xx

parsed_data = my_parser.get_results()


class MySQLBase:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)
        self.prepare()


class TestMysql0(MySQLBase):

    def prepare(self):
        self.count_req = self.mysql_builder.create_count_req('Count', parsed_data[0])

    def test_count_req(self):
        assert self.mysql.session.query(CountReq).count() == 1


class TestMysql1(MySQLBase):

    def prepare(self):
        data = parsed_data[1]
        for k, v in data.items():
            self.type_req = self.mysql_builder.create_type_req(k, v)

    def test_type_req(self):
        assert self.mysql.session.query(TypeReq).count() == len(parsed_data[1])


class TestMysql2(MySQLBase):

    def prepare(self):
        data = parsed_data[2]
        for k, v in data.items():
            self.most_common = self.mysql_builder.create_most_common(k, v)

    def test_most_common(self):
        assert self.mysql.session.query(MostCommon).count() == len(parsed_data[2])


class TestMysql3(MySQLBase):

    def prepare(self):
        data = parsed_data[3]
        for k, v in data.items():
            self.biggest_4xx = self.mysql_builder.create_biggest_4xx(k, *v)

    def test_biggest_4xx(self):
        assert self.mysql.session.query(Biggest4xx).count() == len(parsed_data[3])


class TestMysql4(MySQLBase):

    def prepare(self):
        data = parsed_data[4]
        for k, v in data.items():
            self.top5_5xx = self.mysql_builder.create_top5_5xx(k, v)

    def test_top5_5xx(self):
        assert self.mysql.session.query(Top5xx).count() == len(parsed_data[4])
