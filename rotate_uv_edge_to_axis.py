import bpy
import bmesh
import math

def rotate_uv( uv, pivot, r):
    x1,y1 = uv
    xp,yp = pivot
    x1 -= xp
    y1 -= yp
    cos_r, sin_r = math.cos(r), math.sin(r)
    x2 = x1*cos_r -y1*sin_r + xp
    y2 = x1*sin_r +y1*cos_r + yp
    return x2,y2

def adjustUVedgeToXorYaxis(context):
    obj = context.active_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    uv_layer = bm.loops.layers.uv.verify()

    selects = []
    for face in bm.faces:                    # all faces
        if face.hide == 1 or face.select == 0:
            continue                         # skip hidden/unselected face
        for loop in face.loops:              # all loops
            loop_uv = loop[uv_layer]         # current layer
            if loop_uv.select:               # collect selected
                if loop_uv.uv not in selects:  # and unique
                    selects.append(loop_uv.uv)
    if len(selects)!=2:
        print("----")
        for s in selects:
            print(s)
        return

    if selects[0][0] < selects[1][0]:  # a:left  b:right
        a = selects[0]
        b = selects[1]
    else:
        a = selects[1]
        b = selects[0]

    assert(a[0]!=b[0] and a[1]!=b[1],"aleady") # aligned axis

    t = math.atan2(b[0]-a[0], b[1]-a[1])  # t:CW from top, up(0),right(0.5pi),down(pi) 
    if math.pi*0.25 < t and t < math.pi*0.75: # near X axis
       r = (t - math.pi*0.5)
    elif t < math.pi*0.5:                     # near Y+
        r = t
    else:                                     # near Y-
        r = (t - math.pi)

    pivot = ((a[0]+b[0])/2, (a[1]+b[1])/2)    # a+b/2

#    bpy.ops.uv.select_linked_pick(extend=True, deselect=False, location=a)
#    bpy.ops.uv.select_linked_pick(extend=True, deselect=False, location=(-0.05,-0.052))
    bpy.ops.uv.select_linked()
    bmesh.update_edit_mesh(me) 

    for face in bm.faces:
        for loop in face.loops:
            loop_uv = loop[uv_layer]
            if loop_uv.select:
                loop_uv.uv = rotate_uv( loop_uv.uv, pivot, r )

    bmesh.update_edit_mesh(me)


bl_info = {
"name": "rotate_uv_edge_to_axis",
"author": "Wernyv",
"version": (0, 1),
"blender": (2, 80, 0),
"location": "UV Editor > UV",
"description": "rotate a selected uv-edge to axis with island",
"warning": "",
"support": 'TESTING',
"wiki_url": "",
"tracker_url": "",
"category": "UV"
}

class RotateUVedgeToXorYaxisWithIsland(bpy.types.Operator):
    bl_idname = "uv.edge_rotate_axis"
    bl_label = "UV island rotate to axis"
    bl_description = "rotate selected UVedge to X or Y axis with island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        adjustUVedgeToXorYaxis(context)
        return {'FINISHED'}

classes = [
    RotateUVedgeToXorYaxisWithIsland,
    ]

def menu_func(self, context):
    self.layout.operator("uv.edge_rotate_axis")

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