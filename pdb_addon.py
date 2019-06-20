bl_info = {
    "name": "ProteinBlender",
    "category": "Object",
}

import bpy
import datetime
from bpy_extras.io_utils import ImportHelper

#read file
def read_pdb_file(filename):
    file = open(filename, "r")
    pdb_list = []
    for line in file:
        if (line.startswith("ENDMDL") or line.startswith("TER")):
            break
        if line.startswith("ATOM"):
            atomname = line[12:16]
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            atom_coordinates = (atomname, x, y, z)
            pdb_list.append(atom_coordinates)
    print(datetime.datetime.now())
    file.close()
    count = len(pdb_list)
    return count, pdb_list

# create material with color
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


###### Panel aka Menu
class CreateProteinPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Protein Blender"
    bl_context = 'objectmode'
    bl_category = "Protein Blender"

    # draw the Panel
    def draw(self, context):
        layout = self.layout
        layout.operator("object.create_sphere", text="Draw Protein") # assign a function to the button
        layout.operator("object.create_backbone", text="Draw Backbone")


#####Register
# register the panel
bpy.utils.register_class(CreateProteinPanel)

def register():
    bpy.utils.register_class(DrawSphere)
    bpy.utils.register_class(DrawBackbone)

def unregister():
    bpy.utils.unregister_class(DrawSphere)
    bpy.utils.unregister_class(DrawBackbone)

if __name__ == "__main__":
    register()