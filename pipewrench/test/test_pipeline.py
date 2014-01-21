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