from flask import jsonify, request, Blueprint

from services.auth_service import register , login

auth_bp = Blueprint("auth", __name__)

#--------------------------------------User Registraion-------------------------
@auth_bp.route("/user/registration", methods=['POST'])
def create_user_api():
    data = request.get_json()

    response, status_code = register(data)

    return jsonify(response), status_code

@auth_bp.route("/login", methods=['POST'])
def login_api():
    data = request.get_json()

    response, status_code = login(data)

    return jsonify(response), status_code
