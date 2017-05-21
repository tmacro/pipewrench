import pytest
import logging
import pipewrench
import pipewrench.test.testobjs as testobjs

LOGLVL = logging.DEBUG
logging.basicConfig(level=LOGLVL, format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

@pytest.fixture(scope='function')
def pipeline():
	return pipewrench.pipeline.Pipeline()
	
@pytest.fixture(scope='function')
def message(payload = None):
	if payload:
		return pipewrench.Message(payload=payload)
	else:
		return pipewrench.Message()
	
@pytest.fixture(scope='function')
def filter():
	return testobjs.TFilter
	
class Test_Pipeline(object):
	def test_Register(self, pipeline, filter):
		x = pipeline.Register(filter)
		assert x == pipeline
		assert filter in pipeline.filters
		
	@pytest.mark.parametrize("message,offset", [
				(message(1), 4),
				(message(2), 5),
				(message(3), 6),
		])
	def test_Execute(self, pipeline, filter, message, offset):
		num = message.payload
		pipeline.Register(filter, offset)
		msg = pipeline.Execute(message)
		assert msg.payload == num+offset
		
class Test_Filter(object):
	def test_Filter(self):
		filter = pipewrench.pipeline.Filter()
		assert filter.Execute(True)
		
class Test_Screen(object):
	@staticmethod
	def dummyTarget(msg):
		return msg
		
	def test_Screen(self, message):
		screen = pipewrench.pipeline.Screen(Test_Screen.dummyTarget)
		assert screen.Execute(True)
		
class Test_Route(object):
	@pytest.mark.parametrize("message,final", [
				(message(1), 2),
				(message(2), 4)
		])
	def test_Route(self, message, final):
		router = testobjs.TRouter()
		print(router.pipeline)
		msg = router.Execute(message)
		assert msg.payload == final
		
	def test_RouteBase(self):
		pipefitting = pipewrench.fittings.PipeFitting()
		router = pipewrench.pipeline.Router(pipefitting)
		assert router.Execute(True)