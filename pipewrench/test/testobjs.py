import pipewrench.pipeline as pipeline

class TScreen(pipeline.Screen):
	def Execute(self, msg):
		msg = self.target(msg)
		if msg.StopProcessing:
			print 'FAIL'
		return msg
		
class TFilter(pipeline.Filter):
	def Execute(self, msg):
		msg = msg + 1
		if msg > 3:
			self.msg.StopProcessing = True
		return msg
		
		
class TFilterRetry(pipeline.Filter):
	def Execute(self, msg):
		msg = msg + 1
		if msg < 5:
			self.msg.Retry = True
		return msg