from enum import Enum
from typing import List


class KantanError(object):
    def __init__(self, file: str, line: int, col: int, reason: str, msg: str):
        self.file = file
        self.line = line
        self.col = col
        self.reason = reason
        self.msg = msg

    def __repr__(self):
        return '{}:{}:{}: {}'.format(self.file, self.line, self.col, self.reason)


class Severity(Enum):
    COMPILATION = 1
    COMPILER_MEMORY = 2
    RUNTIME = 3
    RUNTIME_MEMORY = 4


class TestError(object):
    def __init__(self, msg: str, files: List[str], severity=Severity.COMPILATION):
        self.msg = msg
        self.files = files
        self.severity = severity
