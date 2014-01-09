import pytest

import lib.fittings
import tests.testobjs as testobjs

@pytest.fixture(scope = 'class')
def pipefitting():
	return lib.fittings.PipeFitting()
	
@pytest.fixture()
def filter():
	return testobjs.TFilter()
	
@pytest.fixture()
def screen():
	return testobjs.TScreen()
	
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