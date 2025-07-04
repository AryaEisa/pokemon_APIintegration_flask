# security.py

from flask import request, abort, make_response
from functools import wraps
import re
import time

# Rate limiting – spara tidstämpel per IP
_rate_limit_cache = {}

def rate_limit(limit_per_minute=30):
    """
    Dekorator som begränsar antalet förfrågningar per IP-adress per minut.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            ip = request.remote_addr
            current_time = time.time()
            window = 60  # 60 sekunder

            # Rensa gammal historik
            requests_list = _rate_limit_cache.get(ip, [])
            requests_list = [ts for ts in requests_list if current_time - ts < window]

            if len(requests_list) >= limit_per_minute:
                return make_response("Too Many Requests", 429)

            requests_list.append(current_time)
            _rate_limit_cache[ip] = requests_list
            return f(*args, **kwargs)
        return wrapper
    return decorator

def sanitize_input(user_input: str) -> str:
    """
    Enkel sanering av användarinput – tillåter endast bokstäver, siffror och bindestreck.
    """
    cleaned = re.sub(r"[^a-zA-Z0-9\-]", "", user_input)
    return cleaned

def add_security_headers(response):
    """
    Lägger till säkerhetsrelaterade HTTP headers i alla svar.
    """
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' data: https://raw.githubusercontent.com;"
    return response
