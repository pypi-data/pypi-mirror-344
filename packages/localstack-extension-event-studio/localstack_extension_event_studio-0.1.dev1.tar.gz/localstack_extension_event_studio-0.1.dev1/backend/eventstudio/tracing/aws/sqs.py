import logging
from localstack.aws.api.sqs import Message
from localstack.aws.connect import connect_to
from localstack.services.sqs.models import FifoQueue,StandardQueue
from localstack.utils.patch import Patch
from eventstudio.tracing.aws.base import Instrumentation
from eventstudio.tracing.context import TraceContext,get_request_context,get_trace_context,set_trace_context
from eventstudio.types.events import InputEventModel
from eventstudio.types.services import ServiceName
from eventstudio.utils.utils import is_lambda_helper_queue,load_sqs_message_body,log_event_studio_error,pars_timestamp_ms
LOG=logging.getLogger(__name__)
class SQSInstrumentation(Instrumentation):
	def apply(A):Patch.function(StandardQueue.put,A._put_message_sqs_queue).apply();Patch.function(FifoQueue.put,A._put_message_sqs_queue).apply()
	def _put_message_sqs_queue(I,fn,self_,message:Message,**J)->dict:
		H='Send';E=message;A=self_
		try:B=get_trace_context();K=B.parent_id;C=B.trace_id;L=B.version;D=E.copy();M,N=load_sqs_message_body(D['Body']);O=pars_timestamp_ms(list(D['Attributes'].values())[1]);F=get_request_context();P=F.account_id;Q=F.region;G=is_lambda_helper_queue(A.arn,connect_to(region_name=Q,aws_access_key_id=P).lambda_);R=InputEventModel(parent_id=K,trace_id=C,event_id=D.pop('MessageId'),version=L,account_id=A.account_id,region=A.region,service=ServiceName.SQS,resource_name=A.name,arn=A.arn,operation_name=H,is_replayable=True,is_hidden=G if G else False,event_data={'body':M},event_metadata={'queue_arn':A.arn,'body_type':N,'original_time':O});S,C=I.event_storage_service.add_event(InputEventModel.model_validate(R));T=TraceContext(trace_id=C,parent_id=S);set_trace_context(T)
		except Exception as U:log_event_studio_error(logger=LOG,service=ServiceName.SQS,operation=H,error=str(U))
		return fn(A,message=E,**J)