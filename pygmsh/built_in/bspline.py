# -*- coding: utf-8 -*-
#
from .line_base import LineBase
from .point import Point


class Bspline(LineBase):
    """
    Generates the BSpline GMSH function.

    Parameters
    ----------
    control_points : array-like[N][3]
        Coordinates of control points needed to construct b-spline.
    """

    def __init__(self, control_points):
        super(Bspline, self).__init__()

        for c in control_points:
            assert isinstance(c, Point)
        assert len(control_points) > 1

        self.control_points = control_points

        self.code = '\n'.join([
            '{} = newl;'.format(self.id),
            'BSpline({}) = {{{}}};'.format(
                self.id, ', '.join([c.id for c in self.control_points])
            )])
        return
