import jwt
from functools import wraps
from flask import request, jsonify
from app.models.nurse import Nurse
from app.models.mediator import Mediator
from app.models.hospital import Hospital

def login_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                auth_header = request.headers.get('Authorization')
                token = auth_header.split(' ')[1]
                data = jwt.decode(token, 'mysecretkey', algorithms=['HS256'])
                user_id = data['sub']
                user_role = data['role']
                if user_role != role:
                    raise Exception('Unauthorized user')
                if role == 'nurse':
                    user = Nurse.objects(id=user_id).first()
                elif role == 'mediator':
                    user = Mediator.objects(id=user_id).first()
                elif role == 'hospital':
                    user = Hospital.objects(id=user_id).first()
                else:
                    raise Exception('Invalid user role')
                if not user:
                    raise Exception('User not found')
                request.user = user
            except Exception as e:
                return jsonify({'message': str(e)}), 401
            return func(*args, **kwargs)
        return wrapper
    return decorator

nurse_required = login_required('nurse')
mediator_required = login_required('mediator')
hospital_required = login_required('hospital')
