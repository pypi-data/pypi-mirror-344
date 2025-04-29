## 04-04-2025, after the cf-python 3.17.0 release:

### python test_examples.py ExamplesTest

======================================================================
ERROR: test_example_30 (__main__.ExamplesTest.test_example_30)
Test Example 30: two axis plotting.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/slb93/git-repos/cf-plot/cfplot/test/test_examples.py", line 71, in wrapper
    test_method(_self)
  File "/home/slb93/git-repos/cf-plot/cfplot/test/test_examples.py", line 1133, in test_example_30
    u1 = u.subspace(Y=-61.12099075)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/slb93/git-repos/cf-python/cf/subspacefield.py", line 353, in __call__
    raise error
  File "/home/slb93/git-repos/cf-python/cf/subspacefield.py", line 348, in __call__
    out = field[indices]
          ~~~~~^^^^^^^^^
  File "/home/slb93/git-repos/cf-python/cf/field.py", line 445, in __getitem__
    new_data = data[tuple(findices)]
               ~~~~^^^^^^^^^^^^^^^^^
  File "/home/slb93/git-repos/cf-python/cf/data/data.py", line 338, in __getitem__
    new = super(Data, d).__getitem__(indices)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/slb93/git-repos/cfdm/cfdm/data/data.py", line 746, in __getitem__
    raise IndexError(
IndexError: Index [(slice(None, None, None), slice(None, None, None), array([], dtype=int64), slice(None, None, None))] selects no elements from data with shape (1, 23, 160, 1)

======================================================================
FAIL: test_example_17 (__main__.ExamplesTest.test_example_17)
Test Example 17: basic stipple plot.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/slb93/git-repos/cf-plot/cfplot/test/test_examples.py", line 87, in wrapper
    _self.assertIsNone(image_cmp_result, msg=msg)
AssertionError: {'rms': np.float64(99.26315299432427), 'expected': './reference-example-images/ref_fig_17.png', 'actual': './generated-example-images/gen_fig_17.png', 'diff': './generated-example-images/gen_fig_17-failed-diff.png', 'tol': 0.01} is not None : 
Plot comparison shows differences, see result dict for details.

======================================================================
FAIL: test_example_41 (__main__.ExamplesTest.test_example_41)
Test Example 41: feature propagation over Europe.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/slb93/git-repos/cf-plot/cfplot/test/test_examples.py", line 87, in wrapper
    _self.assertIsNone(image_cmp_result, msg=msg)
AssertionError: {'rms': np.float64(0.010610706882150113), 'expected': './reference-example-images/ref_fig_41.png', 'actual': './generated-example-images/gen_fig_41.png', 'diff': './generated-example-images/gen_fig_41-failed-diff.png', 'tol': 0.01} is not None : 
Plot comparison shows differences, see result dict for details.

======================================================================
UNEXPECTED SUCCESS: test_example_9 (__main__.ExamplesTest.test_example_9)
Test Example 9: longitude-pressure plot.
----------------------------------------------------------------------
Ran 51 tests in 93.698s

FAILED (failures=2, errors=1, expected failures=6, unexpected successes=1)

Fixed the one unexpected success, example 9, which looks right plot-comp wise

### python test_examples.py UnnumberedExamplesTest

==================
Regression testing
==================

There was a problem parsing the UGRID mesh topology variable. Ignoring the UGRID mesh for 'u1'.
There was a problem parsing the UGRID mesh topology variable. Ignoring the UGRID mesh for 'u2'.
.There was a problem parsing the UGRID mesh topology variable. Ignoring the UGRID mesh for 'u1'.
There was a problem parsing the UGRID mesh topology variable. Ignoring the UGRID mesh for 'u2'.
.There was a problem parsing the UGRID mesh topology variable. Ignoring the UGRID mesh for 'u1'.
There was a problem parsing the UGRID mesh topology variable. Ignoring the UGRID mesh for 'u2'.
.xx
----------------------------------------------------------------------
Ran 5 tests in 6.912s

OK (expected failures=2)

### NEXT

TODO: tag failures with specific cf-plot bugs!
NOW have failures:======================================================================
ERROR: test_example_30 (__main__.ExamplesTest.test_example_30)
Test Example 30: two axis plotting.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/slb93/git-repos/cf-plot/cfplot/test/test_examples.py", line 71, in wrapper
    test_method(_self)
  File "/home/slb93/git-repos/cf-plot/cfplot/test/test_examples.py", line 1132, in test_example_30
    u1 = u.subspace(Y=-61.12099075)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/slb93/git-repos/cf-python/cf/subspacefield.py", line 353, in __call__
    raise error
  File "/home/slb93/git-repos/cf-python/cf/subspacefield.py", line 348, in __call__
    out = field[indices]
          ~~~~~^^^^^^^^^
  File "/home/slb93/git-repos/cf-python/cf/field.py", line 445, in __getitem__
    new_data = data[tuple(findices)]
               ~~~~^^^^^^^^^^^^^^^^^
  File "/home/slb93/git-repos/cf-python/cf/data/data.py", line 338, in __getitem__
    new = super(Data, d).__getitem__(indices)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/slb93/git-repos/cfdm/cfdm/data/data.py", line 746, in __getitem__
    raise IndexError(
IndexError: Index [(slice(None, None, None), slice(None, None, None), array([], dtype=int64), slice(None, None, None))] selects no elements from data with shape (1, 23, 160, 1)

======================================================================
FAIL: test_example_17 (__main__.ExamplesTest.test_example_17)
Test Example 17: basic stipple plot.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/slb93/git-repos/cf-plot/cfplot/test/test_examples.py", line 87, in wrapper
    _self.assertIsNone(image_cmp_result, msg=msg)
AssertionError: {'rms': np.float64(99.26315299432427), 'expected': './reference-example-images/ref_fig_17.png', 'actual': './generated-example-images/gen_fig_17.png', 'diff': './generated-example-images/gen_fig_17-failed-diff.png', 'tol': 0.01} is not None : 
Plot comparison shows differences, see result dict for details.

======================================================================
FAIL: test_example_41 (__main__.ExamplesTest.test_example_41)
Test Example 41: feature propagation over Europe.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/slb93/git-repos/cf-plot/cfplot/test/test_examples.py", line 87, in wrapper
    """
        
AssertionError: {'rms': np.float64(0.010610706882150113), 'expected': './reference-example-images/ref_fig_41.png', 'actual': './generated-example-images/gen_fig_41.png', 'diff': './generated-example-images/gen_fig_41-failed-diff.png', 'tol': 0.01} is not None : 
Plot comparison shows differences, see result dict for details.

----------------------------------------------------------------------
Ran 51 tests in 109.472s

FAILED (failures=2, errors=1, expected failures=6)



