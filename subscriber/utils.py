"""File with utils functions."""
import os
import requests

API_BASE_URL = '/api/v1/'


def email_exists(email):
    """Function that hits Grafana User API endpoint to verify email exists."""
    # TODO import these from .config or .utils or somewhere that takes env
    # variables.
    admin_user = os.getenv("GRAFANA_USER", "admin")
    admin_psswd = os.getenv("GRAFANA_PASSWORD", "admin")
    host = os.getenv("GRAFANA_HOST", "grafana")
    port = int(os.getenv("GRAFANA_PORT", "3000"))
    endpoint = "/api/users/lookup?loginOrEmail={email}".format(email=email)

    url = "http://{username}:{password}@{host}:{port}{endpoint}".format(
        username=admin_user,
        password=admin_psswd,
        host=host,
        port=port,
        endpoint=endpoint
    )

    return requests.get(url).status_code == 200
