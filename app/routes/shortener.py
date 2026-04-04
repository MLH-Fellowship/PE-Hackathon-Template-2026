import os
import secrets
import string
from datetime import datetime
from urllib.parse import urlparse

from flask import Blueprint, jsonify, redirect, request
from peewee import IntegrityError

from app.models.url import Url

shortener_bp = Blueprint("shortener", __name__)

_ALPHABET = string.ascii_letters + string.digits


def _is_valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _generate_code(length: int = 6) -> str:
    return "".join(secrets.choice(_ALPHABET) for _ in range(length))


def _base_url() -> str:
    configured = os.environ.get("APP_BASE_URL")
    if configured:
        return configured.rstrip("/")
    return request.host_url.rstrip("/")


@shortener_bp.post("/shorten")
def shorten_url():
    payload = request.get_json(silent=True) or {}
    original_url = (payload.get("url") or payload.get("original_url") or "").strip()
    title = (payload.get("title") or "").strip() or None

    if not original_url or not _is_valid_url(original_url):
        return jsonify(error="Please provide a valid http/https URL in 'url'"), 400

    for _ in range(10):
        code = _generate_code()
        try:
            url = Url.create(
                original_url=original_url,
                short_code=code,
                title=title,
                updated_at=datetime.utcnow(),
            )
            return (
                jsonify(
                    original_url=url.original_url,
                    short_code=url.short_code,
                    short_url=f"{_base_url()}/{url.short_code}",
                ),
                201,
            )
        except IntegrityError:
            continue

    return jsonify(error="Could not generate a unique short code. Please retry."), 500


@shortener_bp.get("/<short_code>")
def resolve_short_url(short_code: str):
    url = Url.get_or_none((Url.short_code == short_code) & (Url.is_active == True))
    if url is None:
        return jsonify(error="Short URL not found"), 404

    return redirect(url.original_url, code=302)
