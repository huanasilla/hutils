from setuptools import setup, find_packages
setup(name='asilla_utils',
version='0.2',
description='Help utilities - created by asilla',
url='#',
author='anolla',
author_email='huan@asilla.net',
license='MIT',
py_modules=["asilla_utils"],
test_suite="test.suite",
package_dir={'': 'src'},  # Optional
packages=find_packages(where='src'),  # Required
zip_safe=True)
