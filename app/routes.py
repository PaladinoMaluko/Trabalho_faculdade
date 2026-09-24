from flask import Blueprint, jsonify
from app.models import db

bp = Blueprint('api', __name__)

@bp.route('/', methods=['GET'])
def index():
       return jsonify({"mensagem": "API funcionando"})