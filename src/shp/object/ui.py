from __future__ import annotations
import bpy

from .item import SHP_PG_Object

from .settings import SHP_PG_ObjectSettings
from .operators import SHP_OT_Object_Add, SHP_OT_Object_Remove


class SHP_UL_object_list(bpy.types.UIList):
    bl_idname = 'SHP_UL_object_list'
    def draw_item(self, context, layout: bpy.types.UILayout, data, item: SHP_PG_Object, icon, active_data, active_propname, index):
        obj: bpy.types.Object = item.object
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if obj:
                layout.prop(obj, 'name', text='', emboss=False,
                            icon_value=layout.icon(obj))
            else:
                layout.label(text='', translate=False,
                             icon_value=layout.icon(obj))
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text='', icon_value=layout.icon(obj))


class SHP_PT_Object(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SHP'
    bl_label = 'Shp Objects'
    bl_idname = 'SHP_PT_object'
    bl_order = 1

    def draw(self, context):
        layout = self.layout
        object_settings = SHP_PG_ObjectSettings.get_instance()
        if not object_settings:
            return

        row = layout.row(align=True)
        row.template_list(
            SHP_UL_object_list.bl_idname, '',
            object_settings, 'objects',
            object_settings, 'current_object_index')
        col = row.column(align=True)
        col.operator(SHP_OT_Object_Add.bl_idname, icon='ADD', text='')
        col.operator(SHP_OT_Object_Remove.bl_idname, icon='REMOVE', text='')

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='OBJECT_DATA', text="")
