from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from pathlib import Path

from django.conf import settings


def load_creds() -> tuple[Credentials | None, str | None, bool]:
    """
    Returns credentials from authorized_user.json file

    :returns: Tuple with the creds, error message and
    whether the client secret file exists
    """

    CLIENT_PATH = settings.SECRETS_PATH + "/client_secret.json"
    AUTHORIZED_PATH = settings.SECRETS_PATH + "/authorized_user.json"

    if not Path(settings.SECRETS_PATH).is_dir():
        return (None, f"{settings.SECRETS_PATH} directory does not exist", False)

    if not Path(CLIENT_PATH).is_file():
        return (None, f"{CLIENT_PATH} does not exist", False)

    scopes = settings.GOOGLE_SCOPES

    if Path(AUTHORIZED_PATH).is_file():
        creds = None

        try:
            creds = Credentials.from_authorized_user_file(AUTHORIZED_PATH, scopes)
        except Exception:
            return (None, "Failed to load credentials", True)

        if not creds.valid and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                return (None, "Failed to refresh credentials", True)

            with open(AUTHORIZED_PATH, "w") as f:
                f.write(creds.to_json())

        return (creds, None, True)

    else:
        return (None, "No file to load client from", True)
