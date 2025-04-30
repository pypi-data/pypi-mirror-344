_A=None
import logging
from localstack.aws.api import RequestContext
from localstack.utils.xray.trace_header import TraceHeader
from eventstudio.db.event_storage import EventStorageService
from eventstudio.tracing.context import TraceContext
from eventstudio.utils.utils import compile_regex_patterns
LOG=logging.getLogger(__name__)
XRAY_TRACE_HEADER_PATTERNS=compile_regex_patterns(['Root=([^;]+)'])
XRAY_TRACE_HEADER='X-Amzn-Trace-Id'
def get_trace_context_from_xray_trace_header(context:RequestContext,event_storage_service:EventStorageService)->TraceContext|_A:
	A=next((A[1]for A in context.request.headers if A[0]==XRAY_TRACE_HEADER),_A)
	if not A:return TraceContext()
	try:
		if(D:=extract_xray_trace_id_from_xray_trace_header_str(A)):
			B,C=event_storage_service.get_trace_from_xray_trace(D)
			if B and C:return TraceContext(trace_id=B,parent_id=C)
	except(IndexError,AttributeError,TypeError):pass
	return TraceContext()
def extract_xray_trace_id_from_xray_trace_header_str(xray_header:str)->str|_A:
	try:
		if(B:=XRAY_TRACE_HEADER_PATTERNS[0].search(xray_header)):C=B.group(1);return C
		else:LOG.debug('No X-Ray trace ID found in X-Ray trace header');return
	except KeyError as A:LOG.warning(f"Missing required field in X-Ray trace header: {A}");return
	except Exception as A:LOG.warning(f"Error extracting X-Ray trace ID: {A}");return
def extract_aws_trace_header(trace_context:dict)->TraceHeader|_A:
	try:
		B=trace_context.get('aws_trace_header')
		if not B:LOG.debug('No AWS trace header found in trace context');return
		return B
	except KeyError as A:LOG.warning(f"Missing required field in AWS trace header: {A}");return
	except Exception as A:LOG.warning(f"Error extracting AWS trace header: {A}");return