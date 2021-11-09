from re import L
from sys import exc_info
from typing import Any
from fastapi.routing import APIRouter
from app.core.config import settings
from pprint import pprint
import openapi_client
from openapi_client.api import workflow_service_api
from openapi_client.model.io_argoproj_workflow_v1alpha1_workflow_create_request import IoArgoprojWorkflowV1alpha1WorkflowCreateRequest
from openapi_client.model.io_argoproj_workflow_v1alpha1_workflow_submit_request import IoArgoprojWorkflowV1alpha1WorkflowSubmitRequest
import sseclient
import requests
import json
from sse_starlette.sse import EventSourceResponse
from app.core.log import logger

router = APIRouter()


config = openapi_client.Configuration(host='https://argo-hcptest.skhynix.com')
config.verify_ssl = False
config.discard_unknown_keys = True
api_client = openapi_client.ApiClient(configuration=config)
api_client.set_default_header('Authorization', 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImZ4VWpBRDVYOS1HYlNEWXhjMHFRNllEejYtaUNGVlFLeDIwYjRTbjY5eVEifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJhcmdvIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImFyZ28tc2VydmVyLXRva2VuLXBqMmJ0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFyZ28tc2VydmVyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiOWNhMDAzODAtZWZhNy00ZTE5LTk0M2EtMjU1Y2Q4MmRmMWM5Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmFyZ286YXJnby1zZXJ2ZXIifQ.DAO_KtpeLIki0axcchCP3U4NsatGSGD5By76hPG1GdM1Pqhq9qwUUI13kpMyK92wyt4x9CVv2YZsmqYS4Vo8Ut891tdhkLdo2EtBuaJv8YTT4YbYyk_iE5A7kLZo_1oBEM1m-87VbAIX-WMn7iYC0FsBcsYAT2m-rxnk72iJ6_wQoLbB-WSnBr_kPpd9d8tDqvAS1ZCh_T205ZBllIMUUNrq9OxoJmN3WbLKZQ7skJGkJSX6d7Jd42TQX0lHMS3gy-lyFq_GtUJeGlzjhisTuH1gmaQuuCmdW7bd3jGQ3i1IlBfchBZERQsnVf8ZYpCfN864uOInERqzkw954RlM5Q')
api_client.set_default_header('Accept', 'application/json')
api_client.set_default_header('Content-type', 'application/json')

@router.get("/argowf/test")
def argowf_test():
    try:
        workflow_api = workflow_service_api.WorkflowServiceApi(api_client=api_client)

        # with open("./hello-world.yaml") as f:
        #     manifest: dict = yaml.safe_load(f)
        # # manifest['spec']['serviceAccountName'] = 'argo'

        # api_response = workflow_api.workflow_service_create_workflow(
        #     namespace='argo',
        #     body=IoArgoprojWorkflowV1alpha1WorkflowCreateRequest(workflow=manifest, _check_type=False)
        # )

        submit_options = {
            "entryPoint": "argosay",
            "labels": "submit-from-ui=true",
            "parameters": [
                "message=workflow.parameters.message"
            ]
        }

        api_response = workflow_api.workflow_service_submit_workflow(
            namespace='argo',
            body=IoArgoprojWorkflowV1alpha1WorkflowSubmitRequest(
                _check_type=False,
                namespace='argo',
                resource_kind='WorkflowTemplate',
                resource_name='argowf-template-awesome-octopus',
                submit_options=submit_options
            )
        )

        pprint(api_response)
    except Exception as e:
        logger.error(e, exc_info=True)



@router.get("/argowf/list")
def argowf_list():

    workflow_api = workflow_service_api.WorkflowServiceApi(api_client)
    
    continue_token = workflow_api.workflow_service_list_workflows(namespace='argo',list_options_limit=1)['metadata']['_continue']

    api_response = workflow_api.workflow_service_list_workflows(namespace='argo',list_options_limit=1)
    api_response = workflow_api.workflow_service_list_workflows(namespace='argo',list_options_limit=1, list_options_continue=continue_token)
    
    pprint(api_response)
    print(continue_token)

    # return api_response
    # try:
    #     workflow_api = workflow_service_api.WorkflowServiceApi(api_client)
    #     api_response = workflow_api.workflow_service_list_workflows(namespace='argo',list_options_limit=1)
        
    #     pprint(api_response)

    #     return api_response['items']
    # except Exception as e:
    #     logger.error(e, exc_info=True)


@router.get("/test")
async def test():
    headers = {'accept': 'text/event-stream', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImZ4VWpBRDVYOS1HYlNEWXhjMHFRNllEejYtaUNGVlFLeDIwYjRTbjY5eVEifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJhcmdvIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImFyZ28tc2VydmVyLXRva2VuLXBqMmJ0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFyZ28tc2VydmVyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiOWNhMDAzODAtZWZhNy00ZTE5LTk0M2EtMjU1Y2Q4MmRmMWM5Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmFyZ286YXJnby1zZXJ2ZXIifQ.DAO_KtpeLIki0axcchCP3U4NsatGSGD5By76hPG1GdM1Pqhq9qwUUI13kpMyK92wyt4x9CVv2YZsmqYS4Vo8Ut891tdhkLdo2EtBuaJv8YTT4YbYyk_iE5A7kLZo_1oBEM1m-87VbAIX-WMn7iYC0FsBcsYAT2m-rxnk72iJ6_wQoLbB-WSnBr_kPpd9d8tDqvAS1ZCh_T205ZBllIMUUNrq9OxoJmN3WbLKZQ7skJGkJSX6d7Jd42TQX0lHMS3gy-lyFq_GtUJeGlzjhisTuH1gmaQuuCmdW7bd3jGQ3i1IlBfchBZERQsnVf8ZYpCfN864uOInERqzkw954RlM5Q'}
    resp = sseclient_get('https://argo-hcptest.skhynix.com/api/v1/stream/events/argo', headers)
    
    return EventSourceResponse(resp)

def sseclient_get(url, headers):
    stream_response = requests.get(url, headers=headers, stream=True)
    client = sseclient.SSEClient(stream_response)

    for event in client.events():
        # logger.debug(event.data)
        yield event.data

@router.get("/test_openapi")
def test():
    try:
        headers = {'accept': 'text/application-json', 'Content-Type': 'text/application-json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImZ4VWpBRDVYOS1HYlNEWXhjMHFRNllEejYtaUNGVlFLeDIwYjRTbjY5eVEifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJhcmdvIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImFyZ28tc2VydmVyLXRva2VuLXBqMmJ0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFyZ28tc2VydmVyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiOWNhMDAzODAtZWZhNy00ZTE5LTk0M2EtMjU1Y2Q4MmRmMWM5Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmFyZ286YXJnby1zZXJ2ZXIifQ.DAO_KtpeLIki0axcchCP3U4NsatGSGD5By76hPG1GdM1Pqhq9qwUUI13kpMyK92wyt4x9CVv2YZsmqYS4Vo8Ut891tdhkLdo2EtBuaJv8YTT4YbYyk_iE5A7kLZo_1oBEM1m-87VbAIX-WMn7iYC0FsBcsYAT2m-rxnk72iJ6_wQoLbB-WSnBr_kPpd9d8tDqvAS1ZCh_T205ZBllIMUUNrq9OxoJmN3WbLKZQ7skJGkJSX6d7Jd42TQX0lHMS3gy-lyFq_GtUJeGlzjhisTuH1gmaQuuCmdW7bd3jGQ3i1IlBfchBZERQsnVf8ZYpCfN864uOInERqzkw954RlM5Q'}
        # resp = requests.get(url='https://argo-hcptest.skhynix.com/api/v1/workflows/argo', headers=headers)
        resp = api_client.call_api(method='GET', resource_path='/api/v1/workflows/argo', header_params=headers, _check_type=False)
        return resp
    except Exception as e:
        logger.error(e, exc_info=True)
