
# PoC Test Suite For Corrode

see https://github.com/jameysharp/corrode/issues/44
    for a discussion about testing corrode

The suite takes a body of c-files that return
an integer via an exit code. This provides a nice
process encapsulation and very simple communication
mechanism.

The test runner autogenerates a python method per
c-file that handles c compilation, translation with
corrode, rust compilation and running the resulting
rust program to get the exit code.

To run the test suite

```
virtualenv --python=python3 test.env
. test.env/bin/activate
pip install -r requirements.txt

# rustc, gcc should already be in path
PATH=../.cabal-sandbox/bin:$PATH py.test test.py -r ap
```

Currently there are 7 tests

```
FAIL test.py::test_struct0
FAIL test.py::test_sw0
PASSED test.py::test_al0
PASSED test.py::test_al1
PASSED test.py::test_for1
PASSED test.py::test_struct1
PASSED test.py::test_ten
```

## Creating a Test

1. create a c-file with a `main` method
2. add the `// expected-return:<int>`
3. run the suite as above, confirm result (change return code
    and confirm test fails if already passing)

```c
int main(int argc, char** argv) {
    int j = 4;
    int k = 0;
    for(int i=0; i<10; i++) {
        k = j * i;
    }
    // expected-return:36
    return k;
}
```


http://doc.pytest.org/en/latest/goodpractices.html

