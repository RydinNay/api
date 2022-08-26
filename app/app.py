from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import db,ma
from app.routes.client_route import bp_client
from app.routes.dron_route import bp_dron
from app.routes.tasks_route import bp_tasks
from app.routes.users_route import bp_user
from app.routes.drons_on_tasks_route import bp_drons_on_tasks
from app.routes.dron_base_route import bp_dron_base
from app.routes.statistic_route import bp_statistic


migration = Migrate()
app = Flask(__name__)

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dronzi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db.init_app(app)

migration.init_app(app, db)

ma.init_app(app)

app.register_blueprint(bp_client)
app.register_blueprint(bp_dron)
app.register_blueprint(bp_user)
app.register_blueprint(bp_tasks)
app.register_blueprint(bp_drons_on_tasks)
app.register_blueprint(bp_dron_base)
app.register_blueprint(bp_statistic)

from app.scripts.statistic_add import add_statistic


scheduler = BackgroundScheduler()

scheduler.add_job(add_statistic, trigger="interval", seconds=10)

scheduler.start()