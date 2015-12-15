from setuptools import setup, find_packages
setup(
  name='icinga2_api',
  license='MIT',
  version='0.0.3',
  url='https://github.com/saurabh-hirani/icinga2_api',
  description=('Python library and command-line support for the icinga2 API'),
  author='Saurabh Hirani',
  author_email='saurabh.hirani@gmail.com',
  packages=find_packages(),
  install_requires=[
    'click',
    'requests',
    'pyyaml',
    'simplejson'
  ],
  entry_points = {
    'console_scripts': [
      'icinga2_api = icinga2_api.cmdline:icinga2_api',
    ]
  }
)
