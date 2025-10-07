import bpy

from .props import SHP_PG_HideObject


class SHP_PL_WindowManager(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SHP'
    bl_label = 'Shp'
    bl_idname = 'SHP_PT_shp'

    def draw(self, context):
        layout = self.layout
        settings: SHP_PG_HideObject = context.window_manager.shp

        if not settings.enabled:
            row = layout.row()
            row.prop(settings, 'enabled')
            row.label(text='SHP 未启用')
            return

        layout.prop(settings, 'enabled')

        col = layout.column(align=True)
        col.prop(settings, 'output_template')
        col.prop(settings, 'output')

        col = layout.column(align=True)
        col.prop(settings, 'mode')
        row = col.row(align=True)
        row.prop(settings, 'use_alpha')
        row.prop(settings, 'house_mode')

        col = layout.column(align=True)
        col.prop(settings, 'reverse')
        row = col.row(align=True)
        row.prop(settings, 'directions')
        row.prop(settings, 'direction')

        col.prop(settings, 'direction_count')
        col.prop(settings, 'angle_per_direction')
        row = col.row(align=True).split(factor=0.9)
        row.prop(settings, 'angle')
        row.label(text=settings.angle_text)

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='OBJECT_DATA', text="")


class SHP_PL_Object(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SHP'
    bl_label = 'Shp 对象'
    bl_idname = 'SHP_PT_action'
    bl_order = 1

    def draw(self, context):
        layout = self.layout
        settings: SHP_PG_HideObject = context.window_manager.shp

        if not settings.enabled:
            row = layout.row()
            row.label(text='未启用 SHP, 请检查是否使用了模板')
            return
        row = layout.row(align=True)
        row.template_list(
            'SHP_UL_object_list', '',
            settings, 'objects',
            settings, 'active_object_index')
        col = row.column(align=True)
        col.operator('shp.object_add', icon='ADD', text='')
        col.operator('shp.object_remove', icon='REMOVE', text='')

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='OBJECT_DATA', text="")


class SHP_PL_Material(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SHP'
    bl_label = 'Shp 所属色材质'
    bl_idname = 'SHP_PT_material'
    bl_order = 2

    def draw(self, context):
        layout = self.layout
        settings: SHP_PG_HideObject = context.window_manager.shp

        if not settings.enabled:
            row = layout.row()
            row.label(text='未启用 SHP, 请检查是否使用了模板')
            return

        row = layout.row(align=True)
        row.template_list(
            'SHP_UL_material_list', '',
            settings, 'house_materials',
            settings, 'active_house_material_index')
        col = row.column(align=True)
        col.operator('shp.house_material_node_group_apply',
                     icon='MATERIAL_DATA',
                     text='')
        col.operator('shp.house_material_add', icon='ADD', text='')
        col.operator('shp.house_material_remove', icon='REMOVE', text='')

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='MATERIAL_DATA', text="")
