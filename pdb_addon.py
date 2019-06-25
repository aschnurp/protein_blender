bl_info = {
    "name": "ProteinBlender",
    "category": "Object",
}

import bpy
import datetime
from bpy_extras.io_utils import ImportHelper
from math import sqrt, acos, atan2

#read file
def read_pdb_file(filename):
    file = open(filename, "r")
    pdb_list_coordinates = []
    pdb_list = []
    x_list, y_list, z_list = [], [], []
    for line in file:
        if (line.startswith("ENDMDL") or line.startswith("TER")):
            break
        if line.startswith("ATOM"):
            atomname = line[12:16]
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            x_list.append(x)
            y_list.append(y)
            z_list.append(z)
            atom_coordinates = (atomname, x, y, z)
            pdb_list_coordinates.append(atom_coordinates)
    count = len(pdb_list_coordinates)
    Cx = 1 / count * sum(x_list)
    Cy = 1 / count * sum(y_list)
    Cz = 1 / count * sum(z_list)
    for i in range(0,count):
        x0 = x_list[i] - Cx
        y0 = y_list[i] - Cy
        z0 = z_list[i] - Cz
        atomname = pdb_list_coordinates[i][0]
        centroid_coordinates = (atomname, x0, y0, z0)
        pdb_list.append(centroid_coordinates)
    print(datetime.datetime.now())
    file.close()
    return count, pdb_list

# create a material with a color
def material_colors():
    mat1 = bpy.data.materials.new("Diffuse BSDF")
    mat1.diffuse_color = (float(0.0), 0.0, 0.0)  # black
    mat2 = bpy.data.materials.new("Diffuse BSDF")
    mat2.diffuse_color = (float(1.0), 0.0, 0.0)  # red
    mat3 = bpy.data.materials.new("Diffuse BSDF")
    mat3.diffuse_color = (float(0.1), 0.5, 0.8)  # blue
    mat4 = bpy.data.materials.new("Diffuse BSDF")
    mat4.diffuse_color = (float(0.9), 1.0, 0.0)  # yellow
    dictionary_atom_color = {"C": mat1, "O": mat2, "N": mat3, "S": mat4}
    return mat1, mat2, mat3, mat4, dictionary_atom_color

# create scale dictionary with Van-der-Waals radius
def atom_scales():
    dictionary_atom = {"C": 1.7, "O": 1.52, "N": 1.55, "S": 1.8}
    return dictionary_atom

# adds a class to draw the whole protein
class DrawSphere(bpy.types.Operator, ImportHelper):
    bl_idname = "object.create_sphere"
    bl_label = "load pdb file"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mat1, mat2, mat3, mat4, dictionary_atom_color = material_colors()
        dictionary_atom_scales = atom_scales()
        count, pdb_list = read_pdb_file(self.filepath)

        print(datetime.datetime.now())

        # create spheres with material and color
        for atom in range(0, count):
            scale = dictionary_atom_scales.get(pdb_list[atom][0][1])
            color = dictionary_atom_color.get(pdb_list[atom][0][1])
            bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, size=scale,
                                                 location=(pdb_list[atom][1], pdb_list[atom][2], pdb_list[atom][3]))

            object = bpy.context.selected_objects[0]
            object.active_material = color

            for poly in bpy.context.object.data.polygons:
                poly.use_smooth = True

        print(datetime.datetime.now())
        return {'FINISHED'}

# adds a class to draw the backbone only with atoms
class DrawBackbone(bpy.types.Operator, ImportHelper):
    bl_idname = "object.create_backbone"
    bl_label = "load pdb file"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        mat1, mat2, mat3, mat4, dictionary_atom_color = material_colors()
        dictionary_atom_scales = atom_scales()

        count, pdb_list = read_pdb_file(self.filepath)

        for atom in range(0,count):
            scale = dictionary_atom_scales.get(pdb_list[atom][0][1])
            color = dictionary_atom_color.get(pdb_list[atom][0][1])
            if pdb_list[atom][0] == " CA " or pdb_list[atom][0] == " N  " or pdb_list[atom][0] == " C  ":
                print(pdb_list[atom][0])
                bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, size=scale,
                                                     location=(pdb_list[atom][1], pdb_list[atom][2], pdb_list[atom][3]))
                object = bpy.context.selected_objects[0]
                object.active_material = color
            else:
                pass
        return {'FINISHED'}

# adds a class to draw the backbone with bonds and atoms
class DrawCylinder(bpy.types.Operator, ImportHelper):
    bl_idname = "object.create_cylinder"
    bl_label = "load pdb file"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self,context):
        mat1, mat2, mat3, mat4, dictionary_atom_color = material_colors()
        mat5 = bpy.data.materials.new("Diffuse BSDF")
        mat5.diffuse_color = (float(0.7), 0.7, 0.7)  # white

        # creates a list of all backbone atoms
        count, pdb_list = read_pdb_file(self.filepath)
        backbone_list = []
        for atom in range(0, len(pdb_list)):
            if pdb_list[atom][0] == " CA " or pdb_list[atom][0] == " N  " or pdb_list[atom][0] == " C  ":
                print(pdb_list[atom][0])
                atomname = pdb_list[atom][0]
                x = pdb_list[atom][1]
                y = pdb_list[atom][2]
                z = pdb_list[atom][3]
                coordinates = (atomname, x, y, z)
                backbone_list.append(coordinates)
            else:
                pass
        # use this list to draw spheres (atoms) and cylinder (bonds)
        for i in range(0, len(backbone_list)):
            color = dictionary_atom_color.get(backbone_list[i][0][1])
            bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, size=0.5, location=(backbone_list[i][1], backbone_list[i][2], backbone_list[i][3]))
            object = bpy.context.selected_objects[0]
            object.active_material = color

            if 0 < i < len(backbone_list):
                dx = backbone_list[i - 1][1] - backbone_list[i][1]
                dy = backbone_list[i - 1][2] - backbone_list[i][2]
                dz = backbone_list[i - 1][3] - backbone_list[i][3]
                dist = sqrt(dx ** 2 + dy ** 2 + dz ** 2)

                phi = atan2(dy, dx)
                theta = acos(dz / dist)
                x = dx / 2 + backbone_list[i][1]
                y = dy / 2 + backbone_list[i][2]
                z = dz / 2 + backbone_list[i][3]
                print(x, y, z)

                # add cylinders to display the "bonds"
                bpy.ops.mesh.primitive_cylinder_add(radius=0.2, location=(x, y, z), depth=dist)

                bpy.context.object.rotation_euler[1] = theta
                bpy.context.object.rotation_euler[2] = phi

                object = bpy.context.selected_objects[0]
                object.active_material = mat5
            else:
                pass
        return {'FINISHED'}

# Panel aka Menu
class CreateProteinPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Protein Blender"
    bl_context = 'objectmode'
    bl_category = "Protein Blender"

    # draw the panel and the buttons
    def draw(self, context):
        layout = self.layout
        layout.operator("object.create_sphere", text="Draw Protein")
        layout.operator("object.create_backbone", text="Draw Backbone")
        layout.operator("object.create_cylinder", text="Draw Backbone with Bonds")


# Register
# register the panel
bpy.utils.register_class(CreateProteinPanel)

# register the functions
def register():
    bpy.utils.register_class(DrawSphere)
    bpy.utils.register_class(DrawBackbone)
    bpy.utils.register_class(DrawCylinder)

def unregister():
    bpy.utils.unregister_class(DrawSphere)
    bpy.utils.unregister_class(DrawBackbone)
    bpy.utils.unregister_class(DrawCylinder)

if __name__ == "__main__":
    register()