import sqlalchemy
from sqlalchemy import inspect
from sql_models.models import Base
from sqlalchemy.orm import sessionmaker


class MysqlClient:

    def __init__(self, user='root', password='pass', db_name='test_db', table_name='test_users'):
        self.user = user
        self.password = password
        self.db_name = db_name
        self.table_name = table_name

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
        # self.execute_query("CREATE USER 'test_qa' IDENTIFIED BY 'qa_test';", fetch=False)
        # self.execute_query("GRANT ALL PRIVILEGES ON * . * TO 'test_qa';", fetch=False)
        # self.execute_query("FLUSH PRIVILEGES;", fetch=False)
        self.connection.close()

    def create_base_table(self):
        if not inspect(self.engine).has_table(self.table_name):
            Base.metadata.tables[self.table_name].create(self.engine)
