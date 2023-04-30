import json
import pytest
from app import app, mongo

@pytest.fixture(scope='module')
def hospital():
    # Set up a hospital user for testing
    hospital = {
        'name': 'Test Hospital',
        'email': 'testhospital@example.com',
        'password': 'testpassword'
    }
    mongo.db.hospitals.insert_one(hospital)
    return hospital

def test_hospital_registration(test_client):
    # Test hospital registration
    response = test_client.post('/auth/hospital/register', data=json.dumps({
        'name': 'New Hospital',
        'email': 'newhospital@example.com',
        'password': 'testpassword'
    }), content_type='application/json')
    assert response.status_code == 200

def test_hospital_login(test_client, hospital):
    # Test hospital login
    response = test_client.post('/auth/hospital/login', data=json.dumps({
        'email': hospital['email'],
        'password': hospital['password']
    }), content_type='application/json')
    assert response.status_code == 200

def test_create_shift(test_client, hospital):
    # Test creating a shift for a hospital
    response = test_client.post('/hospitals/shifts', headers={
        'Authorization': f'Bearer {hospital["access_token"]}'
    }, data=json.dumps({
        'location': 'Test Location',
        'time': '2:00 PM',
        'date': '2023-05-01',
        'price': 50.00
    }), content_type='application/json')
    assert response.status_code == 200
