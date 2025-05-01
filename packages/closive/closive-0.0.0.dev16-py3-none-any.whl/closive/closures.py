"""Closures

Abstractions for callback-heavy control flows.
"""

from copy import copy
from collections.abc import Callable
from functools import wraps
from typing import Optional, Union, Any


class _Closure:
    """A callable decorator factory that supports chaining transformations in a pipeline."""

    def __init__(self, fn: Optional[Callable] = None, debug: bool = False):
        """
        Instantiates a new closure.

        Args:
          fn: 
            The function whose return value will be passed as the first argument to the next callback.
          debug:
            If True, prints each step of the transformation pipeline.
        """
        if not callable(fn):
            raise TypeError("Expected a callable to initialize closure.")
        self._callbacks = [fn]
        self._count = len(self._callbacks)
        self._debug = debug
        self._nextcb = self._callbacks[-1] or None

    def __call__(self, target):
        """
        Makes the _Closure class callable as a decorator.
        """
        @wraps(target)
        def wrapped(*args, **kwargs):
            result = target(*args, **kwargs)
            if self._debug:
                print(f"[closure] Initial result from {target.__name__}: {result!r}")
            for idx, fn in enumerate(self._callbacks):
                result = fn(result, *args, **kwargs)
                if self._debug:
                    print(f"[closure] After step {idx+1} ({fn.__name__}): {result!r}")
            return result
        return wrapped

    def __rshift__(self, other: Union['_Closure', Callable]) -> '_Closure':
        """
        Enables chaining using the >> operator.
        Handles both _Closure instances and callables.
        """
        new = copy(self)
        
        if isinstance(other, _Closure):
            # Combine two closure pipelines
            new._callbacks = self._callbacks + other._callbacks
        elif callable(other):
            # Add a callable function to the pipeline
            new._callbacks.append(other)
        else:
            raise TypeError(f"Cannot chain with >> - expected a callable or _Closure, got {type(other).__name__}")
            
        return new

    @property
    def callbacks(self):
        return self._callbacks

    @callbacks.setter
    def callbacks(self, value):
        if not all(callable(fn) for fn in value):
            raise TypeError("All callbacks must be callable")
        self._callbacks = value
    
    @property
    def count(self):
        return len(self._callbacks)

    @property
    def nextcb(self):
        return self._callbacks[0] if self._callbacks else None
   
    def pipe(self, fn: Callable) -> "_Closure":
        """Add a callback to the pipeline."""
        if not callable(fn):
            raise TypeError(f"pipe expects a callable, got {type(fn).__name__}")
        new = copy(self)
        new._callbacks.append(fn)
        return new

    def drain(self) -> "_Closure":
        """Remove a callback from the end of the pipeline."""
        if not self._callbacks:
            raise ValueError("Cannot drain callback from empty pipeline.")
        
        new = copy(self)
        new._callbacks.pop()
        return new

    def repeat(self, x: int) -> "_Closure":
        """
        Repeats the last callback x additional times.
        """
        if not self._callbacks:
            raise ValueError("No callback to repeat in empty pipeline.")
        if x < 1:
            raise ValueError(f"Repeat count must be at least 1, got {x}")
        
        new = copy(self)
        callback = new._callbacks[-1]
        for _ in range(x):
            new._callbacks.append(callback)
        return new

    # Operator methods integrated into the _Closure class
    def add(self, n: Union[int, float]) -> "_Closure":
        """Add a function that adds n to its input value."""
        def inner(r, *args, **kwargs):
            return r + n
        inner.__name__ = f"add({n})"
        return self.pipe(inner)

    def subtract(self, n: Union[int, float]) -> "_Closure":
        """Add a function that subtracts n from its input value."""
        def inner(r, *args, **kwargs):
            return r - n
        inner.__name__ = f"subtract({n})"
        return self.pipe(inner)

    def multiply(self, n: Union[int, float]) -> "_Closure":
        """Add a function that multiplies its input value by n."""
        def inner(r, *args, **kwargs):
            return r * n
        inner.__name__ = f"multiply({n})"
        return self.pipe(inner)

    def divide(self, n: Union[int, float]) -> "_Closure":
        """Add a function that divides its input value by n."""
        if n == 0:
            raise ValueError("Cannot divide by zero")
        def inner(r, *args, **kwargs):
            return r / n
        inner.__name__ = f"divide({n})"
        return self.pipe(inner)

    def exponentiate(self, n: Union[int, float]) -> "_Closure":
        """Add a function that raises its input value to the power of n."""
        def inner(r, *args, **kwargs):
            return r ** n
        inner.__name__ = f"exponentiate({n})"
        return self.pipe(inner)

    def square(self) -> "_Closure":
        """Add a function that squares the input value."""
        def square_fn(r, *args, **kwargs):
            return r ** 2
        square_fn.__name__ = "square"
        return self.pipe(square_fn)

    def cube(self) -> "_Closure":
        """Add a function that cubes the input value."""
        def cube_fn(r, *args, **kwargs):
            return r ** 3
        cube_fn.__name__ = "cube"
        return self.pipe(cube_fn)

    def squareroot(self) -> "_Closure":
        """Add a function that returns the square root of the input value."""
        def sqrt_fn(r, *args, **kwargs):
            if r < 0:
                raise ValueError(f"Cannot compute square root of negative number: {r}")
            return r ** (1/2)
        sqrt_fn.__name__ = "squareroot"
        return self.pipe(sqrt_fn)
    
    def cuberoot(self) -> "_Closure":
        """Add a function that returns the cube root of the input value."""
        def cbrt_fn(r, *args, **kwargs):
            return r ** (1/3)
        cbrt_fn.__name__ = "cuberoot"
        return self.pipe(cbrt_fn)

    def root(self, n: Union[int, float]) -> "_Closure":
        """Add a function that returns the nth root of its input value."""
        if n == 0:
            raise ValueError("Cannot compute 0th root")
        def root_fn(r, *args, **kwargs):
            if n % 2 == 0 and r < 0:
                raise ValueError(f"Cannot compute even root ({n}) of negative number: {r}")
            return r ** (1/n)
        root_fn.__name__ = f"root({n})"
        return self.pipe(root_fn)

    # Aliases for a more expressive API
    do = next = then = pipe
    re = redo = rept = repeat


# Main public API
def closure(fn: Optional[Callable] = None, debug: bool = False) -> _Closure:
    """Create a closure. 
    
    This is a factory function for creating a new closure pipeline.

    Args:
      fn: 
        The first transformation function in the pipeline.
      debug:
        Optional flag to enable debug prints.

    Returns:
      A _Closure instance wrapping the initial function.
    """
    if not fn:
        def fn(r, *args, **kwargs): return r
    
    return _Closure(fn, debug=debug)


# Standalone transformation functions (for backward compatibility)
def add(n):
    """Returns a function that adds n to its input value."""
    def inner(r, *args, **kwargs):
        return r + n
    inner.__name__ = f"add({n})"
    return inner

def subtract(n):
    """Returns a function that subtracts n from its input value."""
    def inner(r, *args, **kwargs):
        return r - n
    inner.__name__ = f"subtract({n})"
    return inner

def multiply(n):
    """Returns a function that multiplies its input value by n."""
    def inner(r, *args, **kwargs):
        return r * n
    inner.__name__ = f"multiply({n})"
    return inner

def divide(n):
    """Returns a function that divides its input value by n."""
    if n == 0:
        raise ValueError("Cannot divide by zero")
    def inner(r, *args, **kwargs):
        return r / n
    inner.__name__ = f"divide({n})"
    return inner

def exponentiate(n):
    """Returns a function that raises its input value to the power of n."""
    def inner(r, *args, **kwargs):
        return r ** n
    inner.__name__ = f"exponentiate({n})"
    return inner

def square(r, *args, **kwargs):
    """Returns the square of the input value."""
    return r ** 2

def cube(r, *args, **kwargs):
    """Returns the cube of the input value."""
    return r ** 3

def squareroot(r, *args, **kwargs):
    """Returns the square root of the input value."""
    if r < 0:
        raise ValueError(f"Cannot compute square root of negative number: {r}")
    return r ** (1/2)
    
def cuberoot(r, *args, **kwargs):
    """Returns the cube root of the input value."""
    return r ** (1/3)

def root(n):
    """Returns a function that returns the nth root of its input value."""
    if n == 0:
        raise ValueError("Cannot compute 0th root")
    def inner(r, *args, **kwargs):
        if n % 2 == 0 and r < 0:
            raise ValueError(f"Cannot compute even root ({n}) of negative number: {r}")
        return r ** (1/n)
    inner.__name__ = f"root({n})"
    return inner

def linfunc(params, *args, **kwargs):
    """Uses the provided linear parameters to process x.

    Args:
      params:
        A tuple containing (x, m, b) where:
        x: A list-like object containing a series of x values.
        m: A float or integer that represents the slope of the line.
        b: A float or integer that represents the line's y-intercept.
    """
    try:
        import pandas as pd
        import numpy as np
    except Exception as e:
        raise ImportError("Required libraries missing: pandas, numpy") from e

    if not params or len(params) < 3:
        raise ValueError("params must contain at least (x, m, b)")
        
    x, m, b = params[0:3]
    
    print("m = {}".format(m))
    print("x = {}".format(x))
    print("b = {}".format(b))
    
    try:
        y = np.array([(m * n + b) for n in x])
        df = pd.DataFrame({"x": x, "y": y})
    except Exception as e:
        raise ValueError(f"Error computing linear function: {e}")
    
    return df


# Visualization method
def linvis(df, *args, **kwargs):
    """Creates a linear visualization from a DataFrame with x and y columns.
    
    Returns:
        A seaborn.objects.Plot object.
    """
    try:
        import seaborn as sns
        import seaborn.objects as so
    except Exception as e:
        raise ImportError("Required library missing: seaborn") from e
    
    if 'x' not in df.columns or 'y' not in df.columns:
        raise ValueError("DataFrame must contain 'x' and 'y' columns")
    
    sns.set_palette("magma")
    
    try:
        p = (
            so.Plot(data=df, x="x", y="y")
            .add(so.Line())
            .label(title="y = mx + b")
            .theme({
                "figure.dpi": 300,
                "font.family": "sans-serif"
            })
        )
        return p
    except Exception as e:
        raise ValueError(f"Error creating visualization: {e}") from e


def to_dataframe(r, *args, **kwargs) -> tuple:
    """Converts the pipeline result and original input to a DataFrame.

    Creates a DataFrame with two columns:
    - "input": The original input values passed to the function.
    - "output": The transformed values after all pipeline operations.
    
    Args:
      r:
        The result from the pipeline (transformed values).
      *args:
        Arguments passed to the decorated function. First arg is used
        as input.
      **kwargs:
        Keyword arguments passed to the decorated function.
    
    Returns:
        pandas.DataFrame: A DataFrame with "input" and "output" columns.
    """
    try:
        import pandas as pd
        import numpy as np
    except ImportError as e:
        raise ImportError("Required libraries missing: pandas, numpy") from e
    
    if not args:
        raise ValueError("No input values found in args")
    
    input_val = args[0]  # Get the first argument passed to the decorated function
    
    # Handle different input types
    if isinstance(input_val, (list, tuple, np.ndarray)) and not isinstance(r, (list, tuple, np.ndarray)):
        # If input was array-like but output is scalar, we need to apply the transformation
        # to each element to get the corresponding outputs
        raise ValueError(
            "Cannot create DataFrame: array-like input resulted in scalar output. "
            "The transformation might not preserve the array structure."
        )
    
    # Create the DataFrame based on input and result types
    if isinstance(input_val, (list, tuple, np.ndarray)) and isinstance(r, (list, tuple, np.ndarray)):
        # Both input and output are array-like
        if len(input_val) != len(r):
            raise ValueError(
                f"Input and output arrays have different lengths: {len(input_val)} vs {len(r)}"
            )
        df = pd.DataFrame({
            "input": input_val,
            "output": r
        })
    else:
        # Scalar input and output
        df = pd.DataFrame({
            "input": np.array([input_val]),
            "output": np.array([r])
        })
    
    return args[0], df

def to_plot(r, *args, **kwargs) -> "_Closure":
    """Plot the data resulted by a transformation pipeline.
    
    Creates a seaborn plot from a univariate data frame (such as that
    returned by the `to_dataframe` method or the standalone `dataframe`
    function, both of which return a two-column data frame comprising
    the pipeline's input and output values.

    Args:
      r:
        The result of the last callback in the pipeline.
      *args:
        Arguments passed to the decorated function.
        Unused here but included to preserve pipeline sanity.
      **kwargs:
        Keyword arguments passed to the decorated function.
        Unused here but included to preserve pipeline sanity.
    
    Returns:
        A tuple containing r (unchanged), along with a seaborn.Plot
        object and the pandas.DataFrame object from which it derived,
        in that order.
    """
    try:
        import seaborn as sns
        import seaborn.objects as so
    except ImportError as e:
        raise ImportError(
            "Closive could not import seaborn. Please install it "
            "via `pip install seaborn`."
        )
    else:
        sns.set_palette("magma")

    # Extract the results tuple into separate objects
    result, df = r

    minx = min(df["input"]) - 1
    maxx = max(df["input"]) + 1
    miny = min(df["output"]) - 1
    maxy = max(df["output"]) + 1

    p = (
        so.Plot(data=df, x="input", y="output")
        .add(so.Line())
        .label(title="Results", x="Input", y="Output")
        .theme({
            "axes.edgecolor": "black",
            "axes.facecolor": "white",
            "axes.grid": True,
            "axes.labelsize": 10,
            "axes.labelweight": "bold",
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "figure.dpi": 200,
            "font.family": "monospace",
            "font.size": 9,
            "grid.color": "lightgray",
            "grid.linestyle": "--"
        })
        .layout(size=(6, 4))
        .limit(x=(minx, maxx), y=(miny, maxy))
    )

    return result, p, df

def _closure_to_plot(self):
    """Add a Seaborn Plot creation operation to the pipeline."""
    return self.pipe(to_plot)

def _closure_to_dataframe(self):
    """Add a DataFrame creation operation to the pipeline."""
    return self.pipe(to_dataframe)


# Standalone functions to be used with the >> operator.
def dataframe(r, *args, **kwargs):
    """Standalone function to convert pipeline results to a DataFrame."""
    return to_dataframe(r, *args, **kwargs)

def plot(r, *args, **kwargs):
    """Standalone function to convert results to a seaborn.Plot."""
    return to_plot(r, *args, **kwargs)
    

# Add method to create a linfunc closure
def _closure_linfunc(self):
    """Add a linear function operation to the pipeline."""
    return self.pipe(linfunc)

# Add method to create a linvis closure
def _closure_linvis(self):
    """Add a visualization operation to the pipeline."""
    return self.pipe(linvis)

# Add the methods to the _Closure class
_Closure.linfunc = _closure_linfunc
_Closure.linvis = _closure_linvis
_Closure.to_dataframe = _closure_to_dataframe
_Closure.to_plot = _closure_to_plot

# Pre-composed pipeline
linplot = closure(linfunc) >> linvis


if __name__ == "__main__":
    # Example usage
    @linplot
    def f(*params): return params
        
    x = [-3, -2, -1, 0, 1, 2, 3]
    m = 2
    b = 3.5

    result = f(x, m, b)
    result.show()  # Now result is just the plot object
    
    # Test the desired pipeline with the new API
    @closure(lambda x: x).square().multiply(2).add(3)
    def g(x): return x
    
    print(g(5))  # Should print 53 = ((5^2) * 2) + 3
    
    # Example with repeat
    def printr(r, *args, **kwargs):
        print("Callback returned: ", r)
        return r
        
    square_and_print = (
        closure(printr)
        .square().repeat(3)  # Square 3 additional times (4 total)
        .pipe(printr)
    )
    
    @square_and_print
    def h(x): return x
    
    print(h(2))  # Should print 2, then 4, then 16, then 65536, then 65536 again


