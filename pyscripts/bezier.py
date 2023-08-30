"""
A module providing some utility functions regarding Bezier path manipulation.
"""
import math
import numpy as np


class BezierSegment:
    """
    A d-dimensional Bezier segment.

    Parameters
    ----------
    control_points : (N, d) array
        Location of the *N* control points.
    """

    def __init__(self, control_points):
        self._cpoints = np.asarray(control_points)
        self._N, self._d = self._cpoints.shape
        self._orders = np.arange(self._N)
        coeff = [math.factorial(self._N - 1)
                 // (math.factorial(i) * math.factorial(self._N - 1 - i))
                 for i in range(self._N)]
        self._px = (self._cpoints.T * coeff).T

    def __call__(self, t):
        """
        Evaluate the Bezier curve at point(s) t in [0, 1].

        Parameters
        ----------
        t : (k,) array-like
            Points at which to evaluate the curve.

        Returns
        -------
        (k, d) array
            Value of the curve for each point in *t*.
        """
        t = np.asarray(t)
        return (np.power.outer(1 - t, self._orders[::-1])
                * np.power.outer(t, self._orders)) @ self._px

    def point_at_t(self, t):
        """
        Evaluate the curve at a single point, returning a tuple of *d* floats.
        """
        return tuple(self(t))
