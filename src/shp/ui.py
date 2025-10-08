import bpy

from .settings import SHP_PG_GlobalSettings

class SHP_PT_GlobalSettings(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SHP'
    bl_label = 'Shp'
    bl_idname = 'SHP_PT_shp'

    def draw(self, context):
        layout = self.layout
        settings = SHP_PG_GlobalSettings.get_instance()

        if not settings:
            row = layout.row()
            row.label(text='未启用 SHP, 请检查是否使用了模板')
            return

        layout.prop(settings, 'output_template')

        col = layout.column(align=True)
        col.prop(settings, 'mode')
        row = col.row(align=True)
        row.prop(settings, 'use_alpha')
        row.prop(settings, 'house_mode')

        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(settings, 'reverse')
        row.prop(settings, 'directions')
        col.label(
            text=f"{settings.angle_per_direction}°/direction * {settings.direction_count} diretions")

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='OBJECT_DATA', text="")



