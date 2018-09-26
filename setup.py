from distutils.core import setup
import codecs
import os
import re

def read(*parts):
	return codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts), 'r').read()

def find_version(*file_paths):
	version_file = read(*file_paths)
	version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
							  version_file, re.M)
	if version_match:
		return version_match.group(1)
	raise RuntimeError("Unable to find version string.")

setup(
	name='Pipewrench',
	version=find_version('pipewrench','__init__.py'),
	author='Taylor McKinnon',
	author_email='tokintmac@gmail.com',
	packages=['pipewrench', 'pipewrench.test'],
	url='https://github.com/TokinT-Mac/PipeWrench',
	license='GPLv3',
	description='Framework for pipeline-style message processing',
	long_description=open('README.rst').read(),
)
