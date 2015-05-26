from setuptools import setup

setup(
    name='hashserv', version='1.0',
    description='Federated server for building blockchain notarized Merkle trees.',
    author='Shawn Wilkinson', author_email='shawn+hashserv@storj.io',
    url='http://storj.io',

    #  Uncomment one or more lines below in the install_requires section
    #  for the specific client drivers/modules your application needs.
    install_requires=['flask', 'btctxstore>=2.0.2'],
    tests_require=['coverage', 'coveralls'],
    test_suite="tests",
)
