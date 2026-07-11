from flask import Blueprint, jsonify, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity

    
)

from services.staff_service import (
    get_profile,
    update_profile,
    get_dashboard_statistics,
    get_my_treks,
    update_trek_capacity,
    update_trek_status,
    get_participants
)

staff_bp = Blueprint(
    "staff",
    __name__
)


#-------------------------Get Own Profile-------------------------

@staff_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile_api():

    claims = get_jwt()

    if claims["role"] != "staff":

        return jsonify({

            "message": "Staff access required."

        }),403

    user_id = get_jwt_identity()

    response, status = get_profile(user_id)

    return jsonify(response), status


#-------------------------Complete Profile-------------------------

@staff_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile_api():

    claims = get_jwt()

    if claims["role"] != "staff":

        return jsonify({

            "message": "Staff access required."

        }),403

    user_id = get_jwt_identity()

    data = request.get_json()

    response, status = update_profile(

        user_id,

        data

    )

    return jsonify(response), status

#----------------------Dashboard Statistics----------------------

@staff_bp.route("/dashboard",methods=["GET"])
@jwt_required()
def dashboard_statistics_api():

    claims=get_jwt()

    if claims["role"]!="staff":

        return{

            "message":"Staff access required."

        },403

    user_id=get_jwt_identity()

    response,status=get_dashboard_statistics(

        user_id

    )

    return jsonify(response),status

#-----------------------------my treks-----------------------------

@staff_bp.route("/my-treks", methods=["GET"])
@jwt_required()
def get_my_treks_api():

    claims = get_jwt()

    if claims["role"] != "staff":

        return {
            "message":"Staff access required."
        },403

    user_id = get_jwt_identity()

    response,status = get_my_treks(user_id)

    return jsonify(response),status

#-----------------------update slots-----------------------

@staff_bp.route("/trek/<int:trek_id>/capacity", methods=["PUT"])
@jwt_required()
def update_slots_api(trek_id):

    claims = get_jwt()

    if claims["role"] != "staff":

        return jsonify({
            "message":"Staff access required."
        }),403

    user_id = get_jwt_identity()

    response,status = update_trek_slots(
        user_id,
        trek_id,
        request.get_json()
    )

    return jsonify(response),status

#-----------------------update trek status-----------------------

@staff_bp.route("/trek/<int:trek_id>/status", methods=["PUT"])
@jwt_required()
def update_status_api(trek_id):

    claims = get_jwt()

    if claims["role"]!="staff":

        return jsonify({
            "message":"Staff access required."
        }),403

    user_id=get_jwt_identity()

    response,status=update_trek_status(

        user_id,

        trek_id,

        request.get_json()

    )

    return jsonify(response),status

#-----------------------participants-----------------------

@staff_bp.route("/participants", methods=["GET"])
@jwt_required()
def get_participants_api():

    claims = get_jwt()

    if claims["role"] != "staff":

        return jsonify({
            "message": "Staff access required."
        }), 403

    user_id = get_jwt_identity()

    response, status = get_participants(user_id)

    return jsonify(response), status