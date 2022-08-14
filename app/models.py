from app.database import db,ma


class DronOnTaskStatistic(db.Model):
    Statisticid = db.Column(db.Integer, primary_key = True)
    Status = db.Column(db.Boolean, nullable = False)
    Dronid = db.Column(db.Integer, db.ForeignKey('drons.Dronid'), nullable = False)
    TaskDesc = db.Column(db.String, nullable = False)
    DronBaseid = db.Column(db.Integer, db.ForeignKey('drone_bases.DronBaseid'), nullable = False)
    Data = db.Column(db.DateTime, nullable = False)

    def __repr__(self):
        return f"DronOnTaskStatistic('{self.Statisticid}', '{self.Status}', '{self.TaskDesc}', '{self.Dronid}', '{self.DronBaseid}', '{self.Data}')"

    def serialize(self):
        return {
            'Statisticid': self.Statisticid,
            'Status': self.Status,
            'TaskDesc': self.TaskDesc,
            'Dronid': self.Dronid,
            'DronBaseid': self.DronBaseid,
            'Data': self.Data
        }


class DronsOnTasks(db.Model):
    DronTaskid = db.Column(db.Integer, primary_key = True)
    Date = db.Column(db.DateTime, nullable = False)
    DoTDronid = db.Column(db.Integer, db.ForeignKey('drons.Dronid'), default = 0)
    DoTTaskid = db.Column(db.Integer, db.ForeignKey('tasks.Taskid'), default = 0)
    DoTBaseid = db.Column(db.Integer, db.ForeignKey('drone_bases.DronBaseid'), nullable = False)

    def __repr__(self):
        return f"DronsOnTasks('{self.DronTaskid}', '{self.DoTTaskid}', '{self.DoTDronid}', '{self.Date}', '{self.DoTBaseid}')"

    def serialize(self):
        return {
            'DronTaskid': self.DronTaskid,
            'Date': self.Date,
            'DoTDronid': self.DoTDronid,
            'DoTTaskid': self.DoTTaskid,
            'DoTBaseid': self.DoTBaseid
        }

class DronsOnTasksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DronsOnTasks

class Clients(db.Model):
    Clientid = db.Column(db.Integer, primary_key = True)
    CliName = db.Column(db.String(50), nullable = False, )
    CliEmail = db.Column(db.String(50), unique = True, nullable = False)
    CliTel = db.Column(db.String(20), unique = True, nullable = False)
    CliPass = db.Column(db.String(500), nullable = False)
    tasks = db.relationship('Tasks', backref = 'clients', lazy = True)

#class ClientsSchema(ma.ModelSchema):
#    class Meta:
#        model = Clients


class Tasks(db.Model):
    Taskid = db.Column(db.Integer, primary_key = True)
    Dist = db.Column(db.Integer, nullable = False)
    Weight = db.Column(db.Integer, nullable = False)
    TaskDesc = db.Column(db.String(200), nullable = False)
    Date = db.Column(db.DateTime, nullable = False)
    IsOccupied = db.Column(db.Boolean, default = False)

    Task_Clientid = db.Column(db.Integer, db.ForeignKey('clients.Clientid'))
    dot = db.relationship('DronsOnTasks', backref = 'tasks', lazy = True)

class TasksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tasks

class Drons(db.Model):
    Dronid = db.Column(db.Integer, primary_key = True)
    DronModle = db.Column(db.String(15), nullable = False)
    EnergyCapacity = db.Column(db.Integer, nullable = False)
    LiftingCapacity = db.Column(db.Integer, nullable = False)
    DrDronBaseid = db.Column(db.Integer, db.ForeignKey('drone_bases.DronBaseid'), nullable = False)
    IsOccupied = db.Column(db.Boolean, default = False)
    dot = db.relationship('DronsOnTasks', backref = 'drons', lazy = True)


class DronsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Drons


class Users(db.Model):
    Userid = db.Column(db.Integer, primary_key = True)
    UserName = db.Column(db.String(50), nullable = False)
    UserEmail = db.Column(db.String(50), unique = True,  nullable = False)
    UserTel = db.Column(db.String(20), unique = True, default = 'None')
    UserPass = db.Column(db.String(500), nullable = False)
    UserRoleid = db.Column(db.Integer, db.ForeignKey('roles.Roleid'), nullable = False)
    UserDronBaseid = db.Column(db.Integer, db.ForeignKey('drone_bases.DronBaseid'), nullable = False)

    def __repr__(self):
        return f"Users('{self.Userid}', '{self.UserName}', '{self.UserDronBaseid}', '{self.UserEmail}', '{self.UserTel}')"

    def serialize(self):
        return {
            'Userid': self.Userid,
            'UserName': self.UserName,
            'UserDronBaseid': self.UserDronBaseid,
            'UserEmail': self.UserEmail,
            'UserTel': self.UserTel
        }

#class UsersSchema(ma.SQLAlchemyAutoSchema):
#    class Meta:
#        model = Users

class DroneBases(db.Model):
    DronBaseid = db.Column(db.Integer, primary_key=True)
    CompanyName = db.Column(db.String(30), nullable = False, unique = True)
    CompanyPass = db.Column(db.String(500), nullable = False, unique = True)
    drons = db.relationship('Drons', backref = 'drone_bases', lazy = True)
    drons_on_tasks = db.relationship('DronsOnTasks', backref = 'drone_bases', lazy = True)
    users = db.relationship('Users', backref = 'drone_bases', lazy = True)

class DroneBasesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DroneBases


class Roles(db.Model):
    Roleid = db.Column(db.Integer, primary_key = True)
    RoleName = db.Column(db.String(50), nullable = False)
    RoleDesc = db.Column(db.String(200), nullable = False)
    user = db.relationship('Users', backref = 'roles', lazy = True)


#class RolesSchema(ma.ModelSchema):
#    class Meta:
#        model = Roles