from pipeline import Screen

class ExceptionHandler(Screen):
	def Execute(self, msg):
		try:
			self.target(msg)
		except as e:
			msg.StopProcessing = True
			msg.Error = e
		return msg
		
class StopProcessingHandler(Screen):
	def Execute(self, msg):
		if msg.StopProcessing:
			return msg
		else:
			return self.target(msg)