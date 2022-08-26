from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from app.models import Users, DroneBases

bp_user = Blueprint('user', __name__)

@bp_user.route('/Users/register', methods = ['POST'])
def register():
    data = request.get_json()
    user_name = data.get("username")
    user_email = data.get("email")
    try:
        user_tel = data.get("telephon")
    except:
        user_tel = "None"
    user_pass = generate_password_hash(data.get("password"))
    try:
        user_role = data.get("roleid")
    except:
        user_role = 0
    #user_baseid = data.get("baseid")
    #if(user_baseid == None):
    #    user_baseid = 0


    isAdmin = data.get("isAdmin")

    print(isAdmin)
    try:
        if isAdmin != None:
            company_name= data.get("companyName")
            company_pass = data.get("companyPass")
            dron_base = DroneBases(CompanyName = company_name, CompanyPass = company_pass)
            db.session.add(dron_base)
            db.session.commit()
        else:
            baseid = data.get("baseid")
            dron_base = DroneBases.query.filter_by(DronBaseid = baseid).first()
            print(dron_base)

        new_user = Users(UserName = user_name, UserEmail = user_email,
                             UserTel = user_tel, UserPass = user_pass, UserRoleid = user_role, UserDronBaseid = dron_base.DronBaseid)
        #print(user_name, user_email, user_tel, user_pass, user_role, new_dron_base.DronBaseid)
        db.session.add(new_user)
        db.session.commit()

    except:
        return jsonify({
            "status": "error",
            "message": "Some error happended"
        })

    if isAdmin!=None:
        return jsonify({
            "status": "success",
            "message": "User added successfully",
            "data":{
                "id": new_user.Userid,
                #"token": access_token,
                "email": new_user.UserEmail,
                "dron_baseid" : new_user.UserDronBaseid,
                "user_roleid" : new_user.UserRoleid
            }
        })
    else:
        return jsonify({
            "status": "success",
            "message": "User added successfully",
        })


@bp_user.route('/Users/remove', methods = ['DELETE'])
def remove():
    #data = request.get_json()
    user_id = request.args.get("Userid")

    try:
        user = Users.query.filter_by(Userid = user_id).first()
        db.session.delete(user)
        db.session.commit()
    except:
        return jsonify({
            "status":"Error",
            "message":"Invalid Data"
        })

    return jsonify({
        "status": "success",
        "message": "User remove successfully"
    })



@bp_user.route('/Users/login', methods = ['GET'])
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
        })#, 401

    #access_token = create_access_token(identity=client_email)

    return jsonify({
        "status": "success",
        "message": "login successful",
        "data": {
            "id": user.Userid,
            #"token": access_token,
            "email": user.UserEmail,
            "dron_baseid" : user.UserDronBaseid,
            "user_roleid" : user.UserRoleid
        }
    }), 200


@bp_user.route('/Users/all', methods = ['GET'])
def all_users():
    baseid=request.args.get("baseid")
    users = Users.query.filter(Users.UserDronBaseid == baseid, Users.UserRoleid != 1).all()
    print(users)
    #users_schema = UsersSchema(many=True)
    #users_data = users_schema.dump(users)
    return jsonify(
        list(map(lambda item: item.serialize(), users))
    )