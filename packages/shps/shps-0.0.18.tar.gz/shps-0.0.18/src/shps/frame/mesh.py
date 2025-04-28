import numpy as np


def _poly_facets(coords, offset=0):
    """Return (point_list, facet_index_pairs) for a polygon ring."""
    pts   = [tuple(p[:2]) for p in coords[:-1]]          # drop repeated last pt
    n     = len(pts)
    idx   = list(range(offset, offset + n))
    edges = [(idx[i], idx[(i + 1) % n]) for i in range(n)]
    return pts, edges

def sect2meshpy(sect, size, min_angle=25.0, **kwds):
    """
    Mesh a 2-D section with MeshPy/Triangle.

    Parameters
    ----------
    sect : Any
        Your section description; must be convertible by `sect2shapely` to a
        Shapely Polygon (possibly with holes).
    size : float | (float, …)
        Characteristic length.  MeshPy uses `max_area`, so we set
        max_area ≈ 0.5 * size^2.
    min_angle : float, optional
        Quality constraint passed to Triangle (default 25°).
    **kwds
        Additional keyword args forwarded to `tri.build()`.

    Returns
    -------
    meshio.Mesh
        2-D triangular mesh in the same form returned by `sect2dmsh` / `sect2gmsh`.
    """
    # -- Convert the section to a Shapely polygon ----------------------------
    from shapely.geometry import Polygon
    from meshpy import triangle as tri
    import meshio
    if isinstance(sect, tuple):
        shape = Polygon(*sect)
    elif not isinstance(sect, Polygon):
        shape: Polygon = sect2shapely(sect)
    else:
        shape = sect

    # -- Gather points, facets, and hole markers -----------------------------
    points, facets, holes = [], [], []

    # exterior ring
    exterior_pts, exterior_facets = _poly_facets(np.array(shape.exterior.coords))
    points.extend(exterior_pts)
    facets.extend(exterior_facets)

    # interior rings (holes)
    for ring in shape.interiors:
        ring_pts, ring_facets = _poly_facets(np.array(ring.coords), offset=len(points))
        points.extend(ring_pts)
        facets.extend(ring_facets)

        # Triangle needs *one* point inside each hole
        holes.append(ring.representative_point().coords[0][:2])

    # -- Build the mesh ------------------------------------------------------
    mesh_info = tri.MeshInfo()
    mesh_info.set_points(points)
    mesh_info.set_facets(facets)
    if holes:
        mesh_info.set_holes(holes)

    # Characteristic length -> target triangle area
    if isinstance(size, (list, tuple, np.ndarray)):
        size = float(size[0])
    max_area = 0.5 * size ** 2

    tri_mesh = tri.build(
        mesh_info,
        max_volume=max_area,
        min_angle=min_angle,
        **kwds,          # e.g. allow_boundary_steiner=False, …
    )

    # -- Convert to meshio ----------------------------------------------------
    pts = np.column_stack((np.asarray(tri_mesh.points), np.zeros(len(tri_mesh.points))))
    cells = [("triangle", np.asarray(tri_mesh.elements, dtype=int))]

    return meshio.Mesh(pts, cells)

def sect2shapely(section):
    """
    Generate `shapely` geometry objects
    from `opensees` patches or a FiberSection.
    """
    import shapely.geometry
    from shapely.ops import unary_union
    shapes = []
    if hasattr(section, "patches"):
        patches = section.patches
    elif isinstance(section, list):
        patches = section
    else:
        patches = [section]

    for patch in patches:
        name = patch.__class__.__name__.lower()
        if name in ["quad", "poly", "rect", "_polygon"]:
            points = np.array(patch.vertices)
            width,_  = points[1] - points[0]
            _,height = points[2] - points[0]
            shapes.append(shapely.geometry.Polygon(points))
        else:
            # Assuming its a circle
            n = 64 # points on circumference
            x_off, y_off = 0.0, 0.0
            external = [[
                0.5 * patch.extRad * np.cos(i*2*np.pi*1./n - np.pi/8) + x_off,
                0.5 * patch.extRad * np.sin(i*2*np.pi*1./n - np.pi/8) + y_off
                ] for i in range(n)
            ]
            if patch.intRad > 0.0:
                internal = [[
                    0.5 * patch.intRad * np.cos(i*2*np.pi*1./n - np.pi/8) + x_off,
                    0.5 * patch.intRad * np.sin(i*2*np.pi*1./n - np.pi/8) + y_off
                    ] for i in range(n)
                ]
                shapes.append(shapely.geometry.Polygon(external, [internal]))
            else:
                shapes.append(shapely.geometry.Polygon(external))

    if len(shapes) > 1:
        return unary_union(shapes)
    else:
        return shapes[0]


def sect2dmsh(sect, size, **kwds):
    import dmsh 
    if isinstance(size, (list, tuple)):
        size = size[0]

    shape = sect2shapely(sect)
    
    geo = dmsh.Polygon(shape.exterior.coords[:-1])

    for hole in shape.interiors:
        geo  = geo - dmsh.Polygon(hole.coords[:-1])

    msh = dmsh.generate(geo, size, **kwds)
    import meshio
    return meshio.Mesh(*msh)

def sect2gmsh(sect, size, **kwds):
    import pygmsh
    if isinstance(size, (int, float)):
        size = [size]*2

    shape = sect2shapely(sect)

    with pygmsh.geo.Geometry() as geom:
        geom.characteristic_length_min = size[0]
        geom.characteristic_length_max = size[1]
        coords = np.array(shape.exterior.coords)
        holes = [
            geom.add_polygon(np.array(h.coords)[:-1], size[0], make_surface=False).curve_loop
            for h in shape.interiors
        ]
        if len(holes) == 0:
            holes = None

        poly = geom.add_polygon(coords[:-1], size[1], holes=holes)
        # geom.set_recombined_surfaces([poly.surface])
        mesh = geom.generate_mesh(**kwds)

    mesh.points = mesh.points[:,:2]
    for blk in mesh.cells:
        blk.data = blk.data.astype(int)
    # for cell in mesh.cells:
    #     cell.data = np.roll(np.flip(cell.data, axis=1),3,1)
    return mesh
