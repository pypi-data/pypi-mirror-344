from eventstudio.db.event_storage import EventStorageService
class Instrumentation:
	event_storage_service:EventStorageService
	def __init__(A,event_storage_service:EventStorageService):A.event_storage_service=event_storage_service
	def apply(A):0