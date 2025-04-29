from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='AreaCalcF',
  version='0.0.4',
  author='fominaav',
  author_email='fomina.av@phystech.edu',
  description='This is the simplest module for calculation square of input figure.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='http://wubbalubba/area_function',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
  project_urls={
    'GitHub': 'https://github.com/vvubbalubbab'
  },
  python_requires='>=3.6'
)