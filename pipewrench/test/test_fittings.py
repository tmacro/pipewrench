import pytest
import pipewrench.test.testobjs as testobjs
import logging
import pipewrench
from pipewrench.screens import *
import pipewrench.errors as errors
LOGLVL = logging.DEBUG

logging.basicConfig(level=LOGLVL, format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

@pytest.fixture(scope = 'class')
def basefitting():
	return pipewrench.fittings.BaseFitting()

@pytest.fixture(scope = 'function')
def pipefitting():
	return pipewrench.fittings.PipeFitting()

@pytest.fixture(scope = 'class')
def retry_pipe(retry):
	fitting = pipewrench.fittings.RetryFitting(retry, 0)
	return fitting
		
@pytest.fixture(scope = 'function')
def message(payload = 1):
	return pipewrench.Message(payload = payload)
	
class Test_Retry(object):
	@pytest.mark.parametrize("retrypipe,message,throw", [
				(retry_pipe(3), message(1), 3),
				(retry_pipe(5), message(1), 5),
				pytest.mark.xfail((retry_pipe(5), message(None), None)),
				pytest.mark.xfail((retry_pipe(1), message(-10), 3)),
		])
	def test_Invoke(self, retrypipe, message, throw):
		retrypipe.Register(testobjs.TFilterRetry, throw)
		msg = retrypipe.Invoke(message)
		assert msg.payload == throw 
		assert msg.StopProcessing == False	
			
class Test_BaseFitting(object):
	def test_Invoke(self, basefitting, message):
		basefitting.Register(testobjs.TFilter)
		msg = basefitting.Invoke(message)
		assert msg.payload == 2
		
class Test_PipeFitting(object):
	def test_Exception(self, pipefitting, message):
		pipefitting.Register(testobjs.TFilterException)
		msg = pipefitting.Invoke(message)
		print(msg.Error)
		assert msg.StopProcessing == True
	
	def test_StopProcessing(self, pipefitting, message):
		pipefitting.Register(testobjs.TFilterStopProcessing)
		message.payload = True
		msg = pipefitting.Invoke(message)
		assert msg.StopProcessing