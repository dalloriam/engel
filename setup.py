from setuptools import setup, find_packages
import re, os


version = ''
with open('popeui/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')


readme = ''
with open('README.md') as f:
    readme = f.read()

setup(name='popeui',
      author='Dalloriam',
      author_email='dalloriam@gmail.com',
      url='https://github.com/Dalloriam/popeui',
      version=version,
      packages=find_packages(),
      license='MIT',
      description='Build miraculous web interfaces for your projects.',
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      long_description=readme,
      include_package_data=True,
      install_requires=[
        "autobahn==0.13.0",
        "requests==2.10.0",
        "asyncio==3.4.3"
      ]
)
