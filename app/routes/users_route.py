from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from app.models import Users

bp_user = Blueprint('user', __name__)

@bp_user.route('/Users/register', methods = ['POST'])
def register():
    #data = request.get_json()
    user_name = request.args.get("username")
    user_email = request.args.get("email")
    try:
        user_tel = request.args.get("telephon")
    except:
        user_tel = "None"
    user_pass = generate_password_hash(request.args.get("password"))
    try:
        user_role = request.args.get("roleid")
    except:
        user_role = 0

    try:
        user_baseid = request.args.get("baseid")
    except:
        user_baseid = 0

    try:
        new_client = Users(UserName = user_name, UserEmail = user_email,
                             UserTel = user_tel, UserPass = user_pass, UserRole = user_role, UserDroneBaseid = user_baseid)
        db.session.add(new_client)
        db.session.commit()

    except:
        return jsonify({
            "status": "error",
            "message": "Some error happended"
        })

    return jsonify({
        "status": "success",
        "message": "User added successfully"
    })


@bp_user.route('/Users/login', methods = ['POST'])
def login():
    #data = request.get_json()
    #client_name = data.get("username")
    user_email = request.args.get("email")
    #client_tel = data.get("telephon")
    user_pass = request.args.get("password")
    user = Users.query.filter_by(UserEmail = user_email).first()

    #b = check_password_hash(client.CliPass, client_pass)
    #return client_pass

    if not user or not check_password_hash(user.UserPass, user_pass):
        return jsonify({
            "status": "failed",
            "message": "Failed getting user"
        }), 401

    #access_token = create_access_token(identity=client_email)

    return jsonify({
        "status": "success",
        "message": "login successful",
        "data": {
            "id": user.Userid,
            #"token": access_token,
            "email": user.UserEmail,
            "dron_baseid" : user.UserDronBaseid
        }
    }), 200