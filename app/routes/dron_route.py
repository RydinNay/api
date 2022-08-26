from flask import request, jsonify, Blueprint
from app.database import db
from app.models import Drons, DronsSchema, Tasks, DronsOnTasks
from flask_cors import CORS, cross_origin

bp_dron = Blueprint('dron', __name__)


@bp_dron.route('/Dron', methods = ['POST'])
def add():
    data = request.get_json()
    dron_modle = data.get("modle")
    dron_ecap = data.get("ecapacity")
    dron_lcap = data.get("lcapacity")
    dron_baseid = data.get("baseid")

    try:
        new_dron = Drons(DronModle = dron_modle, EnergyCapacity = dron_ecap,
                     LiftingCapacity = dron_lcap, DrDronBaseid = dron_baseid)
        db.session.add(new_dron)
        db.session.commit()
    except:
        return jsonify({
            "status": "error",
            "message": "Some kind of error happended",
            "molde": dron_modle,
            "lcap":dron_lcap,
            "ecap":dron_ecap
        })

    return jsonify({
        "status": "success",
        "message": "Dron added successfully"
    }), 201


@bp_dron.route('/Dron', methods = ['DELETE'])
def remove():

    #data = request.get_json()
    dron_id = request.args.get("dronid")

    try:
        dron = Drons.query.filter_by(Dronid = dron_id).first()
        db.session.delete(dron)
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


@bp_dron.route('/Dron', methods = ['PUT'])
def edit():
    data = request.get_json()
    dronid = data.get("dronid")
    energycap = data.get("ecapacity")
    liftcap = data.get("lcapacity")

    try:
        dron = Drons.query.filter_by(Dronid = dronid).first()
    except:
        return jsonify({
            "status":"error",
            "message":"That dron dose not exist"
        })

    if energycap != None:
        try:
            dron_encap = Drons.query.filter_by(Dronid = dronid).update({'EnergyCapacity': energycap})
            db.session.commit()
        except:
            return jsonify({
                "status":"error"
            })

    if liftcap != None:
        try:
            dron_liftcap = Drons.query.filter_by(Dronid = dronid).update({'LiftingCapacity': liftcap})
            db.session.commit()
        except:
            return jsonify({
                "status":"error"
            })

    return jsonify({
        "status":"succsed",
        "mesage":"Dron edit succesfully"
    })


@bp_dron.route('/Dron', methods = ['GET'])
@cross_origin()
def select():
    dron_baseid = request.args.get("baseid")
    dron = Drons.query.filter_by(DrDronBaseid = dron_baseid).all()
    dron_schema = DronsSchema(many = True)
    output = dron_schema.dump(dron)

    return jsonify(output)

@bp_dron.route('/Dron/select_for_client', methods = ['GET'])
@cross_origin()
def select_for_client():
    clientid = request.args.get("clientid")
    dron = Drons.query.join(DronsOnTasks, DronsOnTasks.DoTDronid == Drons.Dronid).join(Tasks, Tasks.Taskid == DronsOnTasks.DoTTaskid).filter(Tasks.Task_Clientid == clientid).all()
    print(dron)
    dron_schema = DronsSchema(many = True)
    output = dron_schema.dump(dron)

    return jsonify(output)



