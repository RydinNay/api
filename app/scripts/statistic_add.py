from app.models import DronOnTaskStatistic, DronsOnTasks, Tasks, Drons
from app.database import db
from datetime import datetime
from app.app import app

def add_statistic():
    with app.app_context():
        #print(datetime.now())
        delete_drons_on_task = DronsOnTasks.query.filter(DronsOnTasks.Date < datetime.now()).all()

        for i in range(len(delete_drons_on_task)):
            tasks = Tasks.query.filter(Tasks.Taskid == delete_drons_on_task[i].DoTTaskid).first()
            dron_ocu = Drons.query.filter_by(Dronid = delete_drons_on_task[i].DoTDronid).update({'IsOccupied': False})
            #task = Tasks.query.filter_by(Taskid = delete_drons_on_task[i].DoTTaskid)
            db.session.commit()
            new_task = DronOnTaskStatistic(Status = True, Dronid = delete_drons_on_task[i].DoTDronid, TaskDesc = tasks.TaskDesc, DronBaseid = delete_drons_on_task[i].DoTBaseid, Data = delete_drons_on_task[i].Date)
            db.session.delete(delete_drons_on_task[i])
            db.session.delete(tasks)
            db.session.add(new_task)
            db.session.commit()

