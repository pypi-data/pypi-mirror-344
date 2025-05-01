"""""" # start delvewheel patch
def _delvewheel_patch_1_10_1():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pysymregg.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-pysymregg-1.0.2')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-pysymregg-1.0.2')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_10_1()
del _delvewheel_patch_1_10_1
# end delvewheel patch

import atexit
from contextlib import contextmanager
from threading import Lock
from typing import Iterator, List
from io import StringIO
import tempfile
import csv

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.metrics import mean_squared_error, r2_score

from ._binding import (
    unsafe_hs_pysymregg_version,
    unsafe_hs_pysymregg_main,
    unsafe_hs_pysymregg_run,
    unsafe_hs_pysymregg_init,
    unsafe_hs_pysymregg_exit,
)

VERSION: str = "1.3.0"


_hs_rts_init: bool = False
_hs_rts_lock: Lock = Lock()


def hs_rts_exit() -> None:
    global _hs_rts_lock
    with _hs_rts_lock:
        unsafe_hs_pysymregg_exit()


@contextmanager
def hs_rts_init(args: List[str] = []) -> Iterator[None]:
    global _hs_rts_init
    global _hs_rts_lock
    with _hs_rts_lock:
        if not _hs_rts_init:
            _hs_rts_init = True
            unsafe_hs_pysymregg_init(args)
            atexit.register(hs_rts_exit)
    yield None


def version() -> str:
    with hs_rts_init():
        return unsafe_hs_pysymregg_version()


def main(args: List[str] = []) -> int:
    with hs_rts_init(args):
        return unsafe_hs_pysymregg_main()

def pysymregg_run(dataset: str, gen: int, alg: str, maxSize: int, nonterminals: str, loss: str, optIter: int, optRepeat: int, nParams: int, split: int, dumpTo: str, loadFrom: str) -> str:
    with hs_rts_init():
        return unsafe_hs_pysymregg_run(dataset, gen, alg, maxSize, nonterminals, loss, optIter, optRepeat, nParams, split, dumpTo, loadFrom)

class PySymRegg(BaseEstimator, RegressorMixin):
    """ Builds a symbolic regression model using symregg.

    Parameters
    ----------
    gen : int, default=100
        The number of generations.

    alg : {"BestFirst", "OnlyRandom"}, default="BestFirst"
        Whether to try combining expressions from the fronts/elite (BestFirst)
        or just trying to generate random expressions (OnlyRandom).

    maxSize : int, default=15
        Maximum allowed size for the expression.
        This should not be larger than 100 as the e-graph may grow
        too large.

    nonterminals : str, default="add,sub,mul,div"
        String of a comma separated list of nonterminals.
        These are the allowed functions to be used during the search.
        Available functions: add,sub,mul,div,power,powerabs,aq,abs,sin,cos,
                             tan,sinh,cosh,tanh,asin,acos,atan,asinh,acosh,
                             atanh,sqrt,sqrtabs,cbrt,square,log,logabs,exp,
                             recip,cube.
        Where `aq` is the analytical quotient (x/sqrt(1 + y^2)),
              `powerabs` is the protected power (x^|y|)
              `sqrtabs` is the protected sqrt (sqrt(|x|))
              `logabs` is the protected log (log(|x|))
              `recip` is the reciprocal (1/x)
              `cbrt` is the cubic root

    loss : {"MSE", "Gaussian", "Bernoulli", "Poisson"}, default="MSE"
        Loss function used to evaluate the expressions:
        - MSE (mean squared error) should be used for regression problems.
        - Gaussian likelihood should be used for regression problem when you want to
          fit the error term.
        - Bernoulli likelihood should be used for classification problem.
        - Poisson likelihood should be used when the data distribution follows a Poisson.

    optIter : int, default=50
        Number of iterations for the parameter optimization.

    optRepeat : int, default=2
        Number of restarts for the parameter optimization.

    nParams : int, default=-1
        Maximum number of parameters. If set to -1 it will
        allow the expression to have any number of parameters.
        If set to a number > 0, it will limit the number of parameters,
        but allow it to appear multiple times in the expression.
        E.g., t0 * x0 + exp(t0*x0 + t1)

    split : int, default=1
        How to split the data to create the validation set.
        If set to 1, it will use the whole data for fitting the parameter and
        calculating the fitness function.
        If set to n>1, it will use 1/n for calculating the fitness function
        and the reminder for fitting the parameter.

    dumpTo : str, default=""
        If not empty, it will save the final e-graph into the filename.

    loadFrom : str, default=""
        If not empty, it will load an e-graph and resume the search.
        The user must ensure that the loaded e-graph is from the same
        dataset and loss function.

    Examples
    --------
    >>> from pysymregg import PySymRegg
    >>> import numpy as np
    >>> X = np.arange(100).reshape(100, 1)
    >>> y = np.zeros((100, ))
    >>> estimator = PySymRegg()
    >>> estimator.fit(X, y)
    """
    def __init__(self, gen = 100, alg = "BestFirst", maxSize = 15, nonterminals = "add,sub,mul,div", loss = "MSE", optIter = 50, optRepeat = 2, nParams = -1, split = 1, dumpTo = "", loadFrom = ""):
        nts = "add,sub,mul,div,power,powerabs,\
               aq,abs,sin,cos,tan,sinh,cosh,tanh,\
               asin,acos,atan,asinh,acosh,atanh,sqrt,\
               sqrtabs,cbrt,square,log,logabs,exp,recip,cube"
        losses = ["MSE", "Gaussian", "Bernoulli", "Poisson"]
        if gen < 1:
            raise ValueError('gen should be greater than 1')
        if alg not in ["BestFirst", "OnlyRandom"]:
            raise ValueError('alg must be either BestFirst or OnlyRandom')
        if maxSize < 1 or maxSize > 100:
            raise ValueError('maxSize should be a value between 1 and 100')
        if any(t not in nts for t in nonterminals):
            raise ValueError('nonterminals must be a comma separated list of one or more of ', nts)
        if loss not in losses:
            raise ValueError('loss must be one of ', losses)
        if optIter < 0:
            raise ValueError('optIter must be a positive number')
        if optRepeat < 0:
            raise ValueError('optRepeat must be a positive number')
        if nParams < -1:
            raise ValueError('nParams must be either -1 or a positive number')
        if split < 1:
            raise ValueError('split must be equal or greater than 1')
        self.gen = gen
        self.alg = alg
        self.maxSize = maxSize
        self.nonterminals = nonterminals
        self.loss = loss
        self.optIter = optIter
        self.optRepeat = optRepeat
        self.nParams = nParams
        self.split = split
        self.dumpTo = dumpTo
        self.loadFrom = loadFrom
        self.is_fitted_ = False

    def fit(self, X, y):
        ''' Fits the regression model.

        Parameters
        ----------
        X : np.array
            An m x n np.array describing m observations of n features.
        y : np.array
            An np.array of size m with the measured target values.

        A table with the fitted models and additional information
        will be stored as a Pandas dataframe in self.results.
        '''
        if X.ndim == 1:
            X = X.reshape(-1,1)
        y = y.reshape(-1, 1)
        combined = np.hstack([X, y])
        header = [f"x{i}" for i in range(X.shape[1])] + ["y"]
        with tempfile.NamedTemporaryFile(mode='w+', newline='', delete=False, suffix='.csv') as temp_file:
            writer = csv.writer(temp_file)
            writer.writerow(header)
            writer.writerows(combined)
            dataset = temp_file.name

        csv_data = pysymregg_run(dataset, self.gen, self.alg, self.maxSize, self.nonterminals, self.loss, self.optIter, self.optRepeat, self.nParams, self.split, self.dumpTo, self.loadFrom)
        if len(csv_data) > 0:
            csv_io = StringIO(csv_data.strip())
            self.results = pd.read_csv(csv_io, header=0)
            self.is_fitted_ = True
        return self

    def predict(self, X):
        ''' Generates the prediction using the best model (selected by accuracy)

        Parameters
        ----------
        X : np.array
            An m x n np.array describing m observations of n features.
            This array must have the same number of features as the training data.

        Return
        ------
        y : np.array
            A vector of predictions
        '''
        check_is_fitted(self)
        return self.evaluate_best_model(X)
    def evaluate_best_model(self, x):
        if x.ndim == 1:
            x = x.reshape(-1,1)
        t = np.array(list(map(float, self.results.iloc[-1].theta.split(";"))))
        return eval(self.results.iloc[-1].Numpy)
    def evaluate_model(self, ix, x):
        if x.ndim == 1:
            x = x.reshape(-1,1)
        t = np.array(list(map(float, self.results.iloc[-1].theta.split(";"))))
        return eval(self.results.iloc[i].Numpy)
    def score(self, X, y):
        ypred = self.evaluate_best_model(X)
        return r2_score(y, ypred)
