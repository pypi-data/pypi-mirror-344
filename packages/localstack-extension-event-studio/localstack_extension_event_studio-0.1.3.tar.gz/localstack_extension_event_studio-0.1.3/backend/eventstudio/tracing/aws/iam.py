import json,logging
from localstack.aws.api import RequestContext
from localstack.pro.core.services.iam.policy_engine.engine import EvaluationCallback,IAMEnforcementEngine
from localstack.pro.core.services.iam.policy_engine.models import PolicyEvaluationResult
from eventstudio.db.event_storage import EventStorageService
from eventstudio.tracing.aws.base import Instrumentation
from eventstudio.tracing.context import extract_trace_context_from_context
from eventstudio.types.errors import ErrorType,InputErrorModel
LOG=logging.getLogger(__name__)
class IAMInstrumentation(Instrumentation):
	def apply(A):B=EventStudioIAMCallback(event_storage_service=A.event_storage_service);IAMEnforcementEngine.get().add_callback(B)
class EventStudioIAMCallback(EvaluationCallback):
	def __init__(A,event_storage_service:EventStorageService)->None:(A._event_storage_service):EventStorageService=event_storage_service
	def __call__(D,evaluation_result:PolicyEvaluationResult,context:RequestContext):
		B=context;A=evaluation_result
		if A.allowed:return
		C=extract_trace_context_from_context(B)
		if C.parent_id is None:return
		E="Request for service '{}' for operation '{}' denied.".format(B.service.service_id,B.service_operation.operation);F='Necessary permissions for this action: {}'.format([f"Action '{A.action}' for '{A.resource}'"for A in A.explicit_deny+A.explicit_allow+A.implicit_deny]);G='{} permissions have been explicitly denied: {}'.format(len(A.explicit_deny),[f"Action '{A.action}' for '{A.resource}'"for A in A.explicit_deny]);H='{} permissions have been explicitly allowed: {}'.format(len(A.explicit_allow),[f"Action '{A.action}' for '{A.resource}'"for A in A.explicit_allow]);I='{} permissions have been implicitly denied: {}'.format(len(A.implicit_deny),[f"Action '{A.action}' for '{A.resource}'"for A in A.implicit_deny]);J={'error_message':E,'necessary_permissions':F,'explicitly_denied_permissions':G,'explicitly_allowed_permissions':H,'implicitly_denied_permissions':I};K=InputErrorModel(span_id=C.parent_id,error_message=json.dumps(J),error_type=ErrorType.IAM_ERROR);D._event_storage_service.add_error(K)