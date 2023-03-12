from hashlib import md5
from urllib.parse import urlencode

# return only the URL of the gravatar
def gravatar_url(email):
    email = email.encode("utf-8")
    return "https://www.gravatar.com/avatar/%s?%s" % (
        md5(email.lower()).hexdigest(),
        urlencode({"d": "retro"}),
    )
