import sys
import shutil
import logging
from ui.fixtures import *
from docker import DockerClient
from clients.api_client import ApiClient
from clients.db_client import MysqlClient
from clients.socket_http_client import SocketClientHTTP


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--debug_log', action='store_true')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--vnc', action='store_true')
    parser.addoption('--enable_video', action='store_true')


@pytest.fixture(scope='session')
def config(request):
    if request.config.getoption('--selenoid'):
        selenoid = 'http://127.0.0.1:4444'
        if request.config.getoption('--vnc'):
            vnc = True
        else:
            vnc = False
        if request.config.getoption('--enable_video'):
            enable_video = True
        else:
            enable_video = False
    else:
        selenoid = None
        vnc = False
        enable_video = False
    browser = request.config.getoption('--browser')
    debug_log = request.config.getoption('--debug_log')
    enable_video = request.config.getoption('--enable_video')
    return {'browser': browser, 'debug_log': debug_log, 'selenoid': selenoid, 'vnc': vnc, 'enable_video': enable_video}


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_test_dir = 'G:\\Jenkins\\.jenkins\\workspace\\BalkaTest\\FP\\allure-results'
    else:
        base_test_dir = '/tmp/tests'

    if not hasattr(config, 'workerinput'):  # execute only once on main worker
        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)

    mysql_client = MysqlClient()
    mysql_client.recreate_db()
    mysql_client.connect()
    mysql_client.create_base_table()
    mysql_client.connection.close()

    # save to config for all workers
    config.base_test_dir = base_test_dir


@pytest.fixture(scope='function', autouse=True)
def test_dir(request):
    test_name = request._pyfuncitem.nodeid
    prohibitted_chars = '\\/|:*?"<>'
    for char in prohibitted_chars:
        test_name = test_name.replace(char, '_')
    test_dir = os.path.join(request.config.base_test_dir, test_name)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture
def docker_client():
    client = DockerClient()
    yield client
    client.close()


@pytest.fixture
def app_url(docker_client, name='mapp'):
    container = docker_client.containers.get(name)
    base_addr = f'http://{container.attrs["NetworkSettings"]["IPAddress"]}:8080/'
    return base_addr


@pytest.fixture
def socket_client(docker_client):
    client = SocketClientHTTP()
    yield client


@pytest.fixture(scope='session', autouse=True)
def db_client():
    client = MysqlClient()
    client.connect()
    yield client
    client.connection.close()


@pytest.fixture(scope='session', autouse=True)
def my_builder(db_client):
    from builders import MySQLBuilder
    mysql_builder = MySQLBuilder(db_client)
    yield mysql_builder


@pytest.fixture(scope='session', autouse=True)
def api_client():
    client = ApiClient()
    yield client


@pytest.fixture(scope='class', autouse=True)
def clear_table(db_client, my_builder):
    db_client.execute_query('truncate test_users;', False)
    my_builder.create_user('superuser', 'superuser', 'superuser@gmail.com')


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(test_dir, 'test.log')

    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    with open(log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)
