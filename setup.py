from setuptools import setup

setup(name='uploader', version='1.0',
	description='Trustless and cryptographically audited public file server.',
	author='Shawn Wilkinson', author_email='shawn+hashserv@storj.io',
	url='http://storj.io',

	#  Uncomment one or more lines below in the install_requires section
	#  for the specific client drivers/modules your application needs.
	install_requires=['flask']
	)