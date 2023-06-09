import pytest
from app import app

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
