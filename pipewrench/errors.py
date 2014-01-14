class Error(Exception):
	'''Base error for this module'''
	def __init__(self, error):
		self.error = error
		
	def __str__(self):
		return str(self.error)
	
	
class StopProcessingError(Error):
	'''Exception raised to hault pipeline execution'''
	pass

class RetryError(Error):
	'''Execption rasied to retry filter'''
	def __init__(self, error, msg = None):
		self.error = error
		self.msg = msg