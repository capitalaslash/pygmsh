from math import pi
import pytest

import pygmsh
from helpers import compute_volume


@pytest.mark.skipif(pygmsh.get_gmsh_major_version() < 3, reason="requires Gmsh >= 3")
def test():
    geom = pygmsh.opencascade.Geometry()

    geom.add_cone(
        [0.0, 0.0, 0.0], [0.0, 0.0, 1.0], 1.0, 0.3, 1.25 * pi, char_length=0.1
    )

    ref = 0.90779252263
    mesh = pygmsh.generate_mesh(geom)
    assert abs(compute_volume(mesh) - ref) < 1.0e-2 * ref
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("opencascade_cone.vtu", test())
