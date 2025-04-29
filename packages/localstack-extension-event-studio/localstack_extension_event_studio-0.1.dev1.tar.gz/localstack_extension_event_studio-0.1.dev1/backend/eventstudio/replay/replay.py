_A=None
import json
from abc import ABC,abstractmethod
from datetime import datetime
from typing import Any
from botocore.client import BaseClient
from localstack.aws.api.events import AccountId,PutEventsRequestEntry,PutEventsResponse
from localstack.aws.connect import connect_to
from eventstudio.constants import INTERNAL_REQUEST_TRACE_HEADER
from eventstudio.db.event_storage import EventStorageService
from eventstudio.tracing.context import TraceContext
from eventstudio.types.errors import ErrorType,InputErrorModel
from eventstudio.types.events import EventModel,RegionName
from eventstudio.types.services import ServiceName
from eventstudio.utils.arns import get_queue_url_from_arn
from eventstudio.utils.utils import dict_to_xml
class ReplayEventSender(ABC):
	service:ServiceName;account_id:AccountId;region:RegionName
	def __init__(A,service:ServiceName,account_id:AccountId,region:RegionName,event_studio_service:EventStorageService):A.service=service;A.account_id=account_id;A.region=region;(A._client):BaseClient|_A=_A;(A._event_studio_service):EventStorageService=event_studio_service
	@property
	def client(self):
		A=self
		if A._client is _A:A._client=A._initialize_client()
		return A._client
	def _initialize_client(A)->BaseClient:B=connect_to(aws_access_key_id=A.account_id,region_name=A.region);C=B.get_client(A.service.value);return C
	def _set_headers(B,event:EventModel):
		A=event
		def C(params:dict[str,Any],context:dict[str,Any],**C):B=TraceContext(trace_id=A.trace_id,parent_id=A.span_id,version=A.version);params['headers'][INTERNAL_REQUEST_TRACE_HEADER]=B.model_dump_json()
		B.client.meta.events.register('before-call.*.*',handler=C)
		def D(exception,**E):
			C=exception
			if C is not _A:D=InputErrorModel(error_type=ErrorType.BOTO_ERROR,error_text=str(C),span_id=A.span_id);B._event_studio_service.add_error(D)
		B.client.meta.events.register('after-call-error',handler=D)
	def replay_event(A,event:EventModel)->dict[str,str]:B=event;A._set_headers(B);return A.send_event(B)
	@abstractmethod
	def send_event(self,event:EventModel)->dict[str,str]:0
class DynamoDBReplayEventSender(ReplayEventSender):
	def send_event(B,event:EventModel)->dict[str,str]:A=event;C=A.event_data;D=A.event_metadata;E=D.table_name;F=C.item;G=B.client.put_item(TableName=E,Item=F);return G
class EventsReplayEventSender(ReplayEventSender):
	def _re_format_event(E,event:EventModel)->PutEventsRequestEntry:
		B=event;A=B.event_data;D=B.event_metadata;C={'Source':A.source,'DetailType':A.detail_type,'Detail':json.dumps(A.detail),'Time':B.creation_time.isoformat()if B.creation_time else datetime.now().isoformat(),'EventBusName':D.event_bus_name}
		if A.resources:C['Resources']=str(A.resources)
		if D.replay_name:C['ReplayName']=A.replay_name
		return PutEventsRequestEntry(**C)
	def send_event(A,event:EventModel)->PutEventsResponse:B=A._re_format_event(event);C=A.client.put_events(Entries=[B]);return C
class LambdaReplayEventSender(ReplayEventSender):
	def send_event(B,event:EventModel)->dict[str,str]:A=event;C=A.event_metadata.function_name;D=A.event_data.payload;E=A.event_metadata.invocation_type;F=B.client.invoke(FunctionName=C,InvocationType=E,Payload=json.dumps(D));return F
class SnsReplayEventSender(ReplayEventSender):
	def send_event(B,event:EventModel)->dict[str,str]:A=event;C=A.event_metadata.topic_arn;D=A.event_data.message.get('message');E=B.client.publish(TopicArn=C,Message=json.dumps(D));return E
class SqsReplayEventSender(ReplayEventSender):
	def send_event(D,event:EventModel)->dict[str,str]:
		A=event;E=get_queue_url_from_arn(A.event_metadata.queue_arn);B=A.event_data.body
		if A.event_metadata.body_type=='TEXT':C=B
		if A.event_metadata.body_type=='JSON':C=json.dumps(B)
		if A.event_metadata.body_type=='XML':C=dict_to_xml(B)
		F=D.client.send_message(QueueUrl=E,MessageBody=C);return F
class S3ReplayEventSender(ReplayEventSender):
	def send_event(E,event:EventModel)->dict[str,str]:
		B=event;F=B.event_data;A=B.event_metadata;C=B.event_bytedata;G=A.bucket;H=A.key
		if A.data_type=='TEXT':D=json.dumps(F.body)
		elif A.data_type=='BINARY'and C:D=C
		else:return{'error':'Invalid data type'}
		I=E.client.put_object(Bucket=G,Key=H,Body=D);return I
class ReplayEventSenderFactory:
	service:ServiceName;account_id:AccountId;region:RegionName;service_map={ServiceName.DYNAMODB:DynamoDBReplayEventSender,ServiceName.EVENTS:EventsReplayEventSender,ServiceName.LAMBDA:LambdaReplayEventSender,ServiceName.SNS:SnsReplayEventSender,ServiceName.SQS:SqsReplayEventSender,ServiceName.S3:S3ReplayEventSender}
	def __init__(A,service:ServiceName,account_id:AccountId,region:RegionName,event_studio_service:EventStorageService):A.service=service;A.account_id=account_id;A.region=region;(A.event_studio_service):EventStorageService=event_studio_service
	def get_sender(A)->ReplayEventSender:return A.service_map[A.service](service=A.service,account_id=A.account_id,region=A.region,event_studio_service=A.event_studio_service)