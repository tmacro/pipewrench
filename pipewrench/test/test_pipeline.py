import pytest

import pipewrench
import pipewrench.test.testobjs as testobjs
import logging
LOGLVL = logging.DEBUG

logging.basicConfig(level=LOGLVL, format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

@pytest.fixture(scope = 'class')
def pipefitting():
	return pipewrench.PipeFitting()
	
@pytest.fixture()
def filter():
	return testobjs.TFilter()
	
@pytest.fixture()
def screen():
	return testobjs.TScreen()
	
@pytest.fixture()
def retryscreen():
	return pipewrench.RetryScreen(slideTime = 1)
	
@pytest.fixture()
def retryfilter():
	return testobjs.TFilterRetry()
	
class Test_PipeFitting(object):
	def test_addFilter(self, pipefitting, filter):
		pipefitting.addFilter(filter)
		
	def test_addFilter2(self, pipefitting, filter):
		pipefitting.addFilter(filter)
		
	def test_addFilter3(self, pipefitting, filter):
		pipefitting.addFilter(filter)
	
	def test_addFilterScreen(self, pipefitting, screen):
		assert pipefitting.addScreen(screen, True)
		
	def test_addGlobalScreen(self, pipefitting, screen):
		assert pipefitting.addScreen(screen)
		
	def test_Process(self, pipefitting):
		msg = pipefitting.Process(1)
		assert msg == 4
		
	def test_Step(self, pipefitting):
		for msg in pipefitting.Step(1):
			print msg
			
	
class Test_Retry(object):
	def test_addObjs(self, retryfilter, retryscreen, pipefitting):
		pipefitting.addFilter(retryfilter)
		pipefitting.addScreen(retryscreen, True)
		
	def test_Retry(self, pipefitting):
		msg = pipefitting.Process(0)
		assert msg == 4
