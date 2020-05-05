from setuptools import setup, find_packages
setup(name='hutils',
version='0.1',
description='Help utilities - created by huanasilla',
url='#',
author='huan',
author_email='huan@asilla.net',
license='MIT',
#keywords=['test','Logger','TimeInspector','Configuration'],
#packages=['src'],
py_modules=["hutils"],
test_suite="test.suite",
package_dir={'': 'src'},  # Optional
packages=find_packages(where='src'),  # Required
entry_points={  # Optional
        'console_scripts': [
            'hutils=hutils:main',
        ],
},
zip_safe=False)
