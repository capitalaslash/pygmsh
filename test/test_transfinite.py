"""Mesh a square using the transfinite algorithm and check that the numbers of
cells generated is correct.
"""
import pygmsh


def test(lcar=1.0):
    geom = pygmsh.built_in.Geometry()
    poly = geom.add_polygon(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]], lcar
    )

    geom.set_transfinite_surface(poly.surface, size=[11, 9], progression=1.2)

    pts = [
        geom.add_point(x, lcar=lcar)
        for x in [[2.0, 0.0, 0.0], [3.0, 0.0, 0.0], [2.0, 1.0, 0.0], [3.0, 1.0, 0.0]]
    ]
    lines = []
    lines.append(geom.add_line(pts[0], pts[1]))
    lines.append(geom.add_line(pts[2], pts[3]))
    lines.append(geom.add_line(pts[0], pts[2]))
    lines.append(geom.add_line(pts[1], pts[3]))
    ll = geom.add_line_loop((lines[0], lines[3], -lines[2], -lines[1]))
    surface = geom.add_plane_surface(ll)

    geom.set_transfinite_lines([lines[0], lines[1]], 11, progression=1.2)
    geom.set_transfinite_lines([lines[2], lines[3]], 9, progression=1.2)
    geom.set_transfinite_surface(surface)

    mesh = pygmsh.generate_mesh(geom, geo_filename="transfinite.geo")
    assert len(mesh.cells["triangle"]) == 10 * 8 * 2 * 2
    return mesh


if __name__ == "__main__":
    import meshio

    meshio.write("transfinite.vtu", test())
