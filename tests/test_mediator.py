import json
import pytest
from app import app, mongo

@pytest.fixture(scope='module')
def mediator():
    # Set up a mediator user for testing
    mediator = {
        'name': 'Test Mediator',
        'email': 'testmediator@example.com',
        'password': 'testpassword'
    }
    mongo.db.mediators.insert_one(mediator)
    return mediator

def test_mediator_registration(test_client):
    # Test mediator registration
    response = test_client.post('/auth/mediator/register', data=json.dumps({
        'name': 'New Mediator',
        'email': 'newmediator@example.com',
        'password': 'testpassword'
    }), content_type='application/json')
    assert response.status_code == 200

def test_mediator_login(test_client, mediator):
    # Test mediator login
    response = test_client.post('/auth/mediator/login', data=json.dumps({
        'email': mediator['email'],
        'password': mediator['password']
    }), content_type='application/json')
    assert response.status_code == 200

def test_create_hospital(test_client, mediator):
    # Test creating a hospital for a mediator
    response = test_client.post('/mediators/hospitals', headers={
        'Authorization': f'Bearer {mediator["access_token"]}'
    }, data=json.dumps({
        'name': 'Test Hospital',
        'email': 'testhospital@example.com',
        'password': 'testpassword'
    }), content_type='application/json')
    assert response.status_code == 200
