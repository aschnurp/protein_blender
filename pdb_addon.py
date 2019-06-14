bl_info = {
    "name": "ProteinBlender",
    "category": "Object",
}

import bpy
import datetime

class DrawSphere(bpy.types.Operator):
    bl_idname = "object.create_sphere"
    bl_label = "ProteinBlender"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        filename = "C:/Users/Seide/OneDrive/Documents/Studium/Biotechnologie Bachelor/Sommersemester 19/Problemorientierte Programmierung/PyCharm/protein_blender/test.txt"

        # create material with color
        mat1 = bpy.data.materials.new("Diffuse BSDF")
        mat1.diffuse_color = (float(0.0), 0.0, 0.0) # black
        mat2 = bpy.data.materials.new("Diffuse BSDF")
        mat2.diffuse_color = (float(1.0), 0.0, 0.0) # red
        mat3 = bpy.data.materials.new("Diffuse BSDF")
        mat3.diffuse_color = (float(0.1), 0.5, 0.8) # blue
        mat4 = bpy.data.materials.new("Diffuse BSDF")
        mat4.diffuse_color = (float(0.9), 1.0, 0.0) # yellow

        # create dictionary with atom names and scales
        # dictionary_atom = {"C" : (1.7, mat1), "O" : (1.52, mat2), "N" : (1.55, mat3),"S" : (1.8, mat4)}
        dictionary_atom = {"C": 1.7, "O": 1.52, "N": 1.55, "S": 1.8}
        dictionary_atom_color = {"C": mat1, "O": mat2, "N": mat3, "S": mat4}

        print(datetime.datetime.now())

        count, pdb_list = read_pdb_file(filename)

        # create spheres with material and color
        for i in range(0, count):
            scale = dictionary_atom.get(pdb_list[i][0][1])
            color = dictionary_atom_color.get(pdb_list[i][0][1])
            bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, size=scale, calc_uvs=False, view_align=False,
                                                 enter_editmode=False, location=(pdb_list[i][1], pdb_list[i][2], pdb_list[i][3]), rotation=(0.0, 0.0, 0.0))

            object = bpy.context.selected_objects[0]
            object.active_material = color

            for poly in bpy.context.object.data.polygons:
                poly.use_smooth = True

        print(datetime.datetime.now())
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


#####Register
# register the panel
bpy.utils.register_class(CreateProteinPanel)

def register():
    bpy.utils.register_class(DrawSphere)

def unregister():
    bpy.utils.unregister_class(DrawSphere)

def read_pdb_file(filename):
    # read file
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
            atomcoordinaten = (x, y, z)
            tupel = (atomname, x, y, z, atomcoordinaten)
            pdb_list.append(tupel)
    print(datetime.datetime.now())
    file.close()
    count = len(pdb_list)
    return count, pdb_list

if __name__ == "__main__":
    register()