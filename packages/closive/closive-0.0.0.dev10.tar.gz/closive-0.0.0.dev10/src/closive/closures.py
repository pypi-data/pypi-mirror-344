"""Closures

Abstractions for callback-heavy control flows.
"""

from copy import copy
from collections.abc import Callable
from functools import wraps
from typing import Optional


class _Closure:
    """A callable decorator factory that supports chaining transformations in a pipeline."""

    def __init__(self, fn: Callable, debug: bool = False):
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

    def __rshift__(self, other):
        """
        Enables chaining using the >> operator.
        """
        if not callable(other):
            raise TypeError("Can only chain callables with >>")
        new = copy(self)
        new._callbacks = self._callbacks + [other]
        return new

    @property
    def callbacks(self):
        return self._callbacks

    @callbacks.setter
    def callbacks(self, value):
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
            raise TypeError("pipe expects a callable")
        self._callbacks.append(fn)
        return self

    def drain(self) -> "_Closure":
        """Remove a callback from the end of the pipeline."""
        if not self._callbacks:
            raise ValueError("Cannot drain callback from pipeline.")

        self._callbacks.pop()
        
        return self

    def repeat(self, x: int) -> "_Closure":
        """
        Repeats the last callback x additional times.
        """
        if not self._callbacks:
            raise ValueError("No callback to repeat.")
        if x < 1:
            raise ValueError("Repeat count must be at least 1.")
        
        callback = self._callbacks[-1]
        for _ in range(x):
            self.pipe(callback)
        return self

    # Aliases for a more expressive API
    do = next = then = pipe
    re = redo = rept = repeat


# Main public API
def closure(fn: Callable, debug: bool = False) -> _Closure:
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
    return _Closure(fn, debug=debug)


# Transformation conveniences
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
    return r ** (1/2)
    
def cuberoot(r, *args, **kwargs):
    """Returns the cube root of the input value."""
    return r ** (1/3)

def root(n):
    """Returns a function that returns the nth root of its input value."""
    def inner(r, *args, **kwargs):
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
        raise ImportError from e

    x, m, b = params[0:3]
    
    print("m = {}".format(m))
    print("x = {}".format(x))
    print("b = {}".format(b))
    
    y = np.array([(m * n + b) for n in x])
    df = pd.DataFrame({"x": x, "y": y})
    
    return df


# Visualization
def linvis(df, *args, **kwargs):
    """Creates a linear visualization from a DataFrame with x and y columns.
    
    Returns:
        A seaborn.objects.Plot object.
    """
    try:
        import seaborn as sns
        import seaborn.objects as so
    except Exception as e:
        raise ImportError("[closive] Failed to import seaborn.") from e
    
    sns.set_palette("magma")
    
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
    
    # Test the desired pipeline
    @closure(square) >> add(3) >> multiply(2)
    def g(x): return x
    
    print(g(5))  # Should print 56 = ((5^2) + 3) * 2


