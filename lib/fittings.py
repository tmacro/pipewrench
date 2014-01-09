import pipeline

class PipeFitting(object):
	def __init__(self):
		self.pipeline = pipeline.Pipeline()
		self.addFilter = self.pipeline.addFilter
		self.addScreen = self.pipeline.addScreen
		
	def Process(self, msg):
		msg = self.packMessage(msg)
		msg = self.pipeline.Execute(msg)
		msg = self.unpackMessage(msg)
		return msg
			
	def packMessage(self, msg):
		if isinstance(msg, pipeline.Message):
			return msg
		else:
			return pipeline.Message(msg)
			
	def unpackMessage(self, msg):
		if msg.Unpack:
			return msg.payload
		else:
			return msg
			
	def Step(self, msg):
		msg = self.packMessage(msg)
		for message in self.pipeline.Step(msg):
			msg = self.unpackMessage(message)
			yield msg