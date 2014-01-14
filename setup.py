from distutils.core import setup

setup(
    name='Pipewrench',
    version='0.1.0',
    author='Taylor McKinnon',
    author_email='tokintmac@gmail.com',
    packages=['pipewrench', 'pipewrench.test'],
    url='https://github.com/TokinT-Mac/PipeWrench',
    license='GPLv3',
    description='Framework for pipeline-style message processing',
    long_description=open('README').read(),
)
