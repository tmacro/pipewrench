import pipewrench.pipeline as pipeline
from pipewrench.errors import *
from pipewrench.fittings import BaseFitting
import logging
import pipewrench

module_logger = logging.getLogger(__name__)

class TFilter(pipeline.Filter):
	def __init__(self, offset = 1):
		self.offset = offset
		pipeline.Filter.__init__(self)
		
	def Execute(self, msg):
		msg.payload = msg.payload + self.offset
		self.logger.debug('Message: %s'%str(msg.payload))
		return msg
		
class TFilterRetry(pipeline.Filter):
	def __init__(self, throw = 3):
		self.throw = throw
	def Execute(self, msg):
		if msg.payload == None:
			raise RetryError('HUH?')
			
		msg.payload = msg.payload + 1
		if msg.payload < self.throw:
			raise RetryError('less than 3', msg)
		return msg
		
class TFilterStopProcessing(pipeline.Filter):
	def Execute(self, msg):
		raise StopProcessingError('A wild error has appeared')
			
class TFilterException(pipeline.Filter):
	def Execute(self, msg):
		raise IOError
		
class TRouter(pipeline.Router):
	def Execute(self, msg):
		if msg.payload == 1:
			self.Extend(TFilter, 1)
		else:
			self.Extend(TFilter, 2)
		return self.Route(msg)