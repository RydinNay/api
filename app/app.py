from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from app.database import db,ma
from app.routes.client_route import bp_client
from app.routes.dron_route import bp_dron
from app.routes.tasks_route import bp_tasks
from app.routes.users_route import bp_user
from app.routes.drons_on_tasks_route import bp_drons_on_tasks
from app.routes.dron_base_route import bp_dron_base


migration = Migrate()
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dronzi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
#app.config['CORS_HEADERS'] = 'Content-Type'


db.init_app(app)

migration.init_app(app, db)

ma.init_app(app)

@app.route('/')
def index():
    return jsonify("API in Currently online")


app.register_blueprint(bp_client)
app.register_blueprint(bp_dron)
app.register_blueprint(bp_user)
app.register_blueprint(bp_tasks)
app.register_blueprint(bp_drons_on_tasks)
app.register_blueprint(bp_dron_base)