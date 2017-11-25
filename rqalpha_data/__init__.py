#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# disable rqalpha better_exceptions: WARNING: better_exceptions will only inspect code from the command line
import sys


class StdErrToNothing(object):
    def __init__(self, ):
        pass

    def write(self, txt):
        pass


orig_stderr = sys.stderr
sys.stderr = StdErrToNothing()
import better_exceptions

sys.stderr = orig_stderr

from .datasource import *
from .datetime_utils import *
from .quant_utils import *
