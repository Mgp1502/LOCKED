from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], includes=[], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('program.py', base=base, targetName = 'LOCKED')
]

setup(name='Locked',
      version = '1.0',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)
