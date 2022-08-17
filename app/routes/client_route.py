from flask import request, jsonify, Blueprint
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from app.models import Clients

bp_client = Blueprint('client', __name__)

@bp_client.route('/Client/register', methods = ['POST'])
def register():
    data = request.get_json()
    client_name = data.get("username")
    client_email = data.get("email")
    client_tel = data.get("telephon")
    client_pass = generate_password_hash(data.get("password"))

    try:
        new_client = Clients(CliName = client_name, CliEmail = client_email,
                         CliTel = client_tel, CliPass = client_pass)
        db.session.add(new_client)
        db.session.commit()

    except:
        return jsonify({
            "status": "error",
            "message": "Some error happended"
        })

    return jsonify({
        "status": "success",
        "message": "User added successfully",
        "data": {
            "id": new_client.Clientid,
            #"token": access_token,
            "email": new_client.CliEmail
    }
    })


@bp_client.route('/Client/login', methods = ['GET'])
def login():
    #data = request.get_json()
    #client_name = data.get("username")
    client_email = request.args.get("email")
    #client_tel = data.get("telephon")
    client_pass = request.args.get("password")
    client = Clients.query.filter_by(CliEmail = client_email).first()

    #b = check_password_hash(client.CliPass, client_pass)
    #return client_pass

    if not client or not check_password_hash(client.CliPass, client_pass):
        return jsonify({
            "status": "failed",
            "message": "Failed getting user"
        })#, 401

    #access_token = create_access_token(identity=client_email)

    return jsonify({
        "status": "success",
        "message": "login successful",
        "data": {
            "id": client.Clientid,
            #"token": access_token,
            "email": client.CliEmail
        }
    }), 200


