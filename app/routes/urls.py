from flask import Blueprint, redirect, abort
from playhouse.shortcuts import model_to_dict

from app.models.url import Url

urls_bp = Blueprint("urls", __name__)


@urls_bp.route("/r/<short_code>")
def redirect_url(short_code):
    try:
        url = Url.get(Url.short_code == short_code)
    except Url.DoesNotExist:
        abort(404)

    if not url.is_active:
        abort(404)

    return redirect(url.original_url)
