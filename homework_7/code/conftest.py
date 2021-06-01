import os
import time
import requests
import settings
from mock import flask_mock
from requests.exceptions import ConnectionError


repo_root = os.path.abspath(os.path.join(__file__, os.pardir))  # code


def waiter(host, port, timeout=5):
    started = False
    st = time.time()
    while time.time() - st <= timeout:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass
    if not started:
        raise RuntimeError(f'App did not started in {timeout} s!')


def start_mock():
    flask_mock.run_mock()
    waiter(settings.Mock.HOST, settings.Mock.PORT)


def stop_mock():
    requests.get(f'http://{settings.Mock.HOST}:{settings.Mock.PORT}/shutdown')


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        start_mock()


def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        stop_mock()
