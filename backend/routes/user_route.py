from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required , get_jwt, get_jwt_identity

from services.user_service import dashboard_statistics, browse_treks, book_trek, get_my_bookings, cancel_booking, pay_booking, get_review, submit_review, update_review


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
    search = request.args.get( "search","").strip()

    response, status_code = browse_treks(search)

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

# ------------------------- My Bookings -------------------------

@user_bp.route("/bookings", methods=["GET"])
@jwt_required()
def get_my_bookings_api():

    user_id = int(get_jwt_identity())
    search = request.args.get( "search","").strip()

    response, status_code = get_my_bookings(user_id, search)

    return jsonify(response), status_code

# ------------------------- Cancel Booking -------------------------

@user_bp.route("/bookings/<int:booking_id>/cancel", methods=["PUT"])
@jwt_required()
def cancel_booking_api(booking_id):

    user_id = int(get_jwt_identity())

    response, status_code = cancel_booking(
        user_id,
        booking_id
    )

    return jsonify(response), status_code

# ------------------------- Pay Booking -------------------------

@user_bp.route("/bookings/<int:booking_id>/pay", methods=["PUT"])
@jwt_required()
def pay_booking_api(booking_id):

    user_id = int(get_jwt_identity())

    response, status_code = pay_booking(
        user_id,
        booking_id
    )

    return jsonify(response), status_code

# ------------------------- Submit Review -------------------------

@user_bp.route("/bookings/<int:booking_id>/review", methods=["POST"])
@jwt_required()
def submit_review_api(booking_id):

    user_id = int(get_jwt_identity())

    response, status_code = submit_review(
        user_id,
        booking_id,
        request.get_json()
    )

    return jsonify(response), status_code

# ------------------------- Get Review -------------------------

@user_bp.route("/reviews/<int:trek_id>", methods=["GET"])
@jwt_required()
def get_review_api(trek_id):

    user_id = int(get_jwt_identity())

    response, status_code = get_review(
        user_id,
        trek_id
    )

    return jsonify(response), status_code

# ------------------------- Update Review -------------------------

@user_bp.route("/reviews/<int:trek_id>", methods=["PUT"])
@jwt_required()
def update_review_api(trek_id):

    user_id = int(get_jwt_identity())

    response, status_code = update_review(
        user_id,
        trek_id,
        request.get_json()
    )

    return jsonify(response), status_code

# ---------------- Export Booking History ----------------

@user_bp.route(
    "/export-bookings",
    methods=["POST"]
)
@jwt_required()
def export_booking_history_api():
    from tasks import export_booking_history

    claims = get_jwt()

    if claims["role"] != "trekker":

        return {

            "message": "User access required."

        },403

    user_id = get_jwt_identity()

    export_booking_history.delay(user_id)

    return {

        "message":"Export started. CSV will be sent to your email shortly."

    },202