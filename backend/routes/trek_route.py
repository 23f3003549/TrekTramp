from flask import jsonify, request , Blueprint
from flask_jwt_extended import jwt_required, get_jwt

from services.trek_service import create_trek , get_all_treks , get_trek , update_trek, delete_trek

trek_bp = Blueprint("trek", __name__)

#-------------------------------------create trek-----------------------------
@trek_bp.route("/treks", methods=["POST"])
@jwt_required()
def create_trek_api():
    claims = get_jwt()
    if claims["role"] != "admin":
        return{
            "message": "Only admin can create treks."
        }, 403
    
    data = request.get_json()
    response , status_code = create_trek(data)
    return jsonify(response), status_code

#--------------------------------------all treks-------------------------------
@trek_bp.route("/treks", methods=["GET"])
@jwt_required()
def get_all_treks_api():
    response, status_code = get_all_treks()
    return jsonify(response) , status_code
    

#--------------------------------------single trek----------------------------
@trek_bp.route("/treks/<int:trek_id>", methods=["GET"])
@jwt_required()
def get_trek_api(trek_id):
    response , status_code = get_trek(trek_id)
    return jsonify(response), status_code


#-----------------------------------------update trek---------------------------
@trek_bp.route("/treks/<int:trek_id>", methods=["PUT"])
@jwt_required()
def update_trek_api(trek_id):
    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Only admin can update trek."
        }), 403
    
    data = request.get_json()

    response , status_code = update_trek(trek_id , data)
    return jsonify(response), status_code

#--------------------------------------delete trek(admin)------------------------
@trek_bp.route("/treks/<int:trek_id>", methods=["DELETE"])
@jwt_required()
def delete_trek_api(trek_id):

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "message": "Only admin can delete trek."
        }), 403

    response, status_code = delete_trek(
        trek_id
    )

    return jsonify(response), status_code
