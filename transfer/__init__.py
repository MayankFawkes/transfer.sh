# -*- coding: utf-8 -*-
"""
This is unofficial CLI of transfer.sh
"""

__author__ = "Mayank Gupta"
__license__ = "MIT License"
__github__ = "https://github.com/MayankFawkes/transfer.sh"

from transfer.request import MakeRequest
from transfer.__main__ import Upload, Remove
from transfer.version import __version__