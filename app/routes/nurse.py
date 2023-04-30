from flask import Blueprint, request, jsonify
from app.models.nurse import Nurse, HospitalShift
from app.models.hospital import Shift, Hospital
from app.utils.auth import nurse_required

nurse_routes = Blueprint('nurse', __name__)

@nurse_routes.route('/shifts', methods=['GET'])
@nurse_required
def get_shifts():
    shifts = []
    for hospital_shift in HospitalShift.objects():
        if not hospital_shift.selected_nurse:
            shifts.append(hospital_shift.to_dict())

    return jsonify({'shifts': shifts})

@nurse_routes.route('/shifts/<shift_id>/apply', methods=['POST'])
@nurse_required
def apply_for_shift(shift_id):
    nurse = Nurse.objects(id=request.user.id).first()
    if not nurse:
        return jsonify({'message': 'Nurse not found'}), 404

    hospital_shift = HospitalShift.objects(id=shift_id).first()
    if not hospital_shift:
        return jsonify({'message': 'Shift not found'}), 404

    if hospital_shift.selected_nurse:
        return jsonify({'message': 'Nurse already selected for this shift'}), 400

    if hospital_shift in nurse.shifts:
        return jsonify({'message': 'Nurse already applied for this shift'}), 400

    nurse.shifts.append(hospital_shift)
    nurse.save()

    return jsonify({'message': 'Applied successfully'})