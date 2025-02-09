from flask import Blueprint, jsonify
from services import obtenerTemperatura, controlRele

experiment_bp = Blueprint('auth', __name__)

@experiment_bp.route('/data')
def data_route():
    data = obtenerTemperatura()
    return jsonify(data)

@experiment_bp.route('/rele')
def rele_route():
    result = controlRele()
    return result

