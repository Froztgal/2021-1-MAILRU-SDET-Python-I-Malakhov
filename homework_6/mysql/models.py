from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TypeReq(Base):
    __tablename__ = 'type_req'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TypeReq(" \
               f"id='{self.id}'," \
               f"type='{self.type_req}', " \
               f"count='{self.count}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_req = Column(String(300), nullable=False)
    count = Column(Integer, nullable=False)


class MostCommon(Base):
    __tablename__ = 'most_common'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<MostCommon(" \
               f"id='{self.id}'," \
               f"url='{self.url}', " \
               f"count='{self.count}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(100), nullable=False)
    count = Column(Integer, nullable=False)


class Biggest4xx(Base):
    __tablename__ = 'biggest_4xx'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Biggest4xx(" \
               f"id='{self.id}', " \
               f"bytessent='{self.bytessent}', " \
               f"url='{self.url}', " \
               f"ipaddress='{self.ipaddress}', " \
               f"statuscode='{self.statuscode}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bytessent = Column(Integer, nullable=False)
    url = Column(String(300), nullable=False)
    ipaddress = Column(String(16), nullable=False)
    statuscode = Column(Integer, nullable=False)


class Top5xx(Base):
    __tablename__ = 'top5_5xx'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Top5xx(" \
               f"id='{self.id}', " \
               f"ipaddress='{self.ipaddress}', " \
               f"count='{self.count}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ipaddress = Column(String(16), nullable=False)
    count = Column(Integer, nullable=False)

