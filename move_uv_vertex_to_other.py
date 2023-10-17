import bpy
import bmesh
import math
import mathutils
from bpy.props import (
    IntProperty,
    EnumProperty,
    BoolProperty,
    FloatProperty,
    FloatVectorProperty,
)

def moveUVvertexToOther(context,direction):
    obj = context.active_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    uv_layer = bm.loops.layers.uv.verify()

    uvs = []
    vtx = []
    for face in bm.faces:                    # all faces
        if face.hide == 1 or face.select == 0:
            continue                         # skip hidden/unselected face
        for loop in face.loops:              # all loops
            loop_uv = loop[uv_layer]         # current layer
            if loop_uv.select:               # collect selected
                if loop_uv.uv not in uvs:  # and unique
                    uvs.append(loop_uv.uv)
                    vtx.append(loop.vert.co)
    if len(uvs)!=2:
        for s in uvs:
            print(s)
        return
    print("---=")
    print(uvs[0])
    print(uvs[1])
    print(direction)

    ua = mathutils.Vector(uvs[0])
    ub = mathutils.Vector(uvs[1])
    va = mathutils.Vector(vtx[0])
    vb = mathutils.Vector(vtx[1])

    pivot = uvs[1]
    if direction == 'LEFT':  #pivot=left
        if ua < ub:
            pivot = uvs[0]
    if direction == 'RIGHT':
        if ua > ub:
            pivot = uvs[0]
    if direction == 'ABOVE':
        if va > vb:
            pivot = uvs[0]
    if direction == 'BELOW':
        if va < vb:
            pivot = uvs[0]

    bmesh.update_edit_mesh(me) 

    for face in bm.faces:
        if face.hide == 1 or face.select == 0:
            continue                         # skip hidden/unselected face
        for loop in face.loops:
            loop_uv = loop[uv_layer]
            if loop_uv.select:
                if loop_uv.uv != pivot:
                    loop_uv.uv = pivot
                else:
                    loop_uv.select = False

    bmesh.update_edit_mesh(me)


bl_info = {
"name": "move_vertex_to_other",
"author": "Wernyv",
"version": (0, 1),
"blender": (2, 80, 0),
"location": "UV Editor > UV",
"description": "move one of the two selected UV-vertices to the other",
"warning": "",
"support": 'TESTING',
"wiki_url": "",
"tracker_url": "",
"category": "UV"
}

class MoveSelectedUVToOterOne(bpy.types.Operator):
    bl_idname = "uv.move_vertex_to_other"
    bl_label = "move vertex to other"
    bl_description = "move one of the two selected UV-vertices to the other"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        moveUVvertexToOther(context,self.direction)
        return {'FINISHED'}

    direction_list = [
        ('LEFT', "Left", "5"),
        ('RIGHT', "Right", "6"),
        ('ABOVE', "Above", "7"),
        ('BELOW', "Below", "8"),
    ]
    direction: EnumProperty(
        # オペレータプロパティに表示されるプロパティ名 [str]
        name="Move to",
        # プロパティの説明文 [str]
        description="Move Direction",
        # プロパティのデフォルト値
        items=direction_list,
        default='LEFT',
    )

classes = [
    MoveSelectedUVToOterOne,
    ]

def menu_func(self, context):
    self.layout.operator("uv.move_vertex_to_other")

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.IMAGE_MT_uvs.append(menu_func)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.IMAGE_MT_uvs.remove(menu_func)

#if __name__ == "__main__":
#    register()