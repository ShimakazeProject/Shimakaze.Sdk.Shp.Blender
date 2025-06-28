import bpy

from .. import property

class SHP_PL_Material(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SHP'
    bl_label = 'Shp 所属色材质'
    bl_idname = 'SHP_PT_material'
    bl_order = 2

    def draw(self, context):
        layout = self.layout
        scene: property.SHP_PG_Scene = context.scene.shp
        
        if not scene.enabled:
            layout.label(text='SHP 未启用')
            return
        if not scene.target:
            layout.label(text='未选择动画目标')
            return

        object: property.SHP_PG_Object = scene.target.shp

        row = layout.row(align=True)
        row.template_list(
            'SHP_UL_material_list', '',
            object, 'house_materials',
            object, 'active_house_material_index')
        col = row.column(align=True)
        col.operator('shp.house_material_node_group_apply',
                     icon='MATERIAL_DATA',
                     text='')
        col.operator('shp.house_material_add', icon='ADD', text='')
        col.operator('shp.house_material_remove', icon='REMOVE', text='')

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='MATERIAL_DATA', text="")