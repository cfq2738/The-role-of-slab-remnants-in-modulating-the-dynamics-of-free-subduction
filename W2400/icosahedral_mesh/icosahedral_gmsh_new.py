#!/usr/bin/env python

from optparse import OptionParser
import fluidity.diagnostics.gmshtools as gmshtools
from fluidity.diagnostics.elements import Element
from fluidity.diagnostics.meshes import Mesh
from polyhedra import icosahedron, subdivide, semi_icosahedron
import numpy

optparser=OptionParser(usage='usage: %prog <filename> <radius> <subdivisions>',
                       add_help_option=True,
                       description="""Creates an icohedral gmsh mesh of the 2-sphere in 3D.""")
optparser.add_option("--ascii", "-a",
                  help="Convert to ASCII Gmsh format",
                     action="store_const", const=True, dest="ascii", default=False)

(options, argv) = optparser.parse_args()
try:
    filename = argv[0]
    radius = float(argv[1])
    subdivisions = int(argv[2])
except:
    optparser.error("Incorrect number or value of arguments.")

nodes, faces, semi_faces = semi_icosahedron()

for i in range(subdivisions):
    subdivide(nodes, faces, semi_faces)

nodes = radius * numpy.array(nodes)
mesh = Mesh(3, nodes, volumeElements=[], surfaceElements=[Element(face) for face in faces + semi_faces])

# add edges on the cut-plane as line-elements
# note that we abuse the Mesh class here: it separates into dim volumeElements and dim-1 surfaceElements
# but gmsh doesn't make that distinction, so we just add the dim-2 line elements as surfaceElements

# boundary edges are identified as having both nodes with z=0
for face in faces:
    for i, j in [[0,1], [1,2], [2,0]]:
        if abs(nodes[face[i],1]) + abs(nodes[face[j],1]) < 1e-12:
            line_element = Element([face[i], face[j]], ids=[1], dim=1)
            # hack: we can't use AddSurfaceElement as it resets the dimension to dim-1 (i.e 2 instead of 1)
            mesh._surfaceElements.append(line_element)

# in the semi-faces we know which one is the boundary edge (between local node 0 and 1)
for face in semi_faces:
    line_element = Element([face[0], face[1]], ids=[1], dim=1)
    # hack: we can't use AddSurfaceElement as it resets the dimension to dim-1 (i.e 2 instead of 1)
    mesh._surfaceElements.append(line_element)


# now we can write the gmsh file:
gmshtools.WriteMsh(mesh, "%s.msh" % (filename), binary=not options.ascii)
