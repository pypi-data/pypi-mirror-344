import io,logging,uuid
from localstack.aws.api import RequestContext
from localstack.aws.api.s3 import PutObjectRequest
from localstack.services.s3.notifications import S3EventNotificationContext
from localstack.services.s3.provider import S3Provider
from localstack.utils.patch import Patch
from eventstudio.tracing.aws.base import Instrumentation
from eventstudio.tracing.context import TraceContext,get_trace_context,set_trace_context,submit_with_trace_context
from eventstudio.types.events import InputEventModel
from eventstudio.types.services import ServiceName
from eventstudio.utils.utils import compile_regex_patterns,log_event_studio_error
LOG=logging.getLogger(__name__)
IGNORE_BUCKET_PATTERNS=compile_regex_patterns(['awslambda-.*-tasks'])
class S3Instrumentation(Instrumentation):
	def apply(A):Patch.function(S3Provider.put_object,A._put_object_s3_bucket).apply()
	def _put_object_s3_bucket(O,fn,self_,context:RequestContext,request:PutObjectRequest,**H)->dict:
		N='Put';M='Body';G=self_;B=context;A=request
		try:
			C=A.get('Bucket')
			if any(A.match(C)for A in IGNORE_BUCKET_PATTERNS):return fn(G,context=B,request=A,**H)
			D=get_trace_context();P=D.parent_id;E=D.trace_id;Q=D.version;I=A['Key'];F:bytes=A.get(M).read()
			try:J=F.decode('utf-8');K=None;L='TEXT'
			except UnicodeDecodeError:J='<binary data>';K=F;L='BINARY'
			R=InputEventModel(parent_id=P,trace_id=E,event_id=uuid.uuid4().hex,version=Q,account_id=B.account_id,region=B.region,service=ServiceName.S3,resource_name=C,arn=f"arn:aws:s3:::{C}/{I}",operation_name=N,is_replayable=True,event_data={'body':J},event_bytedata=K,event_metadata={'bucket':C,'key':I,'data_type':L});S,E=O.event_storage_service.add_event(InputEventModel.model_validate(R));T=TraceContext(trace_id=E,parent_id=S);set_trace_context(T);A[M]=io.BytesIO(F)
		except Exception as U:log_event_studio_error(logger=LOG,service=ServiceName.S3,operation=N,error=str(U))
		return fn(G,context=B,request=A,**H)
	def _submit_s3_notification_with_context(A,fn,self_,notifier,ctx:S3EventNotificationContext,config):return submit_with_trace_context(self_._executor,notifier.notify,ctx,config)