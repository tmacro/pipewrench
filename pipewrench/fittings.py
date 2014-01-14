import pipeline
from screens import ExceptionScreen, StopProcessingScreen
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
			
	