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
from eventstudio.types.errors import ErrorType,InputErrorModel
from eventstudio.types.events import InputEventModel
from eventstudio.types.services import ServiceName
from eventstudio.utils.utils import log_event_studio_error
from eventstudio.utils.xray_tracing_utils import extract_aws_trace_header
LOG=logging.getLogger(__name__)
class LambdaInstrumentation(Instrumentation):
	def apply(A):Patch.function(LambdaService.invoke,A._invoke_lambda).apply();Patch.function(LambdaVersionManager.store_logs,A._lambda_proxy_capture_invocation_result).apply();Patch.function(LambdaSender.send_events,A._send_events_to_lambda).apply()
	def _invoke_lambda(G,fn,self_,region:str,account_id:str,request_id:str,payload:bytes|None,**C)->dict:
		I=payload;H=request_id;B=account_id;A=region
		try:
			D=get_trace_context();K=D.parent_id;E=D.trace_id;L=D.version;F=C.get(_A);M=lambda_function_arn(F,B,A);N=json.loads(I);O=InputEventModel(parent_id=K,trace_id=E,event_id=H,version=L,account_id=B,region=A,service=ServiceName.LAMBDA,resource_name=F,arn=M,operation_name=_B,is_replayable=True,event_data={_C:N},event_metadata={_A:F});P,E=G.event_storage_service.add_event(InputEventModel.model_validate(O));J=TraceContext(trace_id=E,parent_id=P);set_trace_context(J)
			if(Q:=extract_aws_trace_header(C['trace_context'])):G.event_storage_service.store_xray_trace(xray_trace_id=Q.root,trace_context=J)
		except Exception as R:log_event_studio_error(logger=LOG,service=ServiceName.LAMBDA,operation=_B,error=str(R))
		return fn(self_,payload=I,region=A,account_id=B,request_id=H,**C)
	def _lambda_proxy_capture_invocation_result(F,fn,self_,invocation_result:InvocationResult,execution_env:ExecutionEnvironment)->None:
		G=invocation_result;B=self_
		try:
			C=get_trace_context();H=C.parent_id;D=copy.copy(G);A=D.payload.decode('utf-8')
			if D.is_error:J=InputErrorModel(span_id=H,error_message=A,error_type=ErrorType.EXECUTION_ERROR);F.event_storage_service.add_error(InputErrorModel.model_validate(J))
			else:A=json.loads(A);E=parse_arn(B.function_arn);I=E['resource'].split(':')[1];K=E['region'];L=E['account'];M=InputEventModel(parent_id=H,trace_id=C.trace_id,event_id=D.request_id,version=C.version,account_id=L,region=K,service=ServiceName.LAMBDA,resource_name=I,arn=B.function_arn,operation_name='Response',is_replayable=True,event_data={'response':A},event_metadata={_A:I});F.event_storage_service.add_event(InputEventModel.model_validate(M))
		except Exception as N:log_event_studio_error(logger=LOG,service=ServiceName.LAMBDA,operation=_B,error=str(N))
		return fn(B,invocation_result=G,execution_env=execution_env)
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