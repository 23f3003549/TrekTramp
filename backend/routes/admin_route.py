from flask import jsonify, request, Blueprint

from services.admin_service import create_staff

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/staff", methods=["POST"])
def create_staff_api():
    data = request.get_json()

    response, status_code = create_staff(data)

    return jsonify(response), status_code