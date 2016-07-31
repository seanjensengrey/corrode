import random
import glob
import re
import os

import subprocess
from collections import namedtuple

CorrodeTestCase = namedtuple("TestCase", "case file expected_return_code")

def randstr(n):
    return ''.join(chr(random.randint(ord('a'),ord('z'))) for _ in range(n))


def _collect_test_cases():
    c_files = glob.glob("*.c")
    expected_m = re.compile("// expected-return:([\d]*)")
    test_cases = []
    for path in c_files:
        with open(path,"r") as f:
            return_code = re.search(expected_m, f.read())
            if return_code is None:
                pass
            else:
                try:
                    test_cases.append(CorrodeTestCase(path.rsplit('.', 1)[0],
                                                      path,
                                                      int(return_code.group(1))))
                except Exception as e:
                    print("Found 'expected-return' " + return_code.groups())

    return test_cases

def c_artifact(test_case):
    return test_case.case + '-gcc'

def corrode_artifact(test_case):
    return test_case.case + ".rs"

def rust_artifact(test_case):
    return test_case.case + '-rust'

isfile = os.path.isfile

def c_compile(test_case):
    subprocess.run(['gcc','-o',test_case.case + '-gcc', test_case.file])
    assert isfile(c_artifact(test_case)), "test_case:%s did not compile (gcc)"  % (test_case.case)


def corrode(test_case):
    subprocess.run(['corrode',test_case.file])
    assert isfile(corrode_artifact(test_case)), "test_case:%s did not translate to rust" % (test_case.case)


def rust_compile(test_case):
    subprocess.run(['rustc','-o', test_case.case + '-rust', test_case.case + '.rs'])
    assert isfile(rust_artifact(test_case)), "test_case:%s did not compile (rust)" % (test_case.case)


def clean(test_case):
    artifacts = [
        c_artifact(test_case),
        corrode_artifact(test_case),
        rust_artifact(test_case)
    ]
    for path in artifacts:
        try:
            os.path.unlink(path)
        except:
            pass


def prepare(test_case):
    clean(test_case)
    c_compile(test_case)
    corrode(test_case)
    rust_compile(test_case)


def run_test_case(test_case):
    prepare(test_case)
    proc = subprocess.run(['./' + test_case.case + '-rust'])
    assert proc.returncode == test_case.expected_return_code, "case:%s failed expected return code:%d found:%d" % (
        test_case.case,
        test_case.expected_return_code,
        proc.returncode
    )


def mk_test_runner(test_case):
    def fn():
        run_test_case(test_case)
    fn.__name__ = test_case.case
    return fn


for tc in _collect_test_cases():
    globals()['test_' + tc.case] = mk_test_runner(tc)

print(globals())