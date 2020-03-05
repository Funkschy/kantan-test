from typing import Optional, List
import importlib.util as util
import subprocess
import os

from errors import TestError, Severity
from output import KantanOutput

error_rc = 255
segfault_rc = -11
abort_rc = -6


def valgrind(filename: str) -> List[str]:
    return [
        'valgrind',
        '--leak-check=full',
        '--error-exitcode=' + str(error_rc),
        '--xml=yes',
        '--xml-file={}.xml'.format(filename)
    ]


class TestCase(object):
    def __init__(self, path: str):
        mod_name = 'test'
        filename = path

        spec = util.spec_from_file_location(mod_name, path)
        module = util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.test_code = module.Test(filename)

    def check_output(self, output: KantanOutput) -> Optional[TestError]:
        return self.test_code.check_output(output)

    # TODO: not only check compiler output, but also execute the program...
    def execute(self, compiler: str, use_valgrind: bool) -> KantanOutput:
        cmd = [compiler] + self.test_code.files()
        if use_valgrind:
            cmd = valgrind(self.filename()) + cmd

        output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return KantanOutput(output, use_valgrind)

    def filename(self) -> str:
        return self.test_code.filename()


# Superclass for all Testclasses
class Code(object):
    def __init__(self, filename):
        self.filepath = filename

    def filename(self) -> str:
        return os.path.splitext(os.path.basename(self.filepath))[0]

    def relative_to(self, filename: str) -> str:
        return os.path.join(os.path.dirname(self.filepath), filename)

    def files(self) -> List[str]:
        return [self.filepath.replace('.py', '.kan')]

    def create_error(self, msg: str, severity=Severity.COMPILATION) -> TestError:
        return TestError(msg, self.files(), severity)

    def check_output(self, output: KantanOutput) -> Optional[TestError]:
        if output.used_valgrind:
            if output.rc == error_rc:
                return self.create_error('{} has memory leaks'.format(self.filepath), Severity.COMPILER_MEMORY)
            elif output.rc == segfault_rc:
                return self.create_error('{} segfaulted'.format(self.filepath), Severity.COMPILER_MEMORY)
            elif output.rc == abort_rc:
                # TODO: not really memory, maybe introduce a separate category
                return self.create_error('{} aborted'.format(self.filepath), Severity.COMPILER_MEMORY)
            else:
                os.remove('{}.xml'.format(self.filename()))
                pass

        return self.check(output)

    def check(self, output: KantanOutput) -> Optional[TestError]:
        if len(output.errors) != 0:
            return self.create_error('expected 0 errors, but got {}'.format(len(output.errors)))

        return None
