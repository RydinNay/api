from app.models import DronOnTaskStatistic, DronsOnTasks
from app.database import db
from datetime import datetime
from app.app import app

def add_statistic():
    with app.app_context():

        delete_drons_on_task = DronsOnTasks.query.filter(DronsOnTasks.Date < datetime.now()).all()
        for i in range(len(delete_drons_on_task)):
            new_task = DronOnTaskStatistic(Status = True, Dronid = delete_drons_on_task[i].DoTDronid, TaskDesc = delete_drons_on_task[i].DoTTaskDesc, DronBaseid = delete_drons_on_task.DoTBaseid, Data = delete_drons_on_task.DoTDate)
            db.session.delete(delete_drons_on_task[i])
            db.session.add(new_task)
            db.session.commit()
        print("a")
