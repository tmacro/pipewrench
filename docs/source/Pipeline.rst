:mod:`pipeline` --- Message processing pipeline
=================================================

This module defines the following functions and objects:

.. class:: Pipeline

		This class represents a message processing pipeline. Messages a processed 
		sequentially through :class:`Filter` to preform actions and :class:`Screen` 
		to provide setup and teardown as well as error handling. 
		
	.. method:: Register(filter, args=[])
	
		Registers a :class:`Filter` to the :class:`Pipeline` . Filters are executed
		in the order they are registered, with the first registered being the first 
		executed. Any other arguments passed with be passed onto to a :class:`Filter` on creation.
		This method returns the :class:`Pipeline`\ , so consecutive calls to *Register* can be 
		chained together.
		
	.. method:: Execute(message)

		Processes *message* through the pipeline, returns modified message.
		
.. class:: Filter

	.. method:: Execute(message)
	
		This function will be called by the :class:`Pipeline` when executing a Filter. 
		It is passed a :class:`Message` instance as its only argument and should return one.
		
.. class:: Screen	

	.. attribute:: target
	
		This is the function the Screen has to call to continue the pipeline.
		
	.. method:: Execute(message)
	
		This function is called when processing the Screen. Like Filters a :class:`Message` instance 
		is passed as its only argument. Screens should call :attr:`target` to continue processing 
		the pipeline and should return a :class:`Message` instance.
		
.. class:: Message(kwargs = {})

	.. attribute:: StopProcessing

		Defaults to *False*, is set to *True* by the :class:`StopProcessingScreen` to indicate an error.
		
	.. attribute:: Error
		
		Defaults to *None*, contains any error caught by the :class:`StopProcessingScreen`\ .
		
Message Objects
***************

Messages contain the data the :class:`Pipeline` processes. Any keyword arguments passed at creation
will be avaliable as Message.<keyword> .::

	>>> from pipewrench.pipeline import Message
	
	>>> msg = Message(foo = 'arg!', bar = 2)
	
	>>> print msg.foo
	arg!
	>>> print msg.bar
	2
	
Filter Objects
**************

Filters do most of the heavy lifting in pipewrench, this is where you *do* something with those messages.
Every time a message is processed the pipeline automatically creates a instance of the filter, passing
in any supplied arguents, and calls :meth:`Filter.Execute`\ . It is where a filter can do its work eg. making a http request.
For example::

	from pipewrench.pipeline import Pipeline, Filter, Message
	
	class testFilter(Filter):
		def Execute(self, message):
			message.payload = message.payload + 1
			return message
			
	pipe = Pipeline()
	pipe.Register(testFilter)
	
	message = Message(payload = 1)
	
	print pipe.Execute(message)
	
Screen Objects
**************
	
Screens are executed before filters and provide functions such as exception handling, and logging. When 
a :meth:`PipeFitting.Invoke` method is called instances of :class:`Screen` is created and their :meth:`Screen.Execute`
method is called with *message* as its only argument. In :meth:`Screen.Execute` Screens should call :attr:`Screen.target`
to continue executing the pipeline and should return a :class:`Message` instance. For example::
	
	from pipewrench.pipeline import Filter, Screen, Pipeline, Message
	from pipewrench.fittings import BaseFitting
	
	class testFilter(Filter):
		def Execute(self, message):
		`	message.payload = message.payload + 1
			return message
			
	class testScreen(Screen):
		def Execute(self, message):
			print 'Before Filter: %s'%str(message.payload)
			message = self.target(message)
			print 'After Filter: %s'%str(message.payload))
			return message
			
	class TestFitting(object):
		def Invoke(self, message):
			test_screen = testScreen(self.Execute)
			return test_screen.Execute(message)
			
	fitting = TestFitting()
	message = Message(payload = 1)
	
	fitting.Register(testFilter)
	msg = fitting.Invoke(message)
	