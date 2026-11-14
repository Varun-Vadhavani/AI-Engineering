TEMPORARY_CODES = {408, 429, 500, 502, 503, 504}
PERMANENT_CODES = {400, 401, 403, 404}

def get_code(e):
    for attr in ("code", "status_code"):
        v = getattr(e, attr, None)
        if isinstance(v, int):
            return v
    v = getattr(getattr(e, "response", None), "status_code", None)
    return v if isinstance(v, int) else None

def is_temporary(e):
    """True only for problems that may fix themselves. Unknown errors count as permanent."""
    code = get_code(e)
    if code in PERMANENT_CODES:
        return False
    if code in TEMPORARY_CODES:
        return True
    if isinstance(e, (TimeoutError, ConnectionError)):
        return True
    text = (type(e).__name__ + " " + str(e)).lower()
    if any(w in text for w in ("api key", "api_key", "not found", "invalid argument", "permission")):
        return False
    return any(w in text for w in ("timeout", "timed out", "deadline", "unavailable",
                                   "overloaded", "rate limit", "resource exhausted",
                                   "connection", "429", "503"))