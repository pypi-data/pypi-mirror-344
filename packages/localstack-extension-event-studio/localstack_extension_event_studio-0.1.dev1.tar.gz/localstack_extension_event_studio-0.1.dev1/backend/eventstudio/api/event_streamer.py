import json,logging
from typing import Any
from localstack.http.websocket import WebSocket,WebSocketDisconnectedError,WebSocketRequest
from eventstudio.utils.utils import CustomJSONEncoder
LOG=logging.getLogger(__name__)
class EventStreamer:
	sockets:list[WebSocket]
	def __init__(A):A.sockets=[]
	def on_websocket_request(B,request:WebSocketRequest,*D,**E):
		A=None
		try:
			with request.accept()as A:
				B.sockets.append(A)
				while True:C=A.receive();LOG.info('Received message from log streamer websocket: %s',C)
		except WebSocketDisconnectedError:LOG.debug('Websocket disconnected: %s',A)
		finally:
			if A is not None:B.sockets.remove(A)
	def notify(A,doc:Any):
		B=json.dumps(doc,cls=CustomJSONEncoder)
		for C in A.sockets:C.send(B)