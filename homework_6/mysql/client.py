import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from mysql.models import Base


class MysqlClient:

    def __init__(self, user, password, db_name):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = '127.0.0.1'
        self.port = 3306

        self.engine = None
        self.connection = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''

        self.engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}',
            encoding='utf8'
        )
        self.connection = self.engine.connect()
        self.session = sessionmaker(bind=self.connection.engine,
                                    autocommit=False,  # use autocommit on session.add
                                    expire_on_commit=False  # expire model after commit (requests data from database)
                                    )()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def recreate_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database if exists {self.db_name}', fetch=False)
        self.execute_query(f'CREATE database {self.db_name}', fetch=False)
        self.connection.close()

    def create_count_req(self):
        if not inspect(self.engine).has_table('count_req'):
            Base.metadata.tables['count_req'].create(self.engine)

    def create_type_req(self):
        if not inspect(self.engine).has_table('type_req'):
            Base.metadata.tables['type_req'].create(self.engine)

    def create_most_common(self):
        if not inspect(self.engine).has_table('most_common'):
            Base.metadata.tables['most_common'].create(self.engine)

    def create_biggest_4xx(self):
        if not inspect(self.engine).has_table('biggest_4xx'):
            Base.metadata.tables['biggest_4xx'].create(self.engine)

    def create_top5_5xx(self):
        if not inspect(self.engine).has_table('top5_5xx'):
            Base.metadata.tables['top5_5xx'].create(self.engine)
