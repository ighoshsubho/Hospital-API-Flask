import json
import pytest
from app import app, mongo

@pytest.fixture(scope='module')
def nurse():
    # Set up a nurse user for testing
    nurse = {
        'name': 'Test Nurse',
        'email': 'testnurse@example.com',
        'password': 'testpassword'
    }
    mongo.db.nurses.insert_one(nurse)
    return nurse

@pytest.fixture(scope='module')
def hospital():
    # Set up a hospital for testing
    hospital = {
        'name': 'Test Hospital',
        'email': 'testhospital@example.com',
        'password': 'testpassword'
    }
    mongo.db.hospitals.insert_one(hospital)
    return hospital

@pytest.fixture(scope='module')
def shift(hospital):
    # Set up a shift for testing
    shift = {
        'hospital_id': hospital['_id'],
        'location': 'Test Location',
        'time': '2:00 PM',
        'date': '2023-05-01',
        'price': 50.00,
        'status': 'open'
    }
    mongo.db.shifts.insert_one(shift)
    return shift

def test_nurse_registration(test_client):
    # Test nurse registration
    response = test_client.post('/auth/nurse/register', data=json.dumps({
        'name': 'New Nurse',
        'email': 'newnurse@example.com',
        'password': 'testpassword'
    }), content_type='application/json')
    assert response.status_code == 200

def test_nurse_login(test_client, nurse):
    # Test nurse login
    response = test_client.post('/auth/nurse/login', data=json.dumps({
        'email': nurse['email'],
        'password': nurse['password']
    }), content_type='application/json')
    assert response.status_code == 200

def test_get_shifts(test_client, nurse, shift):
    # Test getting a list of open shifts
    response = test_client.get('/nurses/shifts', headers={
        'Authorization': f'Bearer {nurse["access_token"]}'
    })
    assert response.status_code == 200
    assert len(response.json['shifts']) == 1

def test_apply_for_shift(test_client, nurse, shift):
    # Test a nurse applying for a shift
    response = test_client.post(f'/nurses/shifts/{str(shift["_id"])}/apply', headers={
        'Authorization': f'Bearer {nurse["access_token"]}'
    })
    assert response.status_code == 200

def test_select_nurse(test_client, hospital, shift, nurse):
    # Test a hospital selecting a nurse for a shift
    response = test_client.post(f'/hospitals/shifts/{str(shift["_id"])}/select', headers={
        'Authorization': f'Bearer {hospital["access_token"]}'
    }, data=json.dumps({
        'nurse_id': str(nurse["_id"])
    }), content_type='application/json')
    assert response.status_code == 200
    assert response.json['shift']['status'] == 'closed'
    assert response.json['shift']['nurse_id'] == str(nurse["_id"])
