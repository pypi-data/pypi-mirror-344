_A=None
import logging
from datetime import datetime,timezone
from localstack.services.apigateway.next_gen.execute_api.context import RestApiInvocationContext
from localstack.services.apigateway.next_gen.execute_api.integrations.aws import RestApiAwsProxyIntegration
from localstack.utils.aws.arns import apigateway_restapi_arn
from localstack.utils.patch import Patch
from localstack.utils.xray.trace_header import TraceHeader
from eventstudio.tracing.aws.base import Instrumentation
from eventstudio.tracing.context import TraceContext,set_trace_context
from eventstudio.types.events import InputEventModel
from eventstudio.types.services import ServiceName
from eventstudio.utils.utils import is_internal_call,load_apigateway_body,log_event_studio_error
from eventstudio.utils.xray_tracing_utils import get_trace_context_from_xray_trace_header
LOG=logging.getLogger(__name__)
class ApigatewayInstrumentation(Instrumentation):
	def apply(A):Patch.function(RestApiAwsProxyIntegration.invoke,A._invoke_apigateway).apply()
	def _invoke_apigateway(E,fn,self_,context:RestApiInvocationContext,**h)->_A:
		g='body_type';f='request_type';e='stage_name';d='deployment_id';c='api_name';b='api_type';a='request';Z='<binary data>';Y='BINARY';X='headers';U='requestId';T='Invoke';L=self_;K='body';A=context
		try:
			M=get_trace_context_from_xray_trace_header(A,E.event_storage_service);N=M.parent_id;B=M.trace_id;O=M.version;P=A.invocation_request.copy();D=A.deployment.rest_api.rest_api.get('name');I=A.account_id;J=A.region;Q=apigateway_restapi_arn(D,I,J);P.pop(X,_A);C,F=load_apigateway_body(P.pop(K,_A))
			if F==Y:G=C;C=Z
			else:G=_A
			if not N and not B:
				if is_internal_call(A):i=ServiceName.INTERNAL;V={'service':i,'operation_name':T}
				else:j=ServiceName.EXTERNAL;V={'user_agent':A.request.user_agent.string,'browser':A.request.user_agent.browser,'language':A.request.user_agent.language,'platform':A.request.user_agent.platform,'version':A.request.user_agent.version}
				H=InputEventModel(parent_id=_A,trace_id=_A,event_id=A.context_variables.get(U),version=O,account_id=I,region=J,service=j,resource_name=D,arn=Q,operation_name='InitialCall',event_metadata=V,creation_time=datetime.now(tz=timezone.utc));N,B=E.event_storage_service.add_event(InputEventModel.model_validate(H))
			H=InputEventModel(parent_id=N,trace_id=B,event_id=A.context_variables.get(U),version=O,account_id=I,region=J,service=ServiceName.APIGATEWAY,resource_name=D,arn=Q,operation_name='Input',is_replayable=True,event_data={K:C,a:P},event_bytedata=G,event_metadata={b:L.name,c:D,d:A.deployment_id,e:A.stage,f:'invocation',g:F});R,B=E.event_storage_service.add_event(InputEventModel.model_validate(H));S=A.integration_request.copy();S.pop(X,_A);C,F=load_apigateway_body(S.pop(K,_A))
			if F==Y:G=C;C=Z
			else:G=_A
			H=InputEventModel(parent_id=R,trace_id=B,event_id=A.context_variables.get(U),version=O,account_id=I,region=J,service=ServiceName.APIGATEWAY,resource_name=D,arn=Q,operation_name=T,is_replayable=True,event_data={K:C,a:S},event_bytedata=G,event_metadata={b:L.name,c:D,d:A.deployment_id,e:A.stage,f:'integration',g:F});R,B=E.event_storage_service.add_event(InputEventModel.model_validate(H));W=TraceContext(trace_id=B,parent_id=R);set_trace_context(W)
			if(k:=A.trace_id):l=TraceHeader.from_header_str(k).ensure_root_exists();E.event_storage_service.store_xray_trace(xray_trace_id=l.root,trace_context=W)
		except Exception as m:log_event_studio_error(logger=LOG,service=ServiceName.APIGATEWAY,operation=T,error=str(m))
		return fn(L,context=A,**h)