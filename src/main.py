import argparse
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import threading
from typing import List

from errors import Severity, TestError
from read import read
from testcase import TestCase

lock = threading.Lock()


def run_test_case(case: TestCase, args, memory_leaks: List[TestError]):
    output = case.execute(args.compiler, args.valgrind)
    error = case.check_output(output)
    if error is None:
        return

    print('{}: {}'.format(case.filename(), error.msg))
    print(output)

    if error.severity == Severity.COMPILER_MEMORY:
        lock.acquire()
        memory_leaks.append(error)
        lock.release()


def main():
    parser = argparse.ArgumentParser(
        description='The Kantan test framework',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('compiler', type=str, help='path to the compiler executable')
    parser.add_argument('tests', type=str, help='path to the test files directory')
    parser.add_argument('--valgrind', type=bool, default=False, help='use valgrind to check for memory leaks')
    parser.add_argument('--threads', type=int, default=multiprocessing.cpu_count() * 2, help='number of worker threads')

    args = parser.parse_args()

    test_cases = read(args.tests)

    memory_leaks = []

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        executor.map(lambda case: run_test_case(case, args, memory_leaks), test_cases)

    if len(memory_leaks) > 0:
        print('THERE WERE COMPILER MEMORY PROBLEMS IN THE COMPILER')
    else:
        print('no memory leaks in the compiler detected')

    for memory_leak in memory_leaks:
        print(memory_leak.files)


if __name__ == '__main__':
    main()
