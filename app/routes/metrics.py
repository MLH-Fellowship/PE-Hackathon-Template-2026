import random
import string

from flask import Blueprint, request, jsonify, abort
from playhouse.shortcuts import model_to_dict

from app.models.url import Url
from app.models.user import User
from app.utils.events import create_event

import psutil
import os

metrics_bp = Blueprint("metrics", __name__)


@metrics_bp.route("/metrics", methods=["GET"])
def get_metrics():
    process = psutil.Process(os.getpid())

  # Memor
    memory = psutil.virtual_memory()
    used_gb = round(memory.used / 1024 / 1024 / 1024, 1)
    total_gb = round(memory.total / 1024 / 1024 / 1024, 1)
    cpu_percent = psutil.cpu_percent(interval=1)
    
    return jsonify({
        'ram': f'{used_gb}/{total_gb} GB',
        'cpu': f'{cpu_percent}%'
    })
