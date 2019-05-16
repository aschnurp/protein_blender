#cerate icosphere
import bpy
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, size=1.0, calc_uvs=False, view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0))


#cerate uv sphere
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, size=1.0, calc_uvs=False, view_align=False, enter_editmode=False, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0))

