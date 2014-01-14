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
	return testobjs.TFitting()

@pytest.fixture(scope = 'class')
def simple_filter():
	return testobjs.TFilter

@pytest.fixture(scope = 'class')
def retry_pipe():
	fitting = testobjs.TRetryFitting()
	fitting.Register(testobjs.TFilterRetry,)
	return fitting
	
@pytest.fixture(scope = 'class')
def stop_processing_pipe():
	fitting = testobjs.TStopProcessingFitting()
	fitting.Register(testobjs.TFilterStopProcessing)
	return fitting
	
@pytest.fixture(scope = 'function')
def message():
	return pipewrench.Message(payload = 1)
	
class Test_Filter(object):
	def test_filter_add(self, simple_filter, pipefitting):
		msg = pipefitting.Register(simple_filter)
		assert msg
		
	def test_Invoke(self, pipefitting, message):
		msg = pipefitting.Invoke(message)
		assert msg.payload == 2
		
class Test_Retry(object):
	def test_Invoke(self, retry_pipe, message):
		msg = retry_pipe.Invoke(message)
		assert msg.payload == 3
		
	def test_maxRetry(self, retry_pipe, message):
		message.payload = -10
		try:
			msg = retry_pipe.Invoke(message)
			
		except errors.StopProcessingError:
			assert True
		
		else:
			assert False
			
class Test_StopProcessing(object):
	def test_Invoke(self, stop_processing_pipe, message):
		message.payload = True
		msg = stop_processing_pipe.Invoke(message)
		assert msg.StopProcessing
		
			

		