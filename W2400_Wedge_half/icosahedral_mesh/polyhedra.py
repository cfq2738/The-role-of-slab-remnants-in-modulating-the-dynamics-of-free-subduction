from numpy import array
from numpy.linalg import norm
from math import sqrt

# 8-3-2017 s.kramer@imperial.ac.uk:
# the icosahedron() code is partly based on http://blog.andreaskahler.com/2009/06/creating-icosphere-mesh-in-code.html
# the subdivide() routine is based on http://prideout.net/blog/?p=44 , but completely rewritten to actually produce a valid mesh
# with unique vertices and not depend on euclid

def icosahedron():
    """Construct a 20-sided polyhedron"""
    t = (1.0 + sqrt(5.0)) / 2.0;
    verts = [(-1,  t,  0),
             ( 1,  t,  0),
             (-1, -t,  0),
             ( 1, -t,  0),

             ( 0, -1,  t),
             ( 0,  1,  t),
             ( 0, -1, -t),
             ( 0,  1, -t),

             ( t,  0, -1),
             ( t,  0,  1),
             (-t,  0, -1),
             (-t,  0,  1)]
    # now normalize them:
    s = sqrt(1 + t**2)
    verts = [tuple(x/s for x in vertex) for vertex in verts]

    faces = [(0, 11, 5),
             (0, 5, 1),
             (0, 1, 7),
             (0, 7, 10),
             (0, 10, 11),
             (1, 5, 9),
             (5, 11, 4),
             (11, 10, 2),
             (10, 7, 6),
             (7, 1, 8),
             (3, 9, 4),
             (3, 4, 2),
             (3, 2, 6),
             (3, 6, 8),
             (3, 8, 9),
             (4, 9, 5),
             (2, 4, 11),
             (6, 2, 10),
             (8, 6, 7),
             (9, 8, 1)]
    return verts, faces


def semi_icosahedron():
    """Construct a 20-sided polyhedron cut in half leaving only the 'Northern' hemi-sphere"""

    # the verts in the full icosahedron are the 3x4 corners of 3 rectangles
    # (see http://blog.andreaskahler.com/2009/06/creating-icosphere-mesh-in-code.html)
    # the first rectangle is in the z=0 plane, is cut in half: we only keep the 2 top corners 
    # the second rectangle, in the x=0 plane, is cut in half as well: we keep the top 2 corners
    # the third rectangle, in the y=0 plane, which will be our cut-plane, and we keep all its 4 vertices
    # and add two new vertices in the y=0 plane
    t = (1.0 + sqrt(5.0)) / 2.0;
    verts = [(-1,  t,  0),
             ( 1,  t,  0),

             ( 0,  1,  t),
             ( 0,  1, -t),

             ( t,  0, -1),
             ( t,  0,  1),
             (-t,  0, -1),
             (-t,  0,  1),

             ( 0,  0,  t),
             ( 0,  0, -t)]
    # now normalize them (note that the two new vertices are separate)
    s = sqrt(1 + t**2)
    verts[0:8] = [tuple(x/s for x in vertex) for vertex in verts[0:8]]
    verts[8:] = [tuple(x/t for x in vertex) for vertex in verts[8:]]

    # these are the uncut faces that are also in the orig. icosahedron
    faces = [(0, 7, 2),
             (0, 6, 7),
             (3, 6, 0),
             (3, 0, 1),
             (4, 3, 1),
             (4, 1, 5),
             (1, 2, 5),
             (1, 0, 2)]

    # the cut faces. we follow a strict ordering of the nodes here
    # local node 0: node on the cut-plane that is opposite the edge that has been cut-in half
    # local node 1: node on the cut-plane that is one end of the cut-in half edge
    # local node 2: node not on the cut-plane that is the other end
    semi_faces = [(7, 8, 2),
                  (6, 9, 3),
                  (4, 9, 3),
                  (5, 8, 2)]
    return verts, faces, semi_faces


def create_new_node(face, i, j, verts, new_nodes):
    a, b = face[i], face[j]
    if (a,b) in new_nodes:
        c = new_nodes[(a,b)]
    elif (b,a) in new_nodes:
        c = new_nodes[(b,a)]
    else:
        s = array(verts[a]) + array(verts[b])
        verts.append(s/norm(s))
        c = len(verts)-1
        new_nodes[(a,b)] = c
    return c


def subdivide(verts, faces, semi_faces):

    """Subdivide each triangle into four triangles, pushing verts to the unit sphere"""


    # map between pairs of existing verts (indices) and the new node (number) created inbetween
    new_nodes = {}

    # we instantiate the enumerated list first, as we only want to loop over already existing faces
    for fi, face in list(enumerate(faces)):

        # Create three new verts at the midpoints of each edge:
        i = create_new_node(face, 0, 1, verts, new_nodes)
        j = create_new_node(face, 1, 2, verts, new_nodes)
        k = create_new_node(face, 0, 2, verts, new_nodes)

        # Split the current triangle into four smaller triangles:
        faces.append((i, j, k))
        faces.append((face[0], i, k))
        faces.append((i, face[1], j))
        faces[fi] = (k, j, face[2])

    # same for semi-faces
    for fi, face in list(enumerate(semi_faces)):
        # we cut the two edges that are not cut already by the half plane z=0
        i = create_new_node(face, 0, 1, verts, new_nodes)
        k = create_new_node(face, 0, 2, verts, new_nodes)

        # the first face is entirely away from the z=0 plane and added as a "full" face
        faces.append((face[1], face[2], k))
        # the new edge opposite the edge that is considered cut-in half by z=0 will also
        # be considered as a cut-in half edge, so the 2 faces that share it are stored
        # as semi_faces (the first overwriting the current, the second added)
        # note that we need to follow the same local node ordering as described in semi_icosahedron()
        semi_faces[fi] = (face[0], i, k)
        semi_faces.append((face[1], i, k))
