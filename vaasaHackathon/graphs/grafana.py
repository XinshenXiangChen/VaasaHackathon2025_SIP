import os

import requests

url = "http://localhost:3000"
token = os.getenv('GRAFANA_API_KEY');

def check(response):
    if not response.ok:
        raise Exception(f"{response.status_code} {response.json()["message"]}")

def make_dashboard(name, folder, spec):
    data = {
        "metadata": {
            "name": f"{name}",
            "annotations": {
            "grafana.app/folder": f"{folder}"
            },
        },
        "spec": spec
    }

    response = requests.post(f"{url}/apis/dashboard.grafana.app/v1beta1/namespaces/default/dashboards",
                  headers={"Authorization": f"Bearer {token}"}, json=data)

    check(response)