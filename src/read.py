from typing import List
from os import listdir
from os.path import abspath, join, splitext

from testcase import TestCase


def read(test_path: str) -> List[TestCase]:
    files = filter(lambda f: splitext(f)[1] == '.py', [abspath(join(test_path, f)) for f in listdir(test_path)])
    return [TestCase(path) for path in files]
