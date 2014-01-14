import pipewrench.pipeline as pipeline
from pipewrench.errors import *
from pipewrench.fittings import BaseFitting
import logging
import pipewrench

module_logger = logging.getLogger(__name__)

class TFilter(pipeline.Filter):
	def Execute(self, msg):
		msg.payload = msg.payload + 1
		self.logger.debug('Message: %s'%str(msg.payload))
		return msg
		
class TFilterRetry(pipeline.Filter):
	def Execute(self, msg):
		msg.payload = msg.payload + 1
		if msg.payload < 3:
			raise RetryError('less than 3', msg)
		return msg
		
class TFilterStopProcessing(pipeline.Filter):
	def Execute(self, msg):
		if msg.payload:
			raise StopProcessingError('A wild error has appeared')
		else:
			return msg
			
class TFitting(BaseFitting):
	pass
	
class TRetryFitting(BaseFitting):
	def Invoke(self, msg):
		retry_screen = pipewrench.RetryScreen(self.Execute, slideTime = 0)
		return retry_screen.Execute(msg)
		
class TStopProcessingFitting(BaseFitting):
	def Invoke(self, msg):
		stop_processing_screen = pipewrench.StopProcessingScreen(self.Execute)
		return stop_processing_screen.Execute(msg)