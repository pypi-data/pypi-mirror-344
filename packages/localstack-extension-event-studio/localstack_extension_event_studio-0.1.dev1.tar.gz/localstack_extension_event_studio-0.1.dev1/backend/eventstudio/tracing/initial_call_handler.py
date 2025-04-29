_A='PutObject'
import logging
from datetime import datetime,timezone
from localstack.aws.api import RequestContext
from localstack.aws.chain import HandlerChain
from localstack.http import Response
from eventstudio.tracing.context import TraceContext,get_trace_context,set_trace_context
from eventstudio.types.events import InputEventModel
from eventstudio.types.services import SERVICE_NAME_VALUES,ServiceName
from eventstudio.utils.utils import get_service_name,log_event_studio_error
LOG=logging.getLogger(__name__)
SERVICE_OPERATIONS_TO_CAPTURE_BY_SERVICE={ServiceName.EVENTS.value:['PutEvents'],ServiceName.DYNAMODB.value:['PutItem'],ServiceName.LAMBDA.value:['Invoke'],ServiceName.S3.value:[_A],ServiceName.SNS.value:['Publish'],ServiceName.SQS.value:['SendMessage']}
def skip_specific_operations(context:RequestContext)->bool:
	A=context;C=A.service.service_name;D=A.service_operation.operation
	if C==ServiceName.S3.value and D==_A:
		B=A.service_request.get('Bucket')
		if B and B.startswith('awslambda')and B.endswith('tasks'):return True
	return False
def is_request_from_lambda(context:RequestContext)->bool:
	B=context.request.environ['HTTP_USER_AGENT'];C=B.split();A=False
	for D in C:
		if D.startswith('exec-env/AWS_Lambda'):A=True;break
	return A
class EventStudioInitialCallHandler:
	def __init__(A,event_storage_service):A._event_storage_service=event_storage_service
	def __call__(I,chain:HandlerChain,context:RequestContext,response:Response):
		H='InitialCall';C=None;A=context;B=A.service.service_name;F=A.service_operation.operation
		if B in SERVICE_NAME_VALUES and F in SERVICE_OPERATIONS_TO_CAPTURE_BY_SERVICE.get(B,[])and not skip_specific_operations(A):
			try:
				D=get_trace_context();J=D.parent_id;E=D.trace_id;K=D.version
				if(not A.is_internal_call or(J is C or E is C))and not is_request_from_lambda(A):
					if A.is_internal_call:L=get_service_name(B);G={'service':L,'operation_name':F}
					else:M=ServiceName.EXTERNAL;G={'user_agent':A.request.user_agent.string,'browser':A.request.user_agent.browser,'language':A.request.user_agent.language,'platform':A.request.user_agent.platform,'version':A.request.user_agent.version}
					N=InputEventModel(parent_id=C,trace_id=C,event_id=A.request_id,version=K,account_id=A.account_id,region=A.region,service=M,resource_name=B,arn='external',operation_name=H,event_metadata=G,creation_time=datetime.now(tz=timezone.utc));O,E=I._event_storage_service.add_event(InputEventModel.model_validate(N));P=TraceContext(trace_id=E,parent_id=O);set_trace_context(P)
			except Exception as Q:log_event_studio_error(logger=LOG,service=get_service_name(B),operation=H,error=str(Q))