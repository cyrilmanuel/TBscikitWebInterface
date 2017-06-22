import pytest
from flask import url_for

from interfaceMl.interfaceMl import create_app

@pytest.fixture
def app():
    app = create_app()
    return app


def test_index(client):
    res = client.get(url_for('index'))
    assert res.status_code == 200


def test_test(client):
    res = client.get(url_for('usescikit'))
    assert res.status_code == 200
