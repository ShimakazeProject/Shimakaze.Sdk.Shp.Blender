import bpy

from .. import property

class SHP_PL_Scene(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SHP'
    bl_label = 'Shp'
    bl_idname = 'SHP_PT_shp'

    def draw(self, context):
        layout = self.layout
        scene: property.SHP_PG_Scene = context.scene.shp

        if not scene.enabled:
            row = layout.row()
            row.prop(scene, 'enabled')
            row.label(text='SHP 未启用')
            return

        layout.prop(scene, 'enabled')
        layout.prop(scene, 'target')

        col = layout.column(align=True)
        col.prop(scene, 'script_alpha')
        col.prop(scene, 'script_object')
        col.prop(scene, 'script_shadow')

        col = layout.column(align=True)
        col.prop(scene, 'output_template')
        col.prop(scene, 'output')

        col = layout.column(align=True)
        col.operator('shp.renderer_one')
        col.operator('shp.renderer_all')
