# Tracking test results

## Test results, 24/03/2025, pre cf-python new release and new cf-plot release

### From running one by one

ExamplesTest:
1 pass
2 pass
3 pass
4 pass
5 pass
6 pass
7 pass
8 pass
9 UNEXPECTED SUCCESS
10  pass
11 pass
12 pass
13 pass
14 pass
15 pass
16 EXPECTED FAILURE
17 FAILURE
18 pass
19 pass
20 pass
21 pass
22 pass
23 pass
24 EXPECTED FAILURE
25 EXPECTED FAILURE
26 EXPECTED FAILURE
27 pass
28 pass
29 pass
30 FAIL
31 pass
32 pass
33 pass
34 pass
35 pass
36 pass
37 pass
38 pass
39 pass BUT HAS SOME SPAM WARNINGS RE shapely
40  pass BUT HAS SOME SPAM WARNINGS RE shapely
41 FAILURE ON PLOT COMPARISON HAS SOME SPAM WARNINGS RE shapely
42 pass BUT HAS SOME SPAM WARNINGS RE shapely
43 pass
END OF NUMBERS

UnnumberedExamplesTest:
BY NAME:
test_example_unstructured_lfric_1: pass
test_example_unstructured_lfric_2: pass
test_example_unstructured_lfric_3: pass
test_example_unstructured_orca_1: EXPECTED FAILURE
test_example_unstructured_station_data_1: EXPECTED FAILURE


NOTE: test 33 (or at least, one of the tests, might not be that one) opens up a plot window

### From running as test suite

╰─ python test_examples.py ExamplesTest                                                            ─╯
==================
Regression testing
==================


___Running code for test_example_1___
___Comparing output images for test_example_1___
.
___Running code for test_example_10___
___Comparing output images for test_example_10___
.
___Running code for test_example_11___
___Comparing output images for test_example_11___
.
___Running code for test_example_12___
___Comparing output images for test_example_12___
.
___Running code for test_example_13___
___Comparing output images for test_example_13___
.
___Running code for test_example_14___
___Comparing output images for test_example_14___
.
___Running code for test_example_15___
___Comparing output images for test_example_15___
.
___Running code for test_example_16___
x
___Running code for test_example_16b___
___Comparing output images for test_example_16b___
.
___Running code for test_example_16c___
___Comparing output images for test_example_16c___
.
___Running code for test_example_17___
___Comparing output images for test_example_17___
F
___Running code for test_example_18___
___Comparing output images for test_example_18___
.
___Running code for test_example_19___
___Comparing output images for test_example_19___
.
___Running code for test_example_19a___
___Comparing output images for test_example_19a___
.
___Running code for test_example_19b___
___Comparing output images for test_example_19b___
.
___Running code for test_example_2___
___Comparing output images for test_example_2___
.
___Running code for test_example_20___
___Comparing output images for test_example_20___
..
___Running code for test_example_21other___
___Comparing output images for test_example_21other___
.
___Running code for test_example_22___
___Comparing output images for test_example_22___
.
___Running code for test_example_22other___
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/site-packages/matplotlib/cbook.py:1762: DeprecationWarning: Conversion of an array with ndim > 0 to a scalar is deprecated, and will error in future. Ensure you extract a single element from your array before performing this operation. (Deprecated NumPy 1.25.)
  return math.isfinite(val)
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/site-packages/matplotlib/cbook.py:1762: DeprecationWarning: Conversion of an array with ndim > 0 to a scalar is deprecated, and will error in future. Ensure you extract a single element from your array before performing this operation. (Deprecated NumPy 1.25.)
  return math.isfinite(val)
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/site-packages/matplotlib/cbook.py:1762: DeprecationWarning: Conversion of an array with ndim > 0 to a scalar is deprecated, and will error in future. Ensure you extract a single element from your array before performing this operation. (Deprecated NumPy 1.25.)
  return math.isfinite(val)
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/site-packages/matplotlib/cbook.py:1762: DeprecationWarning: Conversion of an array with ndim > 0 to a scalar is deprecated, and will error in future. Ensure you extract a single element from your array before performing this operation. (Deprecated NumPy 1.25.)
  return math.isfinite(val)
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/site-packages/matplotlib/cbook.py:1762: DeprecationWarning: Conversion of an array with ndim > 0 to a scalar is deprecated, and will error in future. Ensure you extract a single element from your array before performing this operation. (Deprecated NumPy 1.25.)
  return math.isfinite(val)
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/site-packages/matplotlib/cbook.py:1762: DeprecationWarning: Conversion of an array with ndim > 0 to a scalar is deprecated, and will error in future. Ensure you extract a single element from your array before performing this operation. (Deprecated NumPy 1.25.)
  return math.isfinite(val)
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/site-packages/matplotlib/cbook.py:1762: DeprecationWarning: Conversion of an array with ndim > 0 to a scalar is deprecated, and will error in future. Ensure you extract a single element from your array before performing this operation. (Deprecated NumPy 1.25.)
  return math.isfinite(val)
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/site-packages/matplotlib/cbook.py:1762: DeprecationWarning: Conversion of an array with ndim > 0 to a scalar is deprecated, and will error in future. Ensure you extract a single element from your array before performing this operation. (Deprecated NumPy 1.25.)
  return math.isfinite(val)
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/site-packages/matplotlib/cbook.py:1762: DeprecationWarning: Conversion of an array with ndim > 0 to a scalar is deprecated, and will error in future. Ensure you extract a single element from your array before performing this operation. (Deprecated NumPy 1.25.)
  return math.isfinite(val)
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/site-packages/matplotlib/cbook.py:1762: DeprecationWarning: Conversion of an array with ndim > 0 to a scalar is deprecated, and will error in future. Ensure you extract a single element from your array before performing this operation. (Deprecated NumPy 1.25.)
  return math.isfinite(val)
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/site-packages/matplotlib/cbook.py:1762: DeprecationWarning: Conversion of an array with ndim > 0 to a scalar is deprecated, and will error in future. Ensure you extract a single element from your array before performing this operation. (Deprecated NumPy 1.25.)
  return math.isfinite(val)
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/site-packages/matplotlib/cbook.py:1762: DeprecationWarning: Conversion of an array with ndim > 0 to a scalar is deprecated, and will error in future. Ensure you extract a single element from your array before performing this operation. (Deprecated NumPy 1.25.)
  return math.isfinite(val)
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/site-packages/matplotlib/text.py:756: DeprecationWarning: Conversion of an array with ndim > 0 to a scalar is deprecated, and will error in future. Ensure you extract a single element from your array before performing this operation. (Deprecated NumPy 1.25.)
  posx = float(self.convert_xunits(self._x))
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/site-packages/matplotlib/text.py:757: DeprecationWarning: Conversion of an array with ndim > 0 to a scalar is deprecated, and will error in future. Ensure you extract a single element from your array before performing this operation. (Deprecated NumPy 1.25.)
  posy = float(self.convert_yunits(self._y))
___Comparing output images for test_example_22other___
.
___Running code for test_example_23___
___Comparing output images for test_example_23___
.
___Running code for test_example_23other___
___Comparing output images for test_example_23other___
.x
___Running code for test_example_25___
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/site-packages/matplotlib/cbook.py:97: ResourceWarning: unclosed file <_io.TextIOWrapper name='cfplot_data/synop_data.txt' mode='r' encoding='UTF-8'>
  def __init__(self, obj):
ResourceWarning: Enable tracemalloc to get the object allocation traceback
x
___Running code for test_example_26___
x
___Running code for test_example_27___
___Comparing output images for test_example_27___
.
___Running code for test_example_28___
___Comparing output images for test_example_28___
.
___Running code for test_example_29___
<frozen importlib._bootstrap_external>:752: ResourceWarning: unclosed file <_io.TextIOWrapper name='cfplot_data/synop_data.txt' mode='r' encoding='UTF-8'>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
___Comparing output images for test_example_29___
.
___Running code for test_example_3___
___Comparing output images for test_example_3___
.
___Running code for test_example_30___
E
___Running code for test_example_31___
/home/slb93/miniconda3/envs/cf-env-312-numpy2/lib/python3.12/subprocess.py:1127: ResourceWarning: subprocess 143137 is still running
  _warn("subprocess %s is still running" % self.pid,
ResourceWarning: Enable tracemalloc to get the object allocation traceback
___Comparing output images for test_example_31___
.
___Running code for test_example_32___
x
___Running code for test_example_33___
___Comparing output images for test_example_33___
.
___Running code for test_example_34___
___Comparing output images for test_example_34___
.
___Running code for test_example_35___
___Comparing output images for test_example_35___
.
___Running code for test_example_36___
___Comparing output images for test_example_36___
.
___Running code for test_example_37___
___Comparing output images for test_example_37___
.
___Running code for test_example_38___
___Comparing output images for test_example_38___
.
___Running code for test_example_39___
___Comparing output images for test_example_39___
.
___Running code for test_example_4___
___Comparing output images for test_example_4___
.
___Running code for test_example_40___
___Comparing output images for test_example_40___
.
___Running code for test_example_41___
___Comparing output images for test_example_41___
F
___Running code for test_example_42___
___Comparing output images for test_example_42___
.
___Running code for test_example_42a___
___Comparing output images for test_example_42a___
.
___Running code for test_example_43___
x
___Running code for test_example_5___
___Comparing output images for test_example_5___
.
___Running code for test_example_6___
___Comparing output images for test_example_6___
.
___Running code for test_example_7___
___Comparing output images for test_example_7___
.
___Running code for test_example_8___
___Comparing output images for test_example_8___
.
___Running code for test_example_9___
___Comparing output images for test_example_9___
u
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
Ran 51 tests in 169.862s

FAILED (failures=2, errors=1, expected failures=6, unexpected successes=1)


**************

