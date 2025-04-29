_A=None
import json,logging
from eventstudio.constants import LOG_MESSAGES_TO_CAPTURE
from eventstudio.db.event_storage import EventStorageService
from eventstudio.tracing.context import get_trace_context
from eventstudio.types.errors import ErrorType,InputErrorModel
from eventstudio.utils.errors import get_error_type
LOG=logging.getLogger(__name__)
class EventStudioLogHandler(logging.Handler):
	def __init__(A,event_storage_service:EventStorageService)->_A:logging.Handler.__init__(self=A);A._event_storage_service=event_storage_service
	def emit(B,record:logging.LogRecord)->_A:
		A=record
		if A.levelno>=logging.ERROR:B._process_log_error(A)
		elif any(B in A.getMessage()for B in LOG_MESSAGES_TO_CAPTURE):B._process_log_error(A)
	def _process_log_error(B,record:logging.LogRecord)->_A:
		A=get_trace_context()
		if A.parent_id is not _A:B._create_error_record(record,A.parent_id)
	def _create_error_record(F,record:logging.LogRecord,span_id:str)->_A:
		A=record.getMessage();B=ErrorType.LOCALSTACK_ERROR;C=_A
		try:
			D=json.loads(A)
			if(E:=D.get('ErrorCode')):
				B=get_error_type(E)
				if B is ErrorType.EVENTSTUDIO_ERROR:return
				C=E;A=D['ErrorMessage']
			elif(G:=D.get('InfoCode')):B=ErrorType.LOCALSTACK_WARNING;C=G;A=D['InfoMessage']
			if C:A=f"{C}: {A}"
		except json.JSONDecodeError:pass
		H=InputErrorModel(span_id=span_id,error_message=A,error_type=B);F._event_storage_service.add_error(InputErrorModel.model_validate(H))