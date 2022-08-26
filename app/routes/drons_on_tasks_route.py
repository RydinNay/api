from flask import request, jsonify, Blueprint
from app.database import db
from datetime import datetime
from dateutil.parser import parse
from app.models import DronsOnTasks, Drons, Tasks, DronsOnTasksSchema, DronsSchema, TasksSchema

bp_drons_on_tasks = Blueprint('drons_on_tasks', __name__)


@bp_drons_on_tasks.route('/Drons_on_Tasks/add/common', methods = ['POST'])
def add_common():
    data = request.get_json()
    drontask_drons = data.get("drons")
    drontask_tasks = data.get("tasks")
    #drontask_date = parse(data.get("datetime"))
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

    '''for i in range(0, len(dron_data)):
        print(dron_data[i])
    for i in range(0, len(task_data)):
        print(task_data[i])'''

    for i in range(0, len(task_data)):

        best_dronid = 0;

        for j in range(0, len(dron_data)-1):

            if dron_data[j]["EnergyCapacity"] < task_data[i]["Dist"]:
                continue

            if dron_data[j]["LiftingCapacity"] < task_data[i]["Weight"]:
                continue

            if(i == 0 and j == 0):
                best_dronid = j
                continue

            if (dron_data[best_dronid]["EnergyCapacity"] > dron_data[j]["EnergyCapacity"] and
                    dron_data[best_dronid]["EnergyCapacity"]/dron_data[best_dronid]["LiftingCapacity"] >
                    dron_data[j]["EnergyCapacity"]/dron_data[j]["LiftingCapacity"]):
                best_dronid = j
            else:
                continue
        #remove

        if len(dron_data) != 0:
            try:
                dron_ocu = Drons.query.filter_by(Dronid = dron_data[best_dronid]["Dronid"]).update({'IsOccupied': True})
                task_ocu = Tasks.query.filter_by(Taskid = task_data[i]["Taskid"]).update({'IsOccupied': True})
                db.session.commit()
            except:
                return jsonify({
                    "status":"error"
                })

            new_dronontask = DronsOnTasks(DoTDronid = dron_data[best_dronid]["Dronid"], DoTTaskid = task_data[i]["Taskid"],
                                          Date = parse(task_data[i]["Date"]), DoTBaseid = drontask_baseid)
            db.session.add(new_dronontask)
            db.session.commit()

            del dron_data[best_dronid]
        else:
            return jsonify({
                "status":"succed",
                "message":"all drons are on task"
            })

    return jsonify({
        "status": "success",
        "message": "Dron on Task added successfully"
    }), 201



@bp_drons_on_tasks.route('/Drons_on_Tasks/add/auto', methods = ['POST'])
def add_auto():
    data = request.get_json()
    drontask_baseid = data.get("baseid")
    drontask_date = datetime.now()

    task = Tasks.query.filter_by(IsOccupied = False).all()
    #task_schema = TasksSchema()
    #output = task_schema.dump(task)

    #return jsonify({"task":output})

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

    for i in range(0, len(task_data)):

        best_dronid = 0;

        for j in range(0, len(dron_data)-1):

            if dron_data[j]["EnergyCapacity"] < task_data[i]["Dist"]:
                continue

            if dron_data[j]["LiftingCapacity"] < task_data[i]["Weight"]:
                continue

            if(i == 0 and j == 0):
                best_dronid = j
                continue

            if (dron_data[best_dronid]["EnergyCapacity"] > dron_data[j]["EnergyCapacity"] and
                                    dron_data[best_dronid]["EnergyCapacity"]/dron_data[best_dronid]["LiftingCapacity"] >
                                    dron_data[j]["EnergyCapacity"]/dron_data[j]["LiftingCapacity"]):
                    best_dronid = j
            else:
                continue
        #remove

        if len(dron_data) != 0:
            try:
                dron_ocu = Drons.query.filter_by(Dronid = dron_data[best_dronid]["Dronid"]).update({'IsOccupied': True})
                task_ocu = Tasks.query.filter_by(Taskid = task_data[i]["Taskid"]).update({'IsOccupied': True})
                db.session.commit()
            except:
                return jsonify({
                    "status":"error"
                })

            new_dronontask = DronsOnTasks(DoTDronid = dron_data[best_dronid]["Dronid"], DoTTaskid = task_data[i]["Taskid"],
                                  Date = parse(task_data[i]["Date"]), DoTBaseid = drontask_baseid)
            db.session.add(new_dronontask)
            db.session.commit()

            del dron_data[best_dronid]
        else:
            return jsonify({
                "status":"succed",
                "message":"all drons are on task"
            })

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

