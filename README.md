# The official kantan testrunner
This repository contains the testrunner for the [Kantan Programming Language](https://github.com/funkschy/kantan-lang)

## Usage
```
python3 src/main.py <path-to-compiler> <path-to-test-suite> [--valgrind=True]
```

## How does it work?
1) kantan-test scans the  <path-to-test-suite> directory for .kan and .py files.
2) files listed in kantan-test-ignore are filtered out
3) a python object is created for each test case (.py file) which should extend `testcase.Code`
4) the .kan files are compiled and the output is checked by the objects from the last step
5) if there were errors those are printed to the console
6) (optional) if the --valgrind option is set, memory leaks inside the compiler are listed separately


## Examples
```python
from typing import Optional

from testcase import Code
from errors import TestError, Severity
from output import KantanOutput


class Test(Code):
    # overwrite this method of the Code class. The argument is the compiler output, which
    # has already been parsed
    def check(self, output: KantanOutput) -> Optional[TestError]:
        """Checks if the correct error is printed for struct-decl-access-error.kan"""

        if len(output.errors) != 1:
            msg = 'expected 1 error, but got {}'.format(len(output.errors))
            return self.create_error(msg)

        error = output.errors[0]
        expected_rsn = "'struct declaration' cannot be accessed with '.' operator"
        actual_rsn = error.reason
        if expected_rsn not in actual_rsn:
            msg = 'wrong reason, expected <{}>, but got {}'.format(expected_rsn, actual_rsn)
            return self.create_error(msg)

        if error.line != 5:
            return self.create_error('wrong line')

        if error.col != 1:
            print(error.col)
            return self.create_error('wrong column')

        return None
```