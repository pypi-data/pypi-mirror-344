from __future__ import annotations
import logging as logging
import sys as sys
from .rdBase import *
__all__ = ['VECT_WRAPS', 'VectIter', 'log_handler', 'logger', 'logging', 'name', 'object', 'rdBase', 'sys']
class VectIter:
    def __init__(self, vect):
        ...
    def __iter__(self):
        ...
    def __next__(self):
        ...
def __vect__iter__(vect):
    ...
VECT_WRAPS: set = {'MatchTypeVect', 'VectorOfStringVectors', 'UnsignedLong_Vect', 'VectSizeT'}
__version__: str = '2024.09.6'
log_handler: logging.StreamHandler  # value = <StreamHandler <stderr> (NOTSET)>
logger: logging.Logger  # value = <Logger rdkix (WARNING)>
name: str = '__file__'
object: str = '/Users/runner/work/rdkix-pypi/rdkix-pypi/build/temp.macosx-10.9-x86_64-cpython-312/rdkix_install/lib/python3.12/site-packages/rdkix/rdBase.so'
