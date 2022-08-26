from flask import request, jsonify, Blueprint
from app.database import db
from datetime import datetime
from dateutil.parser import parse
from app.models import DronsOnTasks, Drons, Tasks, DronsOnTasksSchema, DronsSchema, TasksSchema
from app.logic.dron_on_task_add import dron_on_task_add

bp_drons_on_tasks = Blueprint('drons_on_tasks', __name__)


@bp_drons_on_tasks.route('/Drons_on_Tasks/add/common', methods = ['POST'])
def add_common():
    data = request.get_json()
    drontask_drons = data.get("drons")
    drontask_tasks = data.get("tasks")
    drontask_baseid = data.get("baseid")

    task = Tasks.query.filter(Tasks.Taskid.in_(drontask_tasks)).all()

    if task == None:
        return jsonify({
            "status":"error",
            "message":"there are no task requiered"
    })

    dron = Drons.query.filter(Drons.Dronid.in_(drontask_drons)) \
        .filter(Drons.IsOccupied == False).order_by(Drons.EnergyCapacity).order_by(Drons.LiftingCapacity).all()

    dron_schema = DronsSchema(many = True)
    dron_data = dron_schema.dump(dron)

    task_schema = TasksSchema(many = True)
    task_data = task_schema.dump(task)

    dron_on_task_add(task_data, dron_data, drontask_baseid)

    return jsonify({
        "status": "success",
        "message": "Dron on Task added successfully"
    }), 201



@bp_drons_on_tasks.route('/Drons_on_Tasks/add/auto', methods = ['POST'])
def add_auto():
    data = request.get_json()
    drontask_baseid = data.get("baseid")

    task = Tasks.query.filter_by(IsOccupied = False).all()

    if task == None:
        return jsonify({
            "status":"error",
            "message":"there are no task requiered"
        })

    dron = Drons.query.filter(Drons.DrDronBaseid == drontask_baseid)\
        .filter(Drons.IsOccupied == False).order_by(Drons.EnergyCapacity).order_by(Drons.LiftingCapacity).all()

    dron_schema = DronsSchema(many = True)
    dron_data = dron_schema.dump(dron)

    task_schema = TasksSchema(many = True)
    task_data = task_schema.dump(task)

    dron_on_task_add(task_data, dron_data, drontask_baseid)

    return jsonify({
        "status": "success",
        "message": "Dron on Task added successfully"
    }), 201




@bp_drons_on_tasks.route('/Drons_on_Tasks/remove', methods = ['DELETE'])
def remove():

    #data = request.get_json()
    drontask_id = request.args.get("dron_on_taskid")
    #try:
    dron_on_task = DronsOnTasks.query.filter(DronsOnTasks.DronTaskid == drontask_id).first()
    dot_schema = DronsOnTasksSchema()
    output = dot_schema.dump(dron_on_task)

    #return jsonify({
    #    "m":dron_on_task.DoTDronid
    #})

    dron_occu = Drons.query.filter(Drons.Dronid == dron_on_task.DoTDronid).update({'IsOccupied': False})
    task_occu = Tasks.query.filter(Tasks.Taskid == dron_on_task.DoTTaskid).update({'IsOccupied': False})

    db.session.delete(dron_on_task)
    db.session.commit()
    #except:
    #    return jsonify({
    #        "status":"Error",
    #        "message":"Invalid Data"
    #    })

    return jsonify({
        "status": "success",
        "message": "Dron on Task remove successfully"
    })


#@bp_drons_on_tasks.route('/Drons_on_Tasks/edit', methods = ['POST'])
#def edit():
#    !
#    return 'good'


@bp_drons_on_tasks.route('/Drons_on_Tasks/select/user', methods = ['GET'])
def select_for_user():
    #data = request.get_json()

    drontask_baseid = request.args.get('baseid')

    dron_on_task = DronsOnTasks.query.filter(DronsOnTasks.DoTBaseid == drontask_baseid).all()
    dot_schema = DronsOnTasksSchema(many = True)
    output = dot_schema.dump(dron_on_task)
    return jsonify(
       list(map(lambda item: item.serialize(), dron_on_task))
    )


@bp_drons_on_tasks.route('/Drons_on_Tasks/select/client', methods = ['GET'])
def select_for_client():
    #data = request.get_json()
    drontask_clientid = request.args.get("clientid")
    #tasks = Tasks.query.filter(Tasks.Task_Clientid == drontask_clientid).all()
    dron_on_task = DronsOnTasks.query.join(Tasks, DronsOnTasks.DoTTaskid == Tasks.Taskid).filter(Tasks.Task_Clientid == drontask_clientid).all()
    dot_schema = DronsOnTasksSchema(many = True)
    output = dot_schema.dump(dron_on_task)
    return jsonify(
        list(map(lambda item: item.serialize(), dron_on_task))
    )

