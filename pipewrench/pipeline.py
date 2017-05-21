import logging
from . import fittings
import collections
moduleLogger = logging.getLogger(__name__)

class Pipeline(object):
	def __init__(self):
		self.filters = collections.OrderedDict()
	
	def Register(self, filter, *args):
		self.filters[filter] = args
		return self
		
	def Execute(self, message):
		for filter, args in self.filters.items():
			message = filter(*args).Execute(message)
		return message
		
	
class Screen(object):
	def __init__(self, target):
		self.target = target
		self.logger = moduleLogger.getChild(self.__class__.__name__)
		
	def Execute(self, msg):
		return self.target(msg)
		
class Filter(object):	
	def __init__(self):
		self.logger = moduleLogger.getChild(self.__class__.__name__)
	def Execute(self, msg):
		return msg
		
class Router(object):
	def __init__(self, pipeline = None):
		self.logger = moduleLogger.getChild(self.__class__.__name__)
		if not pipeline:
			self.pipeline = fittings.PipeFitting()
		else:
			self.pipeline = pipeline
		
		self.Extend = self.pipeline.Register
		self.Route = self.pipeline.Invoke
		self.Setup()
		
	def Execute(self, msg):
		return self.Route(msg)
	
	def Setup(self):
		pass
		
class Message(object):
	def __init__(self, **kwargs):
		self.StopProcessing = False
		self.Error = None
		self.Retry = False
		for key, value in kwargs.items():
			setattr(self, key, value)
			
	def __repr__(self):
		return 'SP: %s - Retry: %s - Error: %s'%(self.StopProcessing, self.Retry, self.Error)