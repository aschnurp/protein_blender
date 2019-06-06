bl_info = {
    "name": "ProteinBlender",
    "category": "Object",
}

import bpy
import datetime

class DrawSphere(bpy.types.Operator):
    """My Sphere Drawing Script"""
    bl_idname = "object.create_sphere"
    bl_label = "ProteinBlender"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        file = open("C:/Users/Seide/OneDrive/Documents/Studium/Biotechnologie Bachelor/Sommersemester 19/Problemorientierte Programmierung/PyCharm/protein_blender/test.txt", "r")
        liste = []
        count = 1

        dictionary_atom = {"C" : 1.7, "O" : 1.52, "N" : 1.55, "S" : 1.8}

        print(datetime.datetime.now())
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
                liste.append(tupel)
                print(tupel)
                count = count + 1
        print(datetime.datetime.now())
        file.close()

        for i in range(1, count - 1):
            scale = dictionary_atom.get(liste[i][0][1])
            print(scale)
            bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, size=scale, calc_uvs=False, view_align=False,
                                                 enter_editmode=False, location=(liste[i][4]),
                                                 rotation=(0.0, 0.0, 0.0))


        print(datetime.datetime.now())

        return {'FINISHED'}

###### Panel aka Menu
class ObjectSelectPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_Protein Blender"
    bl_label = "Protein Blender"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw_header(self, context):
        layout = self.layout
        obj = context.object
        layout.prop(obj, "select", text="")

    def draw(self, context):
        layout = self.layout

        obj = context.object
        row = layout.row()
        row.prop(obj, "hide_select")
        row.prop(obj, "hide_render")

        rd = context.scene.render
        layout.prop(rd, "filepath", text="PDB file")


        box = layout.box()
        box.label("Selection Tools")
        box.operator("object.select_all").action = 'TOGGLE'
        row = box.row()
        row.operator("object.select_all").action = 'INVERT'
        row.operator("object.select_random")


bpy.utils.register_class(ObjectSelectPanel)

def register():
    bpy.utils.register_class(DrawSphere)


def unregister():
    bpy.utils.unregister_class(DrawSphere)


if __name__ == "__main__":
    register()