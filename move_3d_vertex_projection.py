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

def project3DvertexToFace(context,direction):
    print(direction)
    obj = context.active_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bm.verts.ensure_lookup_table()

    # find last-3 selected verts(index)
    target_v = [] # ordered & selected vertices
    bm.verts.ensure_lookup_table()
    for e in bm.select_history:
        if isinstance(e, bmesh.types.BMVert) and e.select:
            target_v.append(e.index)
    if len(target_v) < 3:
        return False
    target_v = target_v[-3:]
    print(len(target_v))
 
    # find project verts without target_v(index)
    project_v = []
    for v in bm.verts:
        if v.select and v.index not in target_v:
            project_v.append(v.index)
    print(len(project_v))

    # calc face
    p0 = bm.verts[target_v[1]].co   # mathutils.Vector
    va = (p0 - bm.verts[target_v[0]].co).normalized()
    vb = (p0 - bm.verts[target_v[2]].co).normalized()
    vn = va.cross(vb)  # cross product (normal vector)
    print(str(vn))

    # ax + by + cz + d = 0
    d = -(vn.x*p0.x + vn.y*p0.y + vn.z*p0.z)

    if direction == "Z":
        # project Z axis  z = -(ax + by + d)/c
        for v in project_v:
            pn = bm.verts[v].co
            pn.z = -(vn.x*pn.x + vn.y*pn.y + d) / vn.z
    elif direction == "X":
         # project x axis  z = -(by + cz + d)/a
        for v in project_v:
            pn = bm.verts[v].co
            pn.x = -(vn.y*pn.y + vn.z*pn.z + d) / vn.x
    elif direction == "Y":
         # project x axis  z = -(ax + cz + d)/b
        for v in project_v:
            pn = bm.verts[v].co
            pn.y = -(vn.x*pn.x + vn.z*pn.z + d) / vn.y
    elif direction == "Normal":
        # project Normal  pn = pn + t*normal
        for v in project_v:
            pn = bm.verts[v].co
            # p = pn + t*vn
            # a(pn.x + t*vn.x) + b(pn.y + t*vn.y) + c(pn.z + t*vn.z) + d
            # a*pn.x + b*pn.y + c*pn.z + d + t(a*vn.x + b*vn.y + c*vn.z)
            # t = -(a*pn.x + b*pn.y + c*pn.z + d)/(a*vn.x + b*vn.y + c*vn.z)
            t = -(vn.x*pn.x + vn.y*pn.y + vn.z*pn.z + d)/(vn.x*vn.x + vn.y*vn.y + vn.z*vn.z)
            #pn = pn + t*vn
            pn.x = pn.x + t*vn.x
            pn.y = pn.y + t*vn.y
            pn.z = pn.z + t*vn.z

    bmesh.update_edit_mesh(me)
    return True


bl_info = {
"name": "project_vertex_to_face",
"author": "Wernyv",
"version": (0, 1),
"blender": (2, 80, 0),
"location": "View3D > Object",
"description": "move one of the two selected UV-vertices to the other",
"warning": "",
"support": 'TESTING',
"wiki_url": "",
"tracker_url": "",
"category": "Mesh"
}

class ProjectVertexToFace(bpy.types.Operator):
    bl_idname = "3d.project_vertex_to_face"
    bl_label = "project vertex to face"
    bl_description = "move one of the two selected UV-vertices to the other"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_obj = context.active_object
        pre_mode = active_obj.mode
        bpy.ops.object.mode_set(mode='EDIT')

        stat = project3DvertexToFace(context,self.direction)

        bpy.ops.object.mode_set(mode=pre_mode)
        if stat==False:
            self.report(type={'ERROR'}, message="Need to select at least one vertex")
            return {'CANCELLED'}
        else:
            return {'FINISHED'}

    direction_list = [
        ('X',      "X axis",  "5"),
        ('Y',      "Y axis",  "6"),
        ('Z',      "Z axis",  "7"),
        ('Normal', "Normal",  "8"),
    ]
    direction: EnumProperty(
        # オペレータプロパティに表示されるプロパティ名 [str]
        name="Project along",
        # プロパティの説明文 [str]
        description="Project Direction",
        # プロパティのデフォルト値
        items=direction_list,
        default='Normal',
    )

classes = [
    ProjectVertexToFace,
    ]

def menu_func(self, context):
    self.layout.operator("3d.project_vertex_to_face")

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    #bpy.types.IMAGE_MT_uvs.append(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(menu_func)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    #bpy.types.IMAGE_MT_uvs.remove(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(menu_func)


#if __name__ == "__main__":
#    register()