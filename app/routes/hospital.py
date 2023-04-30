from flask import Blueprint, request, jsonify
from app.models.hospital import Hospital, Shift
from app.models.nurse import HospitalShift, Nurse
from app.models.mediator import Mediator
from app.utils.auth import mediator_required

hospital_routes = Blueprint('hospital', __name__)

@hospital_routes.route('/shifts', methods=['POST'])
@mediator_required
def post_shift():
    data = request.get_json()
    hospital = Hospital.objects(name=data['hospital_name']).first()
    if not hospital:
        return jsonify({'message': 'Hospital not found'}), 404

    shift = Shift(
        date=data['date'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        price_per_hour=data['price_per_hour']
    )

    hospital.shifts.append(shift)
    hospital.save()

    return jsonify({'message': 'Shift created successfully'})

@hospital_routes.route('/shifts', methods=['GET'])
@mediator_required
def get_shifts():
    hospital = Hospital.objects(name=request.args.get('hospital_name')).first()
    if not hospital:
        return jsonify({'message': 'Hospital not found'}), 404

    shifts = [shift.to_dict() for shift in hospital.shifts]

    return jsonify({'shifts': shifts})

@hospital_routes.route('/shifts/<shift_id>/applicants', methods=['GET'])
@mediator_required
def get_applicants(shift_id):
    hospital_shift = HospitalShift.objects(id=shift_id).first()
    if not hospital_shift:
        return jsonify({'message': 'Shift not found'}), 404

    applicants = [nurse.to_dict() for nurse in Nurse.objects(shifts=hospital_shift)]

    return jsonify({'applicants': applicants})

@hospital_routes.route('/shifts/<shift_id>/select', methods=['POST'])
@mediator_required
def select_nurse(shift_id):
    data = request.get_json()
    nurse = Nurse.objects(id=data['nurse_id']).first()
    if not nurse:
        return jsonify({'message': 'Nurse not found'}), 404

    hospital_shift = HospitalShift.objects(id=shift_id).first()
    if not hospital_shift:
        return jsonify({'message': 'Shift not found'}), 404

    if hospital_shift.selected_nurse:
        return jsonify({'message': 'Nurse already selected for this shift'}), 400

    hospital_shift.selected_nurse = nurse
    hospital_shift.save()

    return jsonify({'message': 'Nurse selected successfully'})
