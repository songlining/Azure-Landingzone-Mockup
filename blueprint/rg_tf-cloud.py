import requests
from requests.auth import HTTPBasicAuth
from utilities.models import ConnectionInfo
from common.methods import set_progress
import time
from infrastructure.models import CustomField


def get_or_create_custom_fields():
    """
    Helper functions for main function to create custom field as needed
    """
    CustomField.objects.get_or_create(
        name='tfc_workspace',
        defaults={"label": 'TFC Workspace',"type": 'STR',"show_as_attribute":True}
    )
    CustomField.objects.get_or_create(
        name='lz_rg_name',
        defaults={"label": 'Resource Group',"type": 'STR',"show_as_attribute":True}
    )
    CustomField.objects.get_or_create(
        name='lz_project_id',
        defaults={"label": 'Project ID', "type": 'STR', "show_as_attribute":True}
    )
    CustomField.objects.get_or_create(
        name='lz_costcenter_id',
        defaults={"label": 'Cost Center ID', "type": 'STR', "show_as_attribute":True}
    )
    CustomField.objects.get_or_create(
        name='resource_group_id',
        defaults={"label": 'Resource Group ID', "type": 'STR', "show_as_attribute":True}
    )
    CustomField.objects.get_or_create(
        name='github_action_complete',
        defaults={"label": 'GH Action Complete or Not', "type": 'STR', "show_as_attribute":False}
    )


def run(job, resource, **kwargs):

    # change settings below
    ci = ConnectionInfo.objects.get(name="GitHub CAF")
    base_url = "https://api.github.com/repos/CloudBoltsoftware/Azure-CAF/actions/workflows/terraform-cloud.yaml/"
    webhook_url = "https://xx.xx.xx.xx/api/v3/cmp/inboundWebHooks/IWH-bofynxck/run/?token=WRE3f7Mv_D8gU7xhPKRt_UEyB_vnhy3kVQZq"

    rg_name = '{{ rg_name }}'
    project_id = '{{ project_id }}'
    costcenter_id = '{{ costcenter_id }}'

    tfc_workspace = rg_name  # super simplified for now

    get_or_create_custom_fields()
    resource.github_action_complete = "False"
    resource.lz_rg_name = rg_name
    resource.lz_project_id = project_id
    resource.lz_costcenter_id = costcenter_id
    resource.tfc_workspace = tfc_workspace
    resource.save()

    url_dispatches = f"{base_url}dispatches"

    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "ref": "main",
        "inputs": {
            "tfc_workspace": f'{tfc_workspace}',
            "rg_name": f'{rg_name}',
            "project_id": f'{project_id}',
            "costcenter_id": f'{costcenter_id}',
            "resource_id": f'{resource.id}',
            "webhook_url": f'{webhook_url}'
        }
    }
    response = requests.post(url_dispatches, headers=headers, json=data, auth=HTTPBasicAuth(f'{ci.username}', f'{ci.password}'))
    response.raise_for_status()

    # the last step in the github action will call webhook back to CMP to mark github_action_complete to True
    while resource.github_action_complete == 'False':
        time.sleep(10)
        set_progress('Wait for github action to complete')

    return (
        "Success",
        "Github workflow complete",
        f"Github response: {response.url}",
    )
