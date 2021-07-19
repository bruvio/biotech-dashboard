import os
import sys

import pytest
from src.app import server as flask_app

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


@pytest.fixture(scope="module")
def app():
    yield flask_app


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()
