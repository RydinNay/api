from flask import jsonify
from app.database import db
from datetime import datetime
from dateutil.parser import parse
from app.models import DronsOnTasks, Drons, Tasks, DronsOnTasksSchema, DronsSchema, TasksSchema

def dron_on_task_add(task_data, dron_data, drontask_baseid):
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

        if(dron_data[best_dronid]["EnergyCapacuty"] < task_data[i]["Dist"] or dron_data[best_dronid]["EnergyCapacity"] < task_data[i]["Weight"]):
            break

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