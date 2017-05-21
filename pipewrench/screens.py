from .pipeline import Screen
from . import errors
import time
import logging

moduleLogger = logging.getLogger(__name__)

class ExceptionScreen(Screen):
	def Execute(self, msg):
		try:
			msg = self.target(msg)
		except Exception as e:
			self.logger.error('Caught Exception: %s'%str(e))
			msg.StopProcessing = True
		return msg
		
class StopProcessingScreen(Screen):
	def Execute(self, msg):
		try:
			 msg = self.target(msg)
		
		except errors.StopProcessingError as e:
			self.logger.debug('Stop Processing Caught: %s'%str(e))
			msg.StopProcessing = True
			msg.error = str(e)
			return msg
			
		except:
			raise
			
		else:
			return msg
			
			
class RetryScreen(Screen):
	def __init__(self, Target, Retry = 3, slideTime = 1):
		self.maxRetry = Retry
		self.slideTime = slideTime
		self.currentRetry = 0
		self.target = Target
		Screen.__init__(self, Target)
		
	def Execute(self, msg):
		logger = moduleLogger.getChild(self.__class__.__name__)
		try:
			msg = self.target(msg)
			
		except errors.RetryError as e:
			self.currentRetry = self.currentRetry + 1
			self.logger.debug('Caught Retry: %s'%str(self.currentRetry))
			if not self.currentRetry > self.maxRetry:
				self.logger.debug('Sleeping: %s'%str(self.slideTime * self.currentRetry))
				time.sleep(self.slideTime * self.currentRetry)
				if e.msg:
					msg = self.Execute(e.msg)
				else:
					msg = self.Execute(msg)
				
			else:
				raise errors.StopProcessingError('Max Retries Reached: %s'%e.error)
		
		return msg	