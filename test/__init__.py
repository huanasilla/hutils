from functools import partial
import os
import unittest
from asilla_utils import *
__all__ = ['suite']

def suite():
    from test import dummy
    suite = unittest.TestSuite()
    suite.addTest(dummy.suite())
    return suite
