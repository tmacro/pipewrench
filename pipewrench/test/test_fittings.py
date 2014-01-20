import pytest
import pipewrench.test.testobjs as testobjs
import logging
import pipewrench
from pipewrench.screens import *
import pipewrench.errors as errors
LOGLVL = logging.DEBUG

logging.basicConfig(level=LOGLVL, format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

@pytest.fixture(scope = 'class')
def pipefitting():
	return pipewrench.fittings.BaseFitting()

@pytest.fixture(scope = 'class')
def simple_filter():
	return testobjs.TFilter

@pytest.fixture(scope = 'class')
def retry_pipe(retry):
	fitting = pipewrench.fittings.RetryFitting(retry, 0)
	return fitting
	
@pytest.fixture(scope = 'class')
def stop_processing_pipe():
	fitting = testobjs.TStopProcessingFitting()
	fitting.Register(testobjs.TFilterStopProcessing)
	return fitting

	
@pytest.fixture(scope = 'function')
def message(payload = 1):
	return pipewrench.Message(payload = payload)
	
class Test_Retry(object):
	@pytest.mark.parametrize("retrypipe,message,throw", [
				(retry_pipe(3), message(1), 3),
				(retry_pipe(5), message(1), 5),
				pytest.mark.xfail((retry_pipe(1), message(-10), 3)),
		])
	def test_Invoke(self, retrypipe, message, throw):
		retrypipe.Register(testobjs.TFilterRetry, throw)
		msg = retrypipe.Invoke(message)
		assert msg.payload == throw 
		assert msg.StopProcessing == False
			
class Test_StopProcessing(object):
	def test_Invoke(self, stop_processing_pipe, message):
		message.payload = True
		msg = stop_processing_pipe.Invoke(message)
		assert msg.StopProcessing		
			

		