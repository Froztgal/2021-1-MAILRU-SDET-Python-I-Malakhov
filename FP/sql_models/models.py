from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TestUsers(Base):
    __test__ = False
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<TestUsers(" \
               f"id='{self.id}'," \
               f"username='{self.username}', " \
               f"password='{self.password}', " \
               f"email='{self.email}', " \
               f"access='{self.access}', " \
               f"active='{self.active}', " \
               f"start_active_time='{self.start_active_time}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(16))
    password = Column(String(255), nullable=False)
    email = Column(String(64), nullable=False)
    access = Column(Integer)
    active = Column(Integer)
    start_active_time = Column(DateTime)
