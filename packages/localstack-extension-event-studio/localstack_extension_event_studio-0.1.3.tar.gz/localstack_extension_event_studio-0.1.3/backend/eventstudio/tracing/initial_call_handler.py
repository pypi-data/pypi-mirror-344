_A='PutObject'
import logging
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
	def __call__(L,chain:HandlerChain,context:RequestContext,response:Response):
		K='InitialCall';J='external';C=None;A=context;B=A.service.service_name;F=A.service_operation.operation
		if B in SERVICE_NAME_VALUES and F in SERVICE_OPERATIONS_TO_CAPTURE_BY_SERVICE.get(B,[])and not skip_specific_operations(A):
			try:
				D=get_trace_context();M=D.parent_id;E=D.trace_id;N=D.version
				if(not A.is_internal_call or(M is C or E is C))and not is_request_from_lambda(A):
					if A.is_internal_call:G=ServiceName.INTERNAL;O=get_service_name(B);H='internal';I={'service':O,'operation_name':F}
					else:G=ServiceName.EXTERNAL;H=J;I={'user_agent':A.request.user_agent.string,'browser':A.request.user_agent.browser,'language':A.request.user_agent.language,'platform':A.request.user_agent.platform,'version':A.request.user_agent.version}
					P=InputEventModel(parent_id=C,trace_id=C,event_id=A.request_id,version=N,account_id=A.account_id,region=A.region,service=G,resource_name=H,arn=J,operation_name=K,event_metadata=I);Q,E=L._event_storage_service.add_event(InputEventModel.model_validate(P));R=TraceContext(trace_id=E,parent_id=Q);set_trace_context(R)
			except Exception as S:log_event_studio_error(logger=LOG,service=get_service_name(B),operation=K,error=str(S))