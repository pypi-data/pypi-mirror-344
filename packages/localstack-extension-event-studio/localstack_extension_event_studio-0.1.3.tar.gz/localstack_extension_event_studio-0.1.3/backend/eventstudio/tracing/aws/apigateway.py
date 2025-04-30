_A=None
import logging
from localstack.services.apigateway.next_gen.execute_api.context import RestApiInvocationContext
from localstack.services.apigateway.next_gen.execute_api.integrations.aws import RestApiAwsProxyIntegration
from localstack.utils.aws.arns import apigateway_restapi_arn
from localstack.utils.patch import Patch
from localstack.utils.xray.trace_header import TraceHeader
from eventstudio.tracing.aws.base import Instrumentation
from eventstudio.tracing.context import TraceContext,set_trace_context
from eventstudio.tracing.xray_tracing import get_trace_context_from_xray_trace_header
from eventstudio.types.events import InputEventModel
from eventstudio.types.services import ServiceName
from eventstudio.utils.utils import is_internal_call,load_apigateway_body,log_event_studio_error
LOG=logging.getLogger(__name__)
class ApigatewayInstrumentation(Instrumentation):
	def apply(A):Patch.function(RestApiAwsProxyIntegration.invoke,A._invoke_apigateway).apply()
	def _invoke_apigateway(C,fn,self_,context:RestApiInvocationContext,**Z)->_A:
		Y='requestId';X='Invoke';W='<binary data>';V='BINARY';U='body';T='headers';O=self_;A=context
		try:
			F=get_trace_context_from_xray_trace_header(A,C.event_storage_service);G=F.parent_id;B=F.trace_id;P=F.version;H=A.invocation_request.copy();D=A.deployment.rest_api.rest_api.get('name');I=A.account_id;J=A.region;a=apigateway_restapi_arn(D,I,J);H.pop(T,_A);K,b=load_apigateway_body(H.pop(U,_A))
			if b==V:E=K;K=W
			else:E=_A
			L=A.integration_request.copy();L.pop(T,_A);M,Q=load_apigateway_body(L.pop(U,_A))
			if Q==V:E=M;M=W
			else:E=_A
			if not G and not B:
				if is_internal_call(A):c=ServiceName.INTERNAL;R={'service':c,'operation_name':X}
				else:d=ServiceName.EXTERNAL;R={'user_agent':A.request.user_agent.string,'browser':A.request.user_agent.browser,'language':A.request.user_agent.language,'platform':A.request.user_agent.platform,'version':A.request.user_agent.version}
				N=InputEventModel(parent_id=_A,trace_id=_A,event_id=A.context_variables.get(Y),version=P,account_id=I,region=J,service=d,resource_name=D,arn='external',operation_name='InitialCall',event_metadata=R);G,B=C.event_storage_service.add_event(InputEventModel.model_validate(N))
			N=InputEventModel(parent_id=G,trace_id=B,event_id=A.context_variables.get(Y),version=P,account_id=I,region=J,service=ServiceName.APIGATEWAY,resource_name=D,arn=a,operation_name='Request',is_replayable=True,event_data={'invocation_request_body':K,'integration_request_body':M,'invocation_request':H,'integration_request':L},event_bytedata=E,event_metadata={'api_type':O.name,'api_name':D,'deployment_id':A.deployment_id,'stage_name':A.stage,'body_type':Q});e,B=C.event_storage_service.add_event(InputEventModel.model_validate(N));S=TraceContext(trace_id=B,parent_id=e);set_trace_context(S)
			if(f:=A.trace_id):g=TraceHeader.from_header_str(f).ensure_root_exists();C.event_storage_service.store_xray_trace(xray_trace_id=g.root,trace_context=S)
		except Exception as h:log_event_studio_error(logger=LOG,service=ServiceName.APIGATEWAY,operation=X,error=str(h))
		return fn(O,context=A,**Z)