from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required , get_jwt

from services.admin_service import create_staff , assign_staff , admin_dashboard

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

#-------------------------------------assign staff--------------------------
@admin_bp.route("/treks/<int:trek_id>/assign-staff", methods=["PUT"])
@jwt_required()
def assign_staff_api(trek_id):
    claims = get_jwt()

    if claims["role"] != "admin":
        return {
            "message": "Only Admin can assign staff."
        }, 403
    
    data = request.get_json()

    response, status_code = assign_staff(trek_id,data)

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