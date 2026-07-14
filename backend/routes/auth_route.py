from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required , get_jwt, get_jwt_identity, create_access_token

from services.auth_service import register , login

auth_bp = Blueprint("auth", __name__)

#--------------------------------------User Registraion-------------------------
@auth_bp.route("/user/registration", methods=['POST'])
def create_user_api():
    data = request.get_json()

    response, status_code = register(data)

    return jsonify(response), status_code

#----------------------login-------------------------------
@auth_bp.route("/login", methods=['POST'])
def login_api():
    data = request.get_json()

    response, status_code = login(data)

    return jsonify(response), status_code


#---------------------------refresh token-------------------------
@auth_bp.route( "/refresh",methods=["POST"])
@jwt_required(refresh=True)
def refresh():

    user_id = get_jwt_identity()

    claims = get_jwt()

    access_token = create_access_token(

        identity=user_id,

        additional_claims={

            "role": claims["role"]

        }

    )

    return {

        "access_token": access_token

    },200
