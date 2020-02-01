import argparse

from errors import Severity
from read import read


def main():
    parser = argparse.ArgumentParser(description='The Kantan test framework')
    parser.add_argument('compiler', type=str, help='path to the compiler executable')
    parser.add_argument('tests', type=str, help='path to the test files directory')
    parser.add_argument('--valgrind', type=bool, default=False, help='use valgrind to check for memory leaks')

    args = parser.parse_args()

    test_cases = read(args.tests)

    memory_leaks = []

    for case in test_cases:
        output = case.execute(args.compiler, args.valgrind)
        error = case.check_output(output)
        if error is None:
            continue

        print('{}: {}'.format(case.filename(), error.msg))
        print(output)

        if error.severity == Severity.COMPILER_MEMORY:
            memory_leaks.append(error)

    if len(memory_leaks) > 0:
        print('THERE WERE COMPILER MEMORY LEAKS IN THE COMPILER')

    for memory_leak in memory_leaks:
        print(memory_leak.files)


if __name__ == '__main__':
    main()
