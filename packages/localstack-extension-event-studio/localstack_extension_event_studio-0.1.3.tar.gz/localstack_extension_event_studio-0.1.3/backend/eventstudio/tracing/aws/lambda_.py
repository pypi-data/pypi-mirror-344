_C='payload'
_B='Invoke'
_A='function_name'
import copy,json,logging
from localstack.services.lambda_.api_utils import function_locators_from_arn
from localstack.services.lambda_.event_source_mapping.senders.lambda_sender import LambdaSender
from localstack.services.lambda_.invocation.execution_environment import ExecutionEnvironment
from localstack.services.lambda_.invocation.lambda_models import InvocationResult
from localstack.services.lambda_.invocation.lambda_service import LambdaService
from localstack.services.lambda_.invocation.version_manager import LambdaVersionManager
from localstack.utils.aws.arns import lambda_function_arn,parse_arn
from localstack.utils.patch import Patch
from localstack.utils.strings import long_uid
from eventstudio.db.event_storage import EventStorageService
from eventstudio.tracing.aws.base import Instrumentation
from eventstudio.tracing.context import TraceContext,get_trace_context,set_trace_context
from eventstudio.tracing.request_id_tracing import get_trace_context_from_request_id
from eventstudio.tracing.xray_tracing import extract_aws_trace_header
from eventstudio.types.errors import ErrorType,InputErrorModel
from eventstudio.types.events import InputEventModel
from eventstudio.types.services import ServiceName
from eventstudio.utils.utils import log_event_studio_error
LOG=logging.getLogger(__name__)
class LambdaInstrumentation(Instrumentation):
	def apply(A):Patch.function(LambdaService.invoke,A._invoke_lambda).apply();Patch.function(LambdaVersionManager.store_logs,A._lambda_proxy_capture_invocation_result).apply();Patch.function(LambdaSender.send_events,A._send_events_to_lambda).apply()
	def _invoke_lambda(A,fn,self_,region:str,account_id:str,request_id:str,payload:bytes|None,**E)->dict:
		J=payload;D=request_id;C=account_id;B=region
		try:
			F=get_trace_context();K=F.parent_id;G=F.trace_id;L=F.version;H=E.get(_A);M=lambda_function_arn(H,C,B);N=json.loads(J);O=InputEventModel(parent_id=K,trace_id=G,event_id=D,version=L,account_id=C,region=B,service=ServiceName.LAMBDA,resource_name=H,arn=M,operation_name=_B,is_replayable=True,event_data={_C:N},event_metadata={_A:H});P,G=A.event_storage_service.add_event(InputEventModel.model_validate(O));I=TraceContext(trace_id=G,parent_id=P);set_trace_context(I)
			if(Q:=extract_aws_trace_header(E['trace_context'])):A.event_storage_service.store_xray_trace(xray_trace_id=Q.root,trace_context=I)
			A.event_storage_service.store_request_id(request_id=D,trace_context=I)
		except Exception as R:log_event_studio_error(logger=LOG,service=ServiceName.LAMBDA,operation=_B,error=str(R))
		return fn(self_,payload=J,region=B,account_id=C,request_id=D,**E)
	def _lambda_proxy_capture_invocation_result(B,fn,self_,invocation_result:InvocationResult,execution_env:ExecutionEnvironment)->None:
		D=invocation_result;C=self_
		try:
			E=get_trace_context_from_request_id(D.request_id,B.event_storage_service);H=E.parent_id;F=copy.copy(D);A=F.payload.decode('utf-8')
			if F.is_error:J=InputErrorModel(span_id=H,error_message=A,error_type=ErrorType.EXECUTION_ERROR);B.event_storage_service.add_error(InputErrorModel.model_validate(J))
			else:A=json.loads(A);G=parse_arn(C.function_arn);I=G['resource'].split(':')[1];K=G['region'];L=G['account'];M=InputEventModel(parent_id=H,trace_id=E.trace_id,event_id=f"{F.request_id}-response",version=E.version,account_id=L,region=K,service=ServiceName.LAMBDA,resource_name=I,arn=C.function_arn,operation_name='Response',is_hidden=True,event_data={'response':A},event_metadata={_A:I});N,O=B.event_storage_service.add_event(InputEventModel.model_validate(M));P=TraceContext(trace_id=O,parent_id=N);set_trace_context(P)
		except Exception as Q:log_event_studio_error(logger=LOG,service=ServiceName.LAMBDA,operation=_B,error=str(Q))
		return fn(C,invocation_result=D,execution_env=execution_env)
	def _send_events_to_lambda(E,fn,self_,events:list[dict]|dict,**H)->dict:
		G='EventSourceMapping';B=events;A=self_
		try:C=get_trace_context_from_esm_event(B[0],E.event_storage_service);I=C.parent_id;D=C.trace_id;J=C.version;F,R,K,L=function_locators_from_arn(A.target_arn);M={'Records':B};N=InputEventModel(parent_id=I,trace_id=D,event_id=str(long_uid()),version=J,account_id=K,region=L,service=ServiceName.LAMBDA,resource_name=F,arn=A.target_arn,operation_name=G,is_replayable=True,event_data={_C:M},event_metadata={_A:F});O,D=E.event_storage_service.add_event(InputEventModel.model_validate(N));P=TraceContext(trace_id=D,parent_id=O);set_trace_context(P)
		except Exception as Q:log_event_studio_error(logger=LOG,service=ServiceName.LAMBDA,operation=G,error=str(Q))
		return fn(A,events=B,**H)
def _get_event_id_from_esm_event(esm_event:dict)->str|None:
	A=esm_event
	if(B:=A.get('eventID')):return B
	if(C:=A.get('messageId')):return C
def get_trace_context_from_esm_event(esm_event:dict,event_storage_service:EventStorageService)->TraceContext:
	if(B:=_get_event_id_from_esm_event(esm_event)):
		A=event_storage_service.get_event_by_id(B)
		if A:C=A.span_id;D=A.trace_id;E=A.version;return TraceContext(trace_id=D,parent_id=C,version=E)
	return TraceContext()