from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required , get_jwt, get_jwt_identity

from services.user_service import dashboard_statistics, browse_treks, book_trek


user_bp = Blueprint("user", __name__)

# ---------------------- Dashboard Statistics ----------------------

@user_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard_statistics_api():
    print("Dashboard API called")

    user_id = get_jwt_identity()
    print(user_id)

    response, status_code = dashboard_statistics(user_id)

    return jsonify(response), status_code

# ------------------------- Browse Treks -------------------------

@user_bp.route("/treks", methods=["GET"])
@jwt_required()
def browse_treks_api():
    print("Browse Treks API called")

    response, status_code = browse_treks()

    return jsonify(response), status_code


# ------------------------- Book Trek -------------------------

@user_bp.route("/treks/<int:trek_id>/book", methods=["POST"])
@jwt_required()
def book_trek_api(trek_id):

    user_id = get_jwt_identity()

    response, status_code = book_trek(
        int(user_id),
        trek_id
    )

    return jsonify(response), status_code
