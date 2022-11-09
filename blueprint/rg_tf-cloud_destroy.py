import requests
from requests.auth import HTTPBasicAuth
from utilities.models import ConnectionInfo
from common.methods import set_progress
import time

def run(job, resource, **kwargs):

    # change settings below
    ci = ConnectionInfo.objects.get(name="GitHub CAF")
    base_url = "https://api.github.com/repos/CloudBoltsoftware/Azure-CAF/actions/workflows/terraform-cloud-teardown.yaml/"
    tfc_org = "larryslab"

    tfc_workspace = resource.tfc_workspace
    set_progress(f"tfc_workspace: {tfc_workspace}")

    url_dispatches = f"{base_url}dispatches"

    tfc_org_url = f'https://app.terraform.io/api/v2/organizations/{tfc_org}'

    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "ref": "main",
        "inputs": {
            "workspace_name": f'{tfc_workspace}',
            "tfc_org_url": tfc_org_url
        }
    }
    response = requests.post(url_dispatches, headers=headers, json=data, auth=HTTPBasicAuth(f'{ci.username}', f'{ci.password}'))

    response.raise_for_status()

    return (
        "Success",
        "Github workflow complete",
        f"Github response: {response.url}",
    )
