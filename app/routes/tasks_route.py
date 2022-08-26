from flask import request, jsonify, Blueprint
from app.database import db
from app.models import Tasks, TasksSchema
from datetime import datetime
from dateutil.parser import parse

bp_tasks = Blueprint('tasks', __name__)

@bp_tasks.route('/Tasks/add', methods = ['POST'])
def add():
    data = request.get_json()
    task_dist = data.get("dist")
    task_weight = data.get("weight")
    task_desc = data.get("desc")
    task_datetime = parse(data.get("datetime"))
    task_clientid = data.get("clientid")

    try:
        new_task = Tasks(Dist = task_dist, Weight = task_weight,
                         TaskDesc = task_desc, Date = task_datetime, Task_Clientid = task_clientid)
        db.session.add(new_task)
        db.session.commit()
    except:
        return jsonify({
            "status": "error",
            "message": "Some kind of error happended"
        })

    return jsonify({
        "status": "success",
        "message": "Task added successfully"
    }), 201


@bp_tasks.route('/Tasks/remove', methods = ['DELETE'])
def remove():
    #data = request.get_json()
    task_id = request.args.get("taskid")

    try:
        task = Tasks.query.filter_by(Taskid = task_id).first()
        db.session.delete(task)
        db.session.commit()
    except:
        return jsonify({
            "status":"Error",
            "message":"Invalid Data"
        })

    return jsonify({
        "status": "success",
        "message": "Task remove successfully"
    })


@bp_tasks.route('/Tasks/select', methods = ['GET'])
def select():
    #data = request.get_json()
    task_clientid = request.args.get("clientid")

    task = Tasks.query.filter_by(Task_Clientid = task_clientid).all()
    task_schema = TasksSchema(many = True)
    output = task_schema.dump(task)
    return jsonify(
        output
    )


@bp_tasks.route('/Tasks/select_for_user', methods = ['GET'])
def selectAll():

    task_for_user_isOcu = Tasks.query.filter_by().all()
    #task_for_user_isnotOcu = Tasks.query.filter_by(IsOccupied = False).all()
    task_schema = TasksSchema(many = True)
    output = task_schema.dump(task_for_user_isOcu)

    return jsonify(
        output
    )
