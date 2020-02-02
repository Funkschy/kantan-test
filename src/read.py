from typing import List, Set
from os import listdir
from os.path import abspath, join, splitext, isfile, basename

from testcase import TestCase


def read(test_path: str) -> List[TestCase]:
    ignored = read_ignored(test_path)

    def add_file(f) -> bool:
        st = splitext(f)
        return st[1] == '.py' and basename(st[0]) not in ignored

    files = filter(add_file, [abspath(join(test_path, f)) for f in listdir(test_path)])
    return [TestCase(path) for path in files]


def read_ignored(test_path: str) -> Set[str]:
    ignore_file = join(test_path, 'kantan-test-ignore')
    if isfile(ignore_file):
        with open(ignore_file) as f:
            return set(map(lambda n: n.strip(), f.readlines()))

    return set()
