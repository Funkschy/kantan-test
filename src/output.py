from subprocess import CompletedProcess
from typing import List
import re

from errors import KantanError

error_regex = r"ERROR: (.*)\\n--> (.*):(\d+):(\d+)\\n(.*)"


def iterate_errors(haystack):
    needle = 'ERROR'

    ln = len(needle)
    idx = haystack.find(needle)
    while idx >= 0:
        end = haystack.find('\\n\\n', idx + ln)
        if end < 0:
            end = len(haystack)

        yield haystack[idx:end]
        idx = haystack.find(needle, idx + ln)


class KantanOutput(object):
    def __init__(self, raw_output: CompletedProcess, used_valgrind: bool):
        self.rc = raw_output.returncode
        self.raw_stdout = str(raw_output.stdout)
        self.raw_stderr = str(raw_output.stderr)
        self.errors = self.parse_errors()
        self.used_valgrind = used_valgrind

    def __repr__(self):
        return 'return code: {}, errors: {}'.format(self.rc, self.errors)

    def parse_errors(self) -> List[KantanError]:
        kantan_errors = []

        errors = [err for err in iterate_errors(self.raw_stdout)]
        for err in errors:
            matches = re.finditer(error_regex, err, re.MULTILINE)

            for matchNum, match in enumerate(matches, start=1):
                reason = match.group(1)
                filename = match.group(2)
                line = int(match.group(3))
                col = int(match.group(4))
                code = match.group(5)
                kantan_errors.append(KantanError(filename, line, col, reason, code))

        return kantan_errors
