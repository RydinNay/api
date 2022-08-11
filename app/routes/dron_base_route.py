from flask import request, jsonify, Blueprint
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from app.models import DroneBases, DroneBasesSchema, Users

bp_dron_base = Blueprint('dron_base', __name__)


@bp_dron_base.route('/Dron_Bases', methods = ['POST'])
def add():
    data = request.get_json()
    compay_name = data.get("dron_base_name")
    company_pass = data.get("dron_base_pass")

    try:
        new_dron_base = DroneBases(CompanyName = compay_name, CompanyPass = company_pass)
        db.session.add(new_dron_base)
        db.session.commit()
    except:
        return jsonify({
            "status": "error",
            "message": "Some kind of error happended"
        })

    return jsonify({
        "status": "success",
        "message": "Dron_Base added successfully"
    }), 201


@bp_dron_base.route('/Dron_Bases', methods = ['DELETE'])
def remove():

    #data = request.get_json()
    dron_base_id = request.args.get("dron_base_id")
    owner_id = request.args.get("owner_id")

    try:
        dron_base = DroneBases.query.join(Users.UserDronBaseid == owner_id and Users.UserRoleid == 2).filter(DroneBases.DronBaseid == dron_base_id).first()
        db.session.delete(dron_base)
        db.session.commit()
    except:
        return jsonify({
            "status":"Error",
            "message":"Invalid Data"
        })

    return jsonify({
        "status": "success",
        "message": "Dron remove successfully"
    })

@bp_dron_base.route('/Dron_Base', methods=['GET'])
def get_dron_base():
    baseid = request.args.get("baseid")
    try:
        dron_base = DroneBases.query.filter(DroneBases.DronBaseid == baseid).all()
        dron_schema = DroneBasesSchema(many=True)
        output = dron_schema.dump(dron_base)
        return jsonify(output)
    except:
        return jsonify(
            {
                "status":"error"
            }
        )
