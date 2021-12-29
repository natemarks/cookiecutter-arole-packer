Contributing to the cookiecutter-ansible-role project

## How to start

  - Create an issue
  - Pull the repo and get `make test` running. 
  - Create your PR branch with the issue identifier
  - make your changes, cover them with tests and make sure `make test` succeeds
  - submit your pull request



## Testing

Each test case in test/template_test.py runs cookiecutter with a set of overrides for cookiecutter.json variables. I use
testinfra to automatically test generated project directories. You can also manually check them. The generated paths are in the pytest output

```bash
make test
( \
       . .venv/bin/activate; \
       pylint test/*.py; \
    )

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)

( \
       . .venv/bin/activate; \
       python3 -m pytest -o log_cli=true -s -v test; \
    )
==================================================================================================================================================================================================== test session starts ====================================================================================================================================================================================================
platform darwin -- Python 3.9.2, pytest-6.2.5, py-1.11.0, pluggy-1.0.0 -- /Users/nmarks/Projects/cookiecutter-ansible-role/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/nmarks/Projects/cookiecutter-arole-packer, configfile: pytest.ini
plugins: testinfra-6.4.0
collected 2 items

test/template_test.py::TestClass::test_[local-ccinput0]
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- live log call -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2021-12-29 04:58:32 [    INFO] tmpdir: /private/var/folders/72/cmp8x83n3js_spr_3hvvdgch0000gn/T/pytest-of-nmarks/pytest-14/test__local_ccinput0_0 (template_test.py:45)
PASSED
test/template_test.py::TestClass::test_[local-ccinput1]
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- live log call -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
2021-12-29 04:58:32 [    INFO] tmpdir: /private/var/folders/72/cmp8x83n3js_spr_3hvvdgch0000gn/T/pytest-of-nmarks/pytest-14/test__local_ccinput1_0 (template_test.py:45)
PASSED

===================================================================================================================================================================================================== 2 passed in 0.47s =====================================================================================================================================================================================================
❯
```
