_C='DELETE'
_B=None
_A='GET'
import logging,botocore.exceptions
from botocore.client import BaseClient
from localstack.aws.api.events import AccountId
from localstack.http import Request,Response,route
from eventstudio import config,static
from eventstudio.api.event_streamer import EventStreamer
from eventstudio.db.event_storage import EventStorageService
from eventstudio.replay.replay import ReplayEventSender,ReplayEventSenderFactory
from eventstudio.types.errors import ErrorType,InputErrorModel
from eventstudio.types.events import EventModel,EventModelList,InputEventModel,InputEventModelList,RegionName
from eventstudio.types.requests import DeleteEventsRequest
from eventstudio.types.responses import AddEventsResponse,DeleteAllEventsResponse,DeleteEventsResponse,GetEventResponse,ListEventsResponse,ReplayEventsResponse,TraceGraphResponse
from eventstudio.types.services import ServiceName
from eventstudio.utils.utils import parse_request_body
LOG=logging.getLogger(__name__)
class WebApp:
	def __init__(A,event_storage_service:EventStorageService,event_streamer:EventStreamer):(A._event_storage_service):EventStorageService=event_storage_service;(A._clients):dict[tuple[AccountId,RegionName],BaseClient]={};A._replay_event_sender_store={};A._event_streamer=event_streamer
	@route('/')
	def index(self,request:Request,*A,**B):return Response.for_resource(static,'index.html')
	@route('/<path:path>')
	def index2(self,request:Request,path:str,**A):return Response.for_resource(static,path)
	@route(config.get_relative_url(config.EVENTS),methods=['WEBSOCKET'])
	def live_stream(self,request,*A,**B):return self._event_streamer.on_websocket_request(request,*A,**B)
	@route(config.get_relative_url(config.EVENTS),methods=['POST'])
	def add_events(self,request:Request,events:InputEventModelList)->AddEventsResponse:
		A=0;C=[]
		for D in events.events:
			B=self._event_storage_service.add_event(D)
			if isinstance(B,dict)and'error'in B:A+=1;C.append(B.error)
		if A>0:return AddEventsResponse(status=400,FailedEntryCount=A,FailedEntries=C)
		return AddEventsResponse(status=200,FailedEntryCount=0,FailedEntries=[])
	@route(config.get_relative_url(config.EVENTS),methods=[_C])
	def delete_events(self,request:Request)->DeleteEventsResponse:
		D=parse_request_body(request,DeleteEventsRequest);A=0;B=[]
		for E in D.span_ids:
			C=self._event_storage_service.delete_event(span_id=E)
			if C:A+=1;B.append(C)
		if A>0:return DeleteEventsResponse(status=400,FailedEntryCount=A,FailedEntries=B)
		return DeleteEventsResponse(status=200,FailedEntryCount=0,FailedEntries=[])
	@route(config.get_relative_url(config.ALL_EVENTS),methods=[_C])
	def delete_all_events(self,request:Request)->DeleteAllEventsResponse:
		A=self._event_storage_service.delete_all_events()
		if A:return DeleteAllEventsResponse(status=400,error=A.get('error'))
		return DeleteAllEventsResponse(status=200)
	@route(config.get_relative_url(config.EVENTS),methods=[_A])
	def list_events(self,request:Request)->ListEventsResponse:
		try:B=self._event_storage_service.list_events()
		except Exception as A:LOG.error(f"Failed to list events: {A}");return ListEventsResponse(status=400,error=f"Error occurred while fetching all events: {A}")
		return ListEventsResponse(status=200,events=B)
	@route(f"{config.get_relative_url(config.EVENTS)}/<span_id>",methods=[_A])
	def get_event_details(self,request:Request,span_id:str):
		A=span_id
		try:
			B=self._event_storage_service.get_event(A)
			if not B:return GetEventResponse(status=404,error=f"Event with span_id {A} not found.")
			return GetEventResponse(status=200,event=B.dict())
		except Exception as C:LOG.error('Failed to get event with span_id %s: %s',A,C);return GetEventResponse(status=400,error=f"Error occurred while fetching the event: {C}")
	@route(f"{config.get_relative_url(config.TRACES)}/<trace_id>",methods=[_A])
	def get_trace_graph(self,request:Request,trace_id:str)->TraceGraphResponse:
		A=self._event_storage_service.get_event_graph(trace_id=trace_id)
		if A is _B:return TraceGraphResponse(status=404)
		return TraceGraphResponse(status=200,event=A)
	@route(config.get_relative_url(config.REPLAY),methods=['POST'])
	def replay_events(self,request:Request,event_list:EventModelList)->ReplayEventsResponse:
		D=self;E=0;G=[]
		for C in event_list.events:
			if not C.is_replayable:E+=1;G.append(C);continue
			H=D._event_storage_service.get_event(span_id=C.span_id);I=C.model_dump();J=H.model_dump();K={**J,**{B:A for(B,A)in I.items()if A is not _B}};A=InputEventModel(**K)
			if A.version==0:A.parent_id=C.span_id
			A.operation_name='replay_event';A.version+=1;A.is_replayable=False;L,P=D._event_storage_service.add_event(InputEventModel.model_validate(A));B=EventModel(**A.model_dump(),span_id=L);M=D.get_replay_event_sender(service=B.service,account_id=B.account_id,region=B.region)
			try:F=M.replay_event(event=B)
			except(botocore.exceptions.ParamValidationError,botocore.exceptions.ClientError)as N:O=InputErrorModel(span_id=B.span_id,error_message=str(N),error_type=ErrorType.BOTO_ERROR);D._event_storage_service.add_error(InputErrorModel.model_validate(O));F=_B
			if F and F.get('ResponseMetadata',{}).get('HTTPStatusCode')!=200 or F is _B:E+=1;G.append(B)
		if E>0:return ReplayEventsResponse(status=400,FailedEntryCount=E,FailedEntries=G)
		return ReplayEventsResponse(status=200,FailedEntryCount=0,FailedEntries=[])
	@route(config.get_relative_url_v2(config.EVENTS),methods=[_A])
	def list_events_v2(self,request:Request)->ListEventsResponse:
		try:B=self._event_storage_service.list_events_v2()
		except Exception as A:LOG.error(f"Failed to list events: {A}");return ListEventsResponse(status=400,error=f"Error occurred while fetching all events: {A}")
		return ListEventsResponse(status=200,events=B)
	def get_replay_event_sender(A,service:ServiceName,account_id:AccountId,region:RegionName)->ReplayEventSender:D=region;C=account_id;B=service;E=ReplayEventSenderFactory(B,C,D,A._event_storage_service).get_sender();A._replay_event_sender_store[B,C,D]=E;return E