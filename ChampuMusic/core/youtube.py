import json
import os

YOUTUBE = {
    "access_token": "ya29.a0AeDClZCWhJmZVa8F3dekhUnsqJD2rbVZbqRW8JfIDHun7O4dyzQdMe6KJ0SHOVuxxp0P7pW499JTVYgToi4TvtXQEKj_I5Bd831Zqj5_ZQ8u6qNX9IH8-ul2vA8zaOm-FwKdWcXJNcZYlssvpYAI6uEJ84oZJS_gq8MwcV-eMpVW_U64F-WpaCgYKARESARISFQHGX2MiS96BDOnz2FcmBr99MFTPEg0187",
    "expires": 1730055102.644152,
    "refresh_token": "1//05_QJ5UjnairhCgYIARAAGAUSNgF-L9Irc5KD12RJqb_KIFaNzGGcnY4dmo8BQUkLNaMzypntz4uYWKcamZ4p95LpikruLy7IFw",
    "token_type": "Bearer"
}


def vipboy():
    TOKEN_DATA = os.getenv("TOKEN_DATA")
    if not TOKEN_DATA:
        os.environ["TOKEN_DATA"] = json.dumps(YOUTUBE)
