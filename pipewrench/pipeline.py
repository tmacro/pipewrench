import logging

class Pipeline(object):
	def __init__(self):
		self.filters = []
		self.globalScreens = []
		self.filterScreens = {}
		
	def Execute(self, msg):
		for filter in self.filters:
			if msg.StopProcessing:
				return msg
			msg = self._processPipeline(filter, msg)
			
		return msg
		
	def addFilter(self, filter):
		self.filters.append(filter)
		
	def addScreen(self, screen, filter = None):
		#If filter is a filter instance the screen will be added to that filter
		#If filter is True the screen will be added to the last filter
		#If filter is omitted or None the screen will be applied globally
		
		if isinstance(filter, Filter):
			if filter in self.filterScreens:
				self.filterScreens[filter].append(screen)
			else:
				self.filterScreens[filter] = [screen]
		elif filter == None:
			self.globalScreens.append(screen)
			
		elif filter == True:
			if len(self.filters) > 0:
				f = self.filters[len(self.filters)-1]
				if f in self.filterScreens:
					self.filterScreens[f].append(screen)
				else:
					self.filterScreens[f] = [screen]
			else:
				return False
				
		return True
	
	def _processPipeline(self, filter, msg):
		return self._constructPipeline(filter)(msg)
		
		
	def _constructPipeline(self, filter):
		target = filter.Process
		if filter in self.filterScreens:
			for screen in self.filterScreens[filter]:
				screen.setTarget(target)
				target = screen.Execute
		for screen in self.globalScreens:
			screen.setTarget(target)
			target = screen.Execute
		
		return target
	
	def Step(self, msg):
		for filter in self.filters:
			msg = self._processPipeline(filter, msg)
			yield msg
	
class Screen(object):
	def __init__(self):
		self.target = None
		
	def setTarget(self, target):
		self.target = target
		
	def Execute(self, msg):
		return self.target(msg)
		
class Filter(object):
	def Process(self, msg):
		self.msg = msg
		if msg.Unpack:
			msg.payload = self.Execute(msg.payload)
		else:
			msg = self.Execute(msg)
		return msg
			
	def Execute(self, msg):
		return msg
		
	
		
class Message(object):
	def __init__(self, payload = None):
		self.StopProcessing = False
		self.Error = None
		self.Retry = False
		if not payload == None:
			self.payload = payload
			self.Unpack = True
		else:
			self.Unpack = False
			