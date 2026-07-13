import csv
from io import StringIO
from flask import make_response
from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required , get_jwt

from services.admin_service import create_staff , admin_dashboard , get_all_staff , get_staff_details, update_staff_account_status, get_user_details,update_user_account_status, get_all_users, get_user,get_all_bookings, get_booking_details, update_booking, get_reports, export_staff_report, export_booking_report, export_users_report,export_trek_report
from services.staff_service import update_staff, get_staff, staff_assignment , get_available_staff , change_staff_status

admin_bp = Blueprint("admin", __name__)


#-------------------------------create staff------------------------
@admin_bp.route("/staff", methods=["POST"])
@jwt_required()
def create_staff_api():
    claims = get_jwt()

    if claims["role"] != "admin":
        return {
            "message": "Admin access required"
        }, 403
    
    data = request.get_json()

    response, status_code = create_staff(data)

    return jsonify(response), status_code

#------------------------------------admin dashboard----------------------------
@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard_api():
    claims = get_jwt()

    if claims["role"] != "admin":
        return {
            "message": "Only Admin can assign staff."
        }, 403

    response, status_code = admin_dashboard()

    return jsonify(response), status_code     

#----------------------get all staff------------------------

@admin_bp.route("/staff", methods=["GET"])
@jwt_required()
def get_all_staff_api():

    claims = get_jwt()

    if claims["role"] != "admin":

        return {
            "message": "Admin access required."
        }, 403

    response, status_code = get_all_staff()

    return jsonify(response), status_code

#----------------------------update staff-----------------------------

@admin_bp.route("/staff/<int:staff_id>", methods=["PUT"])
@jwt_required()
def update_staff_api(staff_id):

    claims = get_jwt()

    if claims["role"] != "admin":

        return {
            "message": "Admin access required."
        }, 403

    data = request.get_json()

    response, status_code = update_staff(
        staff_id,
        data
    )

    return jsonify(response), status_code

#-----------------------------get a staff----------------------------
@admin_bp.route("/staff/<int:staff_id>", methods=["GET"])
@jwt_required()
def get_staff_api(staff_id):

    claims = get_jwt()

    if claims["role"] != "admin":

        return {
            "message": "Admin access required."
        }, 403

    response, status_code = get_staff(
        staff_id,
    )

    return jsonify(response), status_code

#-----------------------------assign staff----------------------
@admin_bp.route("/staff-assignment", methods=["POST"])
@jwt_required()
def staff_assignment_api():

    claims = get_jwt()

    if claims["role"] != "admin":

        return {
            "message":"Admin access required."
        },403

    data = request.get_json()

    response,status_code = staff_assignment(data)

    return jsonify(response),status_code

#----------------------get available staff-----------------------

@admin_bp.route("/available-staff", methods=["GET"])
@jwt_required()
def get_available_staff_api():

    claims = get_jwt()

    if claims["role"] != "admin":

        return {
            "message": "Admin access required."
        }, 403

    response, status_code = get_available_staff()

    return jsonify(response), status_code

# #----------------------------------change staff status--------------------------
# @admin_bp.route("/staff/<int:staff_id>/status",methods=["PUT"])
# @jwt_required()
# def change_staff_status_api(staff_id):

#     claims=get_jwt()

#     if claims["role"]!="admin":

#         return{

#             "message":"Admin access required."

#         },403

#     data=request.get_json()

#     response,status=change_staff_status(

#         staff_id,

#         data

#     )

#     return jsonify(response),status

#----------------------- Get Staff Details -----------------------

@admin_bp.route("/staff/<int:staff_id>/details", methods=["GET"])
@jwt_required()
def get_staff_details_api(staff_id):

    claims = get_jwt()

    if claims["role"] != "admin":

        return jsonify({

            "message":"Admin access required."

        }),403

    response, status = get_staff_details(

        staff_id

    )

    return jsonify(response), status

#----------------------- Update Staff Account Status -----------------------

@admin_bp.route("/staff/<int:staff_id>/status", methods=["PUT"])
@jwt_required()
def update_staff_account_status_api(staff_id):

    claims = get_jwt()

    if claims["role"] != "admin":

        return jsonify({

            "message":"Admin access required."

        }),403


    response, status = update_staff_account_status(

        staff_id,

        request.get_json()

    )


    return jsonify(response), status

#----------------------- Get User Details -----------------------

@admin_bp.route("/user/<int:user_id>/details", methods=["GET"])
@jwt_required()
def get_user_details_api(user_id):

    claims = get_jwt()

    if claims["role"] != "admin":

        return{

            "message":"Admin access required."

        },403


    response, status = get_user_details(

        user_id

    )

    return jsonify(response), status

#----------------------- Update User Status -----------------------

@admin_bp.route("/user/<int:user_id>/status", methods=["PUT"])
@jwt_required()
def update_user_status_api(user_id):

    claims = get_jwt()

    if claims["role"] != "admin":

        return{

            "message":"Admin access required."

        },403


    response, status = update_user_account_status(

        user_id,

        request.get_json()

    )

    return jsonify(response), status

#----------------------- Get All Users -----------------------

@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def get_all_users_api():

    claims = get_jwt()

    if claims["role"] != "admin":

        return{

            "message":"Admin access required."

        },403

    response,status = get_all_users()

    return jsonify(response),status

#----------------------- Get Single User -----------------------

@admin_bp.route("/user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_api(user_id):

    claims = get_jwt()

    if claims["role"] != "admin":

        return{

            "message":"Admin access required."

        },403

    response,status = get_user(

        user_id

    )

    return jsonify(response),status

#----------------------- Get All Bookings -----------------------

@admin_bp.route("/bookings", methods=["GET"])
@jwt_required()
def get_all_bookings_api():

    claims = get_jwt()

    if claims["role"] != "admin":

        return{

            "message":"Admin access required."

        },403

    response,status = get_all_bookings()

    return jsonify(response),status

#----------------------- Get Booking Details -----------------------

@admin_bp.route("/booking/<int:booking_id>", methods=["GET"])
@jwt_required()
def get_booking_details_api(booking_id):

    claims = get_jwt()

    if claims["role"] != "admin":

        return{

            "message":"Admin access required."

        },403

    response,status = get_booking_details(

        booking_id

    )

    return jsonify(response),status

#----------------------- Update Booking -----------------------

@admin_bp.route("/booking/<int:booking_id>", methods=["PUT"])
@jwt_required()
def update_booking_api(booking_id):

    claims = get_jwt()

    if claims["role"] != "admin":

        return{

            "message":"Admin access required."

        },403

    response,status = update_booking(

        booking_id,

        request.get_json()

    )

    return jsonify(response),status

#----------------------- Reports -----------------------

@admin_bp.route("/reports", methods=["GET"])
@jwt_required()
def reports_api():

    claims = get_jwt()

    if claims["role"] != "admin":

        return{

            "message":"Admin access required."

        },403

    response,status = get_reports()

    return jsonify(response),status


#----------------------- Export Users -----------------------

@admin_bp.route("/reports/users")
@jwt_required()
def export_users_api():

    if get_jwt()["role"]!="admin":

        return{

            "message":"Admin access required."

        },403

    return export_users_report()


#----------------------- Export Staff -----------------------

@admin_bp.route("/reports/staff")
@jwt_required()
def export_staff_api():

    if get_jwt()["role"]!="admin":

        return{

            "message":"Admin access required."

        },403

    return export_staff_report()


#----------------------- Export Booking -----------------------

@admin_bp.route("/reports/bookings")
@jwt_required()
def export_booking_api():

    if get_jwt()["role"]!="admin":

        return{

            "message":"Admin access required."

        },403

    return export_booking_report()


#----------------------- Export Trek -----------------------

@admin_bp.route("/reports/treks")
@jwt_required()
def export_trek_api():

    if get_jwt()["role"]!="admin":

        return{

            "message":"Admin access required."

        },403

    return export_trek_report()