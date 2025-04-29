_A=None
import logging,os,typing as t
from pathlib import Path
from typing import Any
from botocore.client import BaseClient
from localstack.aws import handlers
from localstack.aws.api import RequestContext
from localstack.aws.chain import HandlerChain
from localstack.aws.connect import InternalClientFactory
from localstack.aws.gateway import Gateway
from localstack.aws.handlers.cors import ALLOWED_CORS_ORIGINS
from localstack.config import is_in_docker
from localstack.extensions.patterns.webapp import WebAppExtension
from localstack.http import Response
from localstack.runtime import get_current_runtime
from localstack.utils.patch import Patch
from eventstudio import config
from eventstudio.api.event_streamer import EventStreamer
from eventstudio.api.web import WebApp
from eventstudio.constants import INTERNAL_REQUEST_TRACE_HEADER
from eventstudio.db.event_storage import EventStorageService
from eventstudio.tracing.aws.apigateway import ApigatewayInstrumentation
from eventstudio.tracing.aws.base import Instrumentation
from eventstudio.tracing.aws.dynamodb import DynamoDBInstrumentation
from eventstudio.tracing.aws.events import EventsInstrumentation
from eventstudio.tracing.aws.iam import IAMInstrumentation
from eventstudio.tracing.aws.lambda_ import LambdaInstrumentation
from eventstudio.tracing.aws.s3 import S3Instrumentation
from eventstudio.tracing.aws.sns import SNSInstrumentation
from eventstudio.tracing.aws.sqs import SQSInstrumentation
from eventstudio.tracing.context import extract_trace_context_from_context,get_trace_context,pop_request_context,push_request_context,set_trace_context
from eventstudio.tracing.initial_call_handler import EventStudioInitialCallHandler
from eventstudio.tracing.logging_handler import EventStudioLogHandler
from eventstudio.types.errors import ErrorType,InputErrorModel
from eventstudio.utils.xray_tracing_utils import get_trace_context_from_xray_trace_header
LOG=logging.getLogger(__name__)
class MyExtension(WebAppExtension):
	name='eventstudio';aws_instrumentations:list[t.Type[Instrumentation]]=[ApigatewayInstrumentation,DynamoDBInstrumentation,EventsInstrumentation,IAMInstrumentation,LambdaInstrumentation,S3Instrumentation,SNSInstrumentation,SQSInstrumentation]
	def __init__(A):
		super().__init__(template_package_path=_A);A.db_path=config.DATABASE_PATH
		if not is_in_docker:ALLOWED_CORS_ORIGINS.append('http://127.0.0.1:3000')
		if is_in_docker:
			B=Path('/var/lib/localstack/cache/extensions/eventstudio')
			if not B.is_dir():B.mkdir(parents=True)
			A.clear_db();A.db_path=B/config.DATABASE_NAME
		(A._event_streamer):EventStreamer=EventStreamer();(A._event_storage_service):EventStorageService=EventStorageService(db_path=A.db_path,event_streamer=A._event_streamer)
	def set_thread_local_trace_parameters_from_context(C,_chain:HandlerChain,context:RequestContext,_response:Response):
		B=context;A=extract_trace_context_from_context(B)
		if A.parent_id is _A:
			A=get_trace_context_from_xray_trace_header(B,C._event_storage_service)
			if A is _A or A.parent_id is _A:A=get_trace_context()
		set_trace_context(A)
	def _get_client_post_hook_with_trace_header(C,fn,self_,client:BaseClient,**B):
		A=client;A.meta.events.register('before-call.*.*',handler=_handler_inject_trace_header)
		def D(exception,**F):
			A=exception
			if A is not _A:
				D=get_trace_context();B=D.parent_id
				if B is not _A:E=InputErrorModel(error_type=ErrorType.BOTO_ERROR,error_message=str(A),span_id=B);C._event_storage_service.add_error(E)
		A.meta.events.register('after-call-error',handler=D);return fn(self_,client=A,**B)
	def _inject_request_context_handlers(D,gateway:Gateway):
		A=gateway
		def B(_chain:HandlerChain,context:RequestContext,_response:Response):push_request_context(context)
		def C(_chain:HandlerChain,_context:RequestContext,_response:Response):pop_request_context()
		A.request_handlers.insert(0,B);A.finalizers.append(C)
	def on_platform_ready(A):
		super().on_platform_ready()
		for C in A.aws_instrumentations:C(A._event_storage_service).apply()
		A._inject_request_context_handlers(get_current_runtime().components.gateway);handlers.serve_custom_service_request_handlers.append(A.set_thread_local_trace_parameters_from_context);Patch.function(InternalClientFactory._get_client_post_hook,A._get_client_post_hook_with_trace_header).apply();D=EventStudioInitialCallHandler(event_storage_service=A._event_storage_service);handlers.serve_custom_service_request_handlers.append(D);B=EventStudioLogHandler(event_storage_service=A._event_storage_service);B.setLevel(logging.INFO);E=logging.getLogger();E.addHandler(B);LOG.info('Extension Loaded')
	def collect_routes(A,routes:list[t.Any]):routes.append(WebApp(event_storage_service=A._event_storage_service,event_streamer=A._event_streamer))
	def clear_db(A):
		if config.PERSISTENCE and is_in_docker and os.path.exists(A.db_path):os.remove(A.db_path);LOG.info('EventStudio database removed')
	def on_platform_shutdown(A):A._event_storage_service.close_connection();A.clear_db()
def _handler_inject_trace_header(params:dict[str,Any],context:dict[str,Any],**B):
	A=get_trace_context()
	if A.trace_id and A.parent_id:params['headers'][INTERNAL_REQUEST_TRACE_HEADER]=A.json()