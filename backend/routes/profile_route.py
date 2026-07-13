from flask import Blueprint, jsonify, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from services.profile_service import (
    get_profile,
    update_profile
)

profile_bp = Blueprint(
    "profile",
    __name__
)


# ------------------------- Get Profile -------------------------

@profile_bp.route(
    "/profile",
    methods=["GET"]
)
@jwt_required()
def get_profile_api():

    user_id = int(
        get_jwt_identity()
    )

    response, status_code = get_profile(
        user_id
    )

    return jsonify(response), status_code


# ------------------------- Update Profile -------------------------

@profile_bp.route(
    "/profile",
    methods=["PUT"]
)
@jwt_required()
def update_profile_api():

    user_id = int(
        get_jwt_identity()
    )

    data = request.get_json()

    response, status_code = update_profile(
        user_id,
        data
    )

    return jsonify(response), status_code