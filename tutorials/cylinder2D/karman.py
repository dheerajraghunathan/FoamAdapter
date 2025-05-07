import os

import classy_blocks as cb

cylinder_diameter = 20e-3  # [m]
ring_thickness = 5e-3  # [m]

# domain size
domain_height = 0.1  # [m] (increase for "proper" simulation)
upstream_length = 0.1  # [m]
downstream_length = 0.3  # [m]

# size to roughly match cells outside ring
cell_size = 0.3 * ring_thickness * 0.25 # [m]
print(f"cell size: {cell_size} m")
bl_thickness = 1e-4
c2c_expansion = 1.2  # cell-to-cell expansion ratio

# it's a 2-dimensional case
z = 0.01

mesh = cb.Mesh()

# a layer of cells on the cylinder
d = 2**0.5 / 2
outer_point = d * (cylinder_diameter / 2 + ring_thickness)

wall_ring = cb.ExtrudedRing(
    [0, 0, 0],
    [0, 0, z],
    [outer_point, outer_point, 0],
    cylinder_diameter / 2,
    n_segments=4,  # the default is 8 but here it makes no sense to have more than 4
)

wall_ring.chop_axial(count=1)
wall_ring.chop_tangential(start_size=cell_size)
wall_ring.chop_radial(start_size=bl_thickness, c2c_expansion=c2c_expansion)
wall_ring.set_inner_patch("cylinder")

mesh.add(wall_ring)


# boxes that fill up the whole domain
def make_box(p1, p2, size_axes, patches):
    box = cb.Box([p1[0], p1[1], 0], [p2[0], p2[1], z])

    for axis in size_axes:
        box.chop(axis, start_size=cell_size)

    for side, name in patches.items():
        box.set_patch(side, name)

    mesh.add(box)


# top 3 boxes
make_box(
    [-upstream_length, outer_point], [-outer_point, domain_height / 2], [0, 1], {"back": "upper_wall", "left": "inlet"}
)
make_box([-outer_point, outer_point], [outer_point, domain_height / 2], [], {"back": "upper_wall"})
make_box(
    [outer_point, outer_point],
    [downstream_length, domain_height / 2],
    [0, 1],
    {"back": "upper_wall", "right": "outlet"},
)

# left and right of the cylinder
make_box([-upstream_length, -outer_point], [-outer_point, outer_point], [], {"left": "inlet"})
make_box([outer_point, -outer_point], [downstream_length, outer_point], [], {"right": "outlet"})

# bottom 3 boxes
make_box(
    [-upstream_length, -domain_height / 2],
    [-outer_point, -outer_point],
    [0, 1],
    {"front": "lower_wall", "left": "inlet"},
)
make_box([-outer_point, -domain_height / 2], [outer_point, -outer_point], [], {"front": "lower_wall"})
make_box(
    [outer_point, -domain_height / 2],
    [downstream_length, -outer_point],
    [0, 1],
    {"front": "lower_wall", "right": "outlet"},
)

mesh.write(os.path.join("system", "blockMeshDict"))
