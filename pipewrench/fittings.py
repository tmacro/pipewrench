from . import pipeline
from .screens import ExceptionScreen, StopProcessingScreen, RetryScreen
import logging
module_logger = logging.getLogger(__name__)

class BaseFitting(object):
	def __init__(self):
		self.pipeline = pipeline.Pipeline()
		self.Execute = self.pipeline.Execute
		self.logger = module_logger.getChild(self.__class__.__name__)
		
	def Invoke(self, msg):
		return self.Execute(msg)
		
	def Register(self, filter, *args):
		self.logger.debug('Registered: %s'%str(filter))
		self.pipeline.Register(filter, *args)
		return self
			
class PipeFitting(BaseFitting):
	def Invoke(self, msg):
		stop_processing_screen = StopProcessingScreen(self.Execute)
		exception_screen = ExceptionScreen(stop_processing_screen.Execute)
		return exception_screen.Execute(msg)
		
		
class RetryFitting(BaseFitting):
	def __init__(self, maxRetry = 3, slideTime = 1):
		self.maxRetry = maxRetry
		self.slideTime = slideTime
		BaseFitting.__init__(self)
			
	def Invoke(self, msg):
		retry_screen = RetryScreen(self.Execute, self.maxRetry, self.slideTime)
		stop_processing_screen = StopProcessingScreen(retry_screen.Execute)
		exception_screen = ExceptionScreen(stop_processing_screen.Execute)
		return exception_screen.Execute(msg)