import os
import time
import signal
import requests
import settings
import subprocess
from copy import copy
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


def start_app(config):
    app_path = os.path.join(repo_root, 'app', 'app.py')

    app_out = open('/tmp/app_stdout.log', 'w')
    app_err = open('/tmp/app_stderr.log', 'w')

    env = copy(os.environ)
    env['APP_HOST'] = settings.App.HOST
    env['APP_PORT'] = settings.App.PORT

    env['STUB_HOST'] = settings.Stub.HOST
    env['STUB_PORT'] = settings.Stub.PORT

    env['MOCK_HOST'] = settings.Mock.HOST
    env['MOCK_PORT'] = settings.Mock.PORT

    proc = subprocess.Popen(['python3.8', app_path], stdout=app_out, stderr=app_err, env=env)

    config.app_proc = proc
    config.app_out = app_out
    config.app_err = app_err

    waiter(settings.App.HOST, settings.App.PORT)


def start_stub(config):
    # stub_path = os.path.join(repo_root, 'stub', 'flask_stub.py')
    stub_path = os.path.join(repo_root, 'stub', 'simple_http_server_stub.py')

    stub_out = open('/tmp/stub_stdout.log', 'w')
    stub_err = open('/tmp/stub_stderr.log', 'w')

    env = copy(os.environ)
    env['STUB_HOST'] = settings.Stub.HOST
    env['STUB_PORT'] = settings.Stub.PORT

    proc = subprocess.Popen(['python3.8', stub_path], stdout=stub_out, stderr=stub_err, env=env)

    config.stub_proc = proc
    config.stub_out = stub_out
    config.stub_err = stub_err

    waiter(settings.Stub.HOST, settings.Stub.PORT)


def start_mock():

    flask_mock.run_mock()

    waiter(settings.Mock.HOST, settings.Mock.PORT)


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        start_mock()
        start_stub(config)
        start_app(config)


def stop_app(config):
    config.app_proc.send_signal(signal.SIGINT)
    exit_code = config.app_proc.wait()

    config.app_out.close()
    config.app_err.close()

    assert exit_code == 0


def stop_stub(config):
    config.stub_proc.send_signal(signal.SIGINT)
    config.stub_proc.wait()

    config.stub_out.close()
    config.stub_err.close()


def stop_mock():
    requests.get(f'http://{settings.Mock.HOST}:{settings.Mock.PORT}/shutdown')


def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        stop_app(config)
        stop_stub(config)
        stop_mock()
