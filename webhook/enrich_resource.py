"""
This is a working sample CloudBolt inbound web hook plug-in for you to start with.

These method runs synchronously. i.e. no job is created and the HTTP call will not return until
the method returns. The HTTP response will contain the dictionary which is returned from the method.

See the "CloudBolt Plug-ins" section of the docs for more info and the CloudBolt forge for more examples:
https://github.com/CloudBoltSoftware/cloudbolt-forge/tree/master/actions/cloudbolt_plugins
"""
from common.methods import set_progress


from resources.models import Resource


def inbound_web_hook_get(*args, parameters={}, **kwargs):
    """
    Use this method for operations that are read-only and do not change anything
    in CloudBolt or the environment.
    """
    set_progress(f"This message will show up in CloudBolt's application.log. args: {args}, kwargs: {kwargs}, parameters: {parameters}")
    return({"message":"Successfully executed the GET method of this inbound web hook", "example return info": 147, "GET parameters passed in": parameters})


def inbound_web_hook_post(*args, parameters={}, **kwargs):
    """
    Use this method for operations that make any kind of change. Remove
    this method entirely if your inbound web hook is read only.
    """
    set_progress(f"This message will show up in CloudBolt's application.log. args: {args}, kwargs: {kwargs}, parameters: {parameters}")

    resource_id = parameters['resource_id']
    tf_result = parameters['tf_result']["values"]["root_module"]["resources"][0]["values"]["id"]
    set_progress(f"tf_result: {tf_result}")

    r = Resource.objects.get(id=resource_id)
    r.resource_group_id = tf_result
    r.github_action_complete = "True"
    r.save()


    return({"message":"Successfully executed the POST method of this inbound web hook", "example return list": ["hovercraft", "eels", "bouncy"], "JSON parameters passed in": parameters})
