import glob
import re
import os

import subprocess
from collections import namedtuple

CorrodeTestCase = namedtuple("TestCase", "case file expected_return_code")

import pdb

def c_artifact(test_case):
    return test_case.case + '-gcc'


def corrode_artifact(test_case):
    return test_case.case + ".rs"


def rust_artifact(test_case):
    return test_case.case + '-rust'


isfile = os.path.isfile



def _collect_test_cases():
    """
    gather all the .c files in the current directory
        for each one that has a
            // expected-return:<int>
        entry, generate a CorrodeTestCase for it

    @:returns List[CorrodeTestCase]
    """
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


def compile_c(test_case):
    subprocess.call(['gcc','-o',test_case.case + '-gcc', test_case.file])
    assert isfile(c_artifact(test_case)), "test_case:%s did not compile (gcc)"  % (test_case.case)


def translate_corrode(test_case):
    subprocess.call(['corrode',test_case.file])
    assert isfile(corrode_artifact(test_case)), "test_case:%s did not translate to rust" % (test_case.case)


def compile_rust(test_case):
    subprocess.call(['rustc','-o', test_case.case + '-rust', test_case.case + '.rs'])
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
    compile_c(test_case)
    translate_corrode(test_case)
    compile_rust(test_case)


def run_test_case(test_case):
    prepare(test_case)
    return_code = subprocess.call(['./' + rust_artifact(test_case)])
    assert return_code == test_case.expected_return_code, "case:%s failed expected return code:%d found:%d" % (
        test_case.case,
        test_case.expected_return_code,
        return_code 
    )


def mk_test_runner(test_case):
    def fn():
        run_test_case(test_case)
    fn.__name__ = test_case.case
    return fn


# inject test methods into globals
# so that py.test can pick them up
for tc in _collect_test_cases():
    globals()['test_' + tc.case] = mk_test_runner(tc)
