bl_info = {
    "name": "ProteinBlender",
    "category": "Object",
}

import bpy
import datetime


from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

# class OT_TestOpenFilebrowser(Operator, ImportHelper):
#     bl_idname = "test.open_filebrowser"
#     bl_label = "Open the file browser (yay)"
#     def execute(self, context):
#         """Do something with the selected file(s)."""
#         return {'FINISHED'}

class DrawSphere(bpy.types.Operator, ImportHelper):
    """My Sphere Drawing Script"""
    bl_idname = "object.create_sphere"
    bl_label = "ProteinBlender"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        file = self.filepath
        list = []
        count = 1

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

        # read file
        for line in file:
            if (line.startswith("ENDMDL") or line.startswith("TER")):
                break
            if line.startswith("ATOM"):
                atomname = line[12:16]
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                atomcoordinaten = (x,y,z)
                tupel = (atomname, x,y,z , atomcoordinaten)
                list.append(tupel)
                print(tupel)
                count = count + 1
        print(datetime.datetime.now())
        #file.close()

        # create spheres with material and color
        for i in range(1, count - 1):
            scale = dictionary_atom.get(list[i][0][1])
            print(scale)
            color = dictionary_atom_color.get(list[i][0][1])
            bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, size=scale, calc_uvs=False, view_align=False,
                                                 enter_editmode=False, location=(list[i][1], list[i][2], list[i][3]), rotation=(0.0, 0.0, 0.0))

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

    #Draw the Panel
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        col.operator("object.create_sphere", text="Draw Protein") # assign a function to the button

        # col.operator("test.open_filebrowser", text="filebrowser")  # assign a function to the button








# class AddCube(bpy.types.Operator):
#     bl_idname = "mesh.add_cube"
#     bl_label = "Add Cube"
#     bl_options = {'REGISTER', 'UNDO'}
#     def execute(self, context):
#         bpy.ops.mesh.primitive_cube_add()





############################################################
#Baustelle#
############################################################

#### neuer Header ####

# class AddCubePanel(bpy.types.Panel):
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'TOOLS'
#     bl_label = "Add Cube"
#     bl_context = 'objectmode'
#     bl_category = "Protein Blender"
#
#     def draw(self, context):
#         layout = self.layout
#         col = layout.column(align=True)
#         col.operator("mesh.primitive_cube_add", text="Add Cube")  # assign a function to the button




#####Register
# register the panel
bpy.utils.register_class(CreateProteinPanel)

def register():
    bpy.utils.register_class(DrawSphere)
    #bpy.utils.register_class(OT_TestOpenFilebrowser)


def unregister():
    bpy.utils.unregister_class(DrawSphere)
    #bpy.utils.unregister_class(OT_TestOpenFilebrowser)


if __name__ == "__main__":
    register()