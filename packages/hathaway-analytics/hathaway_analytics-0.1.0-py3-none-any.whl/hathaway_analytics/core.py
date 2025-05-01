import threading
import requests
import platform
import configparser
import os
from flask import request, abort
from flask_login import current_user
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from user_agents import parse as parse_user_agent

# Initialize SQLAlchemy (must be initialized in your Flask app)
db = SQLAlchemy()

# Load configuration from hathaway_analytics.cfg
config = configparser.ConfigParser()
local_path = os.path.join(os.getcwd(), 'hathaway_analytics.cfg')
default_path = os.path.join(os.path.dirname(__file__), 'hathaway_analytics.cfg')
config_path = local_path if os.path.isfile(local_path) else default_path
config.read(config_path)

try:
        ANALYTICS_SECRET = config.get('analytics', 'secret', fallback='').strip() or False
except Exception:
        ANALYTICS_SECRET = False

try:
        ANALYTICS_ENDPOINT = config.get('analytics', 'endpoint', fallback='').strip() or False
except Exception:
        ANALYTICS_ENDPOINT = False

try:
        raw_ips = config.get('analytics', 'allowed_ips', fallback='')
        ALLOWED_IPS = {ip.strip() for ip in raw_ips.split(',') if ip.strip()} or False
except Exception:
        ALLOWED_IPS = False

print(f"[Analytics Config] ANALYTICS_SECRET: {repr(ANALYTICS_SECRET)}")
print(f"[Analytics Config] ANALYTICS_ENDPOINT: {ANALYTICS_ENDPOINT}")
print(f"[Analytics Config] ALLOWED_IPS: {ALLOWED_IPS}")

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String)
    timestamp = db.Column(db.Integer)
    domain = db.Column(db.String)
    path = db.Column(db.String)
    method = db.Column(db.String)
    query = db.Column(db.Text)
    os = db.Column(db.String)
    browser = db.Column(db.String)
    device = db.Column(db.String)
    referrer = db.Column(db.Text)
    user = db.Column(db.String)

def send_data_analytics():
    """
    Collects request metadata and sends it to the central analytics server.
    Safe to call from Flask's @app.before_request. Runs in a thread to avoid blocking.
    """
    try:
        ip = request.headers.get("X-Real-IP", request.remote_addr)

        try:
            user = str(current_user.get_id()) if current_user.is_authenticated else None
        except Exception:
            user = None

        data = {
            "ip": ip,
            "timestamp": int(datetime.utcnow().timestamp()),
            "domain": request.host,
            "path": request.path,
            "method": request.method,
            "query": request.query_string.decode(),
            "referrer": request.referrer,
            "user": user,
            "user_agent": request.headers.get("User-Agent", "")
        }

        headers = {
            "Content-Type": "application/json"
        }
        if ANALYTICS_SECRET:
            headers["X-Analytics-Token"] = ANALYTICS_SECRET

        def _send():
            try:
                print(f"[Analytics] Sending data to {ANALYTICS_ENDPOINT}")
                response = requests.post(
                    ANALYTICS_ENDPOINT,
                    json=data,
                    headers=headers,
                    timeout=0.5
                )
                print(f"[Analytics] Response code: {response.status_code}")
            except Exception as e:
                print(f"[Analytics] Failed to send analytics: {e}")

        threading.Thread(target=_send, daemon=True).start()

    except Exception as e:
        print(f"[Analytics] Error preparing analytics data: {e}")

def receive_data_analytics():
    """
    Flask route handler to receive and store analytics data.
    Enforces secret token and IP filtering if configured.
    """
    if ANALYTICS_SECRET:
        if request.headers.get("X-Analytics-Token") != ANALYTICS_SECRET:
            return abort(403)

    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(',')[0].strip()

    if ALLOWED_IPS and client_ip not in ALLOWED_IPS:
        print(f"[Analytics] Blocked IP: {client_ip}")
        return abort(403)

    data = request.get_json(silent=True)
    if not data:
        return abort(400)

    # Parse user-agent string
    ua_string = data.get("user_agent", "")
    ua = parse_user_agent(ua_string)

    try:
        log = Log(
            ip=data.get("ip"),
            timestamp=data.get("timestamp"),
            domain=data.get("domain"),
            path=data.get("path"),
            method=data.get("method"),
            query=data.get("query"),
            os=ua.os.family,
            browser=ua.browser.family,
            device = "Mobile" if ua.is_mobile else "Tablet" if ua.is_tablet else "PC" if ua.is_pc else "Other",
            referrer=data.get("referrer"),
            user=data.get("user")
        )
        db.session.add(log)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        print("Failed to log analytics:", str(e))
        return abort(500)
