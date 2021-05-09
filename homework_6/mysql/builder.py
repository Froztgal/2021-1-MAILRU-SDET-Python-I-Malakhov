from mysql.models import TypeReq, MostCommon, Biggest4xx, Top5xx


class MySQLBuilder:

    def __init__(self, client):
        self.client = client

    def create_type_req(self, type_req, count):
        type_req = TypeReq(
            type_req=type_req,
            count=count,
        )
        self.client.session.add(type_req)
        self.client.session.commit()  # no need if sessionmaker autocommit=True
        return type_req

    def create_most_common(self, count, url):
        most_common = MostCommon(
            url=url,
            count=count,
        )
        self.client.session.add(most_common)
        self.client.session.commit()  # no need if sessionmaker autocommit=True
        return most_common

    def create_biggest_4xx(self, bytessent, url, ipaddress, statuscode):
        biggest_4xx = Biggest4xx(
            bytessent=bytessent,
            url=url,
            ipaddress=ipaddress,
            statuscode=statuscode,
        )
        self.client.session.add(biggest_4xx)
        self.client.session.commit()  # no need if sessionmaker autocommit=True
        return biggest_4xx

    def create_top5_5xx(self, count, ipaddress):
        top5_5xx = Top5xx(
            ipaddress=ipaddress,
            count=count,
        )
        self.client.session.add(top5_5xx)
        self.client.session.commit()  # no need if sessionmaker autocommit=True
        return top5_5xx
