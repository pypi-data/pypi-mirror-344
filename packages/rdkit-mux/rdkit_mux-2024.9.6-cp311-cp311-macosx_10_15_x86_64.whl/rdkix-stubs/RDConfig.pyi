"""
 Configuration for the RDKix Python code

"""
from __future__ import annotations
import os as os
import rdkix as rdkix
import sqlite3 as sqlite3
import sys as sys
__all__ = ['ObsoleteCodeError', 'RDCodeDir', 'RDContribDir', 'RDDataDatabase', 'RDDataDir', 'RDDocsDir', 'RDProjDir', 'RDTestDatabase', 'UnimplementedCodeError', 'defaultDBPassword', 'defaultDBUser', 'molViewer', 'os', 'pythonExe', 'pythonTestCommand', 'rdkix', 'rpcTestPort', 'sqlite3', 'sys', 'usePgSQL', 'useSqlLite']
class ObsoleteCodeError(Exception):
    pass
class UnimplementedCodeError(Exception):
    pass
RDCodeDir: str = '/Users/runner/work/rdkix-pypi/rdkix-pypi/build/temp.macosx-10.9-x86_64-cpython-311/rdkix_install/lib/python3.11/site-packages/rdkix'
RDContribDir: str = '/Users/runner/work/rdkix-pypi/rdkix-pypi/build/temp.macosx-10.9-x86_64-cpython-311/rdkix_install/share/RDKix/Contrib'
RDDataDatabase: str = '/Users/runner/work/rdkix-pypi/rdkix-pypi/build/temp.macosx-10.9-x86_64-cpython-311/rdkix_install/share/RDKix/Data/RDData.sqlt'
RDDataDir: str = '/Users/runner/work/rdkix-pypi/rdkix-pypi/build/temp.macosx-10.9-x86_64-cpython-311/rdkix_install/share/RDKix/Data'
RDDocsDir: str = '/Users/runner/work/rdkix-pypi/rdkix-pypi/build/temp.macosx-10.9-x86_64-cpython-311/rdkix_install/share/RDKix/Docs'
RDProjDir: str = '/Users/runner/work/rdkix-pypi/rdkix-pypi/build/temp.macosx-10.9-x86_64-cpython-311/rdkix_install/share/RDKix/Projects'
RDTestDatabase: str = '/Users/runner/work/rdkix-pypi/rdkix-pypi/build/temp.macosx-10.9-x86_64-cpython-311/rdkix_install/share/RDKix/Data/RDTests.sqlt'
defaultDBPassword: str = 'masterkey'
defaultDBUser: str = 'sysdba'
molViewer: str = 'PYMOL'
pythonExe: str = '/private/var/folders/gn/rldh9pd93qg48089gvgb1gb80000gn/T/cibw-run-2169he1j/cp311-macosx_x86_64/build/venv/bin/python3.11'
pythonTestCommand: str = 'python'
rpcTestPort: int = 8423
usePgSQL: bool = False
useSqlLite: bool = True
