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

def scale_uv( uv, pivot, s):
    x1,y1 = uv
    xp,yp = pivot
    x2 = xp + s * (uv.x-xp)
    y2 = yp + s * (uv.y-yp)
    return x2,y2

def scaleUVedgeToActualSize(context,scale):
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

    ua = mathutils.Vector(uvs[0])
    ub = mathutils.Vector(uvs[1])
    va = mathutils.Vector(vtx[0])
    vb = mathutils.Vector(vtx[1])
    luv = math.sqrt((ua.x-ub.x)**2 + (ua.y-ub.y)**2)
    lvt = math.sqrt((va.x-vb.x)**2 + (va.y-vb.y)**2 + (va.z-vb.z)**2)

    p = scale #1024  # [mm] on uv=1.0f

    n = 1000*lvt / (p * luv)
    print(n)

    pivot = ((ua.x+ub.x)/2, (ua.y+ub.y)/2)    # a+b/2

    bpy.ops.uv.select_linked()
    bmesh.update_edit_mesh(me) 

    for face in bm.faces:
        if face.hide == 1 or face.select == 0:
            continue                         # skip hidden/unselected face
        for loop in face.loops:
            loop_uv = loop[uv_layer]
            if loop_uv.select:
                loop_uv.uv = scale_uv( loop_uv.uv, pivot, n )
    bmesh.update_edit_mesh(me)


bl_info = {
"name": "scale_edge_to_actual",
"author": "Wernyv",
"version": (0, 1),
"blender": (2, 80, 0),
"location": "UV Editor > UV",
"description": "scale UV-island containing one selected edge to the actually size.",
"warning": "",
"support": 'TESTING',
"wiki_url": "",
"tracker_url": "",
"category": "UV"
}

class ScaleUVedgeToActualSizeWithIsland(bpy.types.Operator):
    bl_idname = "uv.scale_actual_size"
    bl_label = "scale island to actually size"
    bl_description = "scale UV-island containing one selected edge to the actually size."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scaleUVedgeToActualSize(context,self.scale)
        print(self.scale)
        return {'FINISHED'}

    # 複製したオブジェクトの拡大率
    scale: IntProperty(
        # オペレータプロパティに表示されるプロパティ名 [str]
        name="Scale",
        # プロパティの説明文 [str]
        description="Scale of the duplicated object",
        # プロパティのデフォルト値
        default=1024,
        #unit='LENGTH'
    )
"""
    scale: FloatVectorProperty(
        # オペレータプロパティに表示されるプロパティ名 [str]
        name="Scale",
        # プロパティの説明文 [str]
        description="Scale of the duplicated object",
        # プロパティのデフォルト値
        default=1024.0,
        subtype='XYZ',
        unit='LENGTH'
    )"""

classes = [
    ScaleUVedgeToActualSizeWithIsland,
    ]

def menu_func(self, context):
    self.layout.operator("uv.scale_actual_size")

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