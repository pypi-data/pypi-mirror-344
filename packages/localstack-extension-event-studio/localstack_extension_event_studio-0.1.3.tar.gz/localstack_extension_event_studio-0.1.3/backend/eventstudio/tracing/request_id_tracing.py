from eventstudio.db.event_storage import EventStorageService
from eventstudio.tracing.context import TraceContext
def get_trace_context_from_request_id(request_id:str|None,event_storage_service:EventStorageService)->TraceContext|None:
	A=request_id
	if not A:return TraceContext()
	try:
		B,C=event_storage_service.get_trace_from_request_id(A)
		if B and C:return TraceContext(trace_id=B,parent_id=C)
	except(IndexError,AttributeError,TypeError):pass
	return TraceContext()