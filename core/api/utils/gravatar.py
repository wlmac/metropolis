from hashlib import md5
from urllib.parse import urlencode


# return only the URL of the gravatar
def gravatar_url(email: str) -> str:
    email_hash = md5(email.encode("utf-8").lower()).hexdigest()
    query_string = urlencode({"d": "retro"})
    return f"https://www.gravatar.com/avatar/{email_hash}?{query_string}"
