from pipeline import Screen
import time
import logging
moduleLogger = logging.getLogger(__name__)
class ExceptionHandler(Screen):
	def Execute(self, msg):
		try:
			self.target(msg)
		except Exception as e:
			msg.StopProcessing = True
			msg.Error = e
		return msg
		
class StopProcessingHandler(Screen):
	def Execute(self, msg):
		if msg.StopProcessing:
			return msg
		else:
			return self.target(msg)
			
			
class RetryScreen(Screen):
	def __init__(self, Retry = 3, slideTime = 5):
		self.Retry = Retry
		self.slideTime = slideTime
		self.currentRetry = 0
		Screen.__init__(self)
		
	def Execute(self, msg):
		logger = moduleLogger.getChild(self.__class__.__name__)
		msg = self.target(msg)
		try:
			if msg.Retry:
				self.currentRetry = self.currentRetry+1
				logger.debug('msg.Retry = True')
				if not self.currentRetry > self.Retry:
					logger.debug('Retrying %s of %s'%(str(self.currentRetry), str(self.Retry)))
					logger.debug('Sleeping %s'%str(self.slideTime*self.currentRetry))
					time.sleep(self.slideTime*self.currentRetry)
					msg.Retry = False
					msg = self.Execute(msg)
				else:
					logger.debug('Max Retries Reached')
					msg.StopProcessing = True
					msg.Error = 'Max retries reached'
			
		except AttributeError:
			pass
		self.currentRetry = 0
		return msg