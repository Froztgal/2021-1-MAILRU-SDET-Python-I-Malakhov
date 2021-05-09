import pytest
from myparser import my_parser
from mysql.builder import MySQLBuilder
from mysql.models import TypeReq, MostCommon, Biggest4xx, Top5xx

parsed_data = my_parser.get_results()

class MySQLBase:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)
        self.prepare()


class TestMysql1(MySQLBase):

    def prepare(self):
        data = parsed_data[1]
        data['All'] = parsed_data[0]
        for k, v in data.items():
            self.type_req = self.mysql_builder.create_type_req(k, v)

    def test_type_req(self):
        assert self.mysql.session.query(TypeReq).filter_by(type_req='POST').first().count == 102504
        assert self.mysql.session.query(TypeReq).filter_by(type_req='All').first().count == 225133


class TestMysql2(MySQLBase):

    def prepare(self):
        data = parsed_data[2]
        for k, v in data.items():
            self.type_req = self.mysql_builder.create_most_common(k, v)

    def test_type_req(self):
        assert self.mysql.session.query(MostCommon).filter_by(id=1).first().count == 103934


class TestMysql3(MySQLBase):

    def prepare(self):
        data = parsed_data[3]
        for k, v in data.items():
            self.type_req = self.mysql_builder.create_biggest_4xx(k, *v)

    def test_biggest_4xx(self):
        assert self.mysql.session.query(Biggest4xx).filter_by(id=1).first().bytessent == 442


class TestMysql4(MySQLBase):

    def prepare(self):
        data = parsed_data[4]
        for k, v in data.items():
            self.type_req = self.mysql_builder.create_top5_5xx(k, v)

    def test_top5_5xx(self):
        assert self.mysql.session.query(Top5xx).filter_by(id=1).first().count == 225
