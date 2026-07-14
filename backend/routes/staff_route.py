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
    get_trek_participants,
    update_participant,
    get_participant_details,
    get_all_assigned_participants,
    
    
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
    
    search = request.args.get("search","").strip()

    user_id = get_jwt_identity()

    response,status = get_my_treks(user_id, search)

    return jsonify(response),status

#-----------------------update slots-----------------------

@staff_bp.route("/treks/<int:trek_id>/capacity", methods=["PUT"])
@jwt_required()
def update_slots_api(trek_id):

    claims = get_jwt()

    if claims["role"] != "staff":

        return jsonify({
            "message":"Staff access required."
        }),403

    user_id = get_jwt_identity()

    response,status = update_trek_capacity(
        user_id,
        trek_id,
        request.get_json()
    )

    return jsonify(response),status

#-----------------------update trek status-----------------------

@staff_bp.route("/treks/<int:trek_id>/status", methods=["PUT"])
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

#-----------------------get trek participants-----------------------

@staff_bp.route("/treks/<int:trek_id>/participants", methods=["GET"])
@jwt_required()
def get_trek_participants_api(trek_id):

    claims = get_jwt()

    if claims["role"] != "staff":

        return jsonify({
            "message": "Staff access required."
        }), 403
    
    search = request.args.get("search","").strip()

    user_id = get_jwt_identity()

    response, status = get_trek_participants(user_id, trek_id, search)

    return jsonify(response), status
#----------------------- trek participants details-----------------------

@staff_bp.route("/participants/<int:booking_id>", methods=["GET"])
@jwt_required()
def get_participant_details_api(booking_id):

    claims = get_jwt()

    if claims["role"] != "staff":

        return jsonify({
            "message": "Staff access required."
        }), 403

    user_id = get_jwt_identity()

    response, status = get_participant_details(user_id, booking_id)

    return jsonify(response), status

#----------------------- update participants details-----------------------

@staff_bp.route("/participants/<int:booking_id>", methods=["PATCH"])
@jwt_required()
def update_participant_api(booking_id):

    claims = get_jwt()

    if claims["role"] != "staff":

        return jsonify({
            "message": "Staff access required."
        }), 403

    user_id = get_jwt_identity()
    data = request.get_json()

    response, status = update_participant(user_id, booking_id, data)

    return jsonify(response), status

# ---------------------- All Assigned Participants ----------------------

@staff_bp.route(

    "/participants",

    methods=["GET"]

)

@jwt_required()

def get_all_assigned_participants_api():

    claims = get_jwt()

    if claims["role"] != "staff":

        return jsonify({

            "message":"Staff access required."

        }),403

    user_id = get_jwt_identity()

    search = request.args.get("search","").strip()

    response,status = get_all_assigned_participants(

        user_id, search

    )

    return jsonify(response),status
