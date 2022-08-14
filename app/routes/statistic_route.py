from flask import request, jsonify, Blueprint
from app.database import db
from app.models import DronOnTaskStatistic
bp_statistic = Blueprint('statistic;;', __name__)

@bp_statistic.route('/Statistic', methods = ['GET'])
def register():
    #data = request.get_json()
    base = request.args.get("baseid")

    statistic = DronOnTaskStatistic.query.filter(DronOnTaskStatistic.DronBaseid == base).all()

    return jsonify({
        "status": "success",
        "message": "User added successfully",
        "data": list(map(lambda item: item.serialize(), statistic))
    })

