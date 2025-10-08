from __future__ import annotations
import bpy

from .operators import SHP_OT_Action_Add, SHP_OT_Action_Init, SHP_OT_Action_Remove

from .item import SHP_PG_Action

from .settings import SHP_PG_ActionSettings


class SHP_UL_action_list(bpy.types.UIList):
    bl_idname = 'SHP_UL_action_list'

    def draw_item(self, context, layout: bpy.types.UILayout, data, item: SHP_PG_Action, icon, active_data, active_propname, index):
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if item:
                frameRange = f"{item.start}" if item.start == item.end else f"{item.start}-{item.end}"

                row = layout.row()
                row.prop(item, 'name', text='', emboss=False,
                         icon_value=layout.icon(item))
                row.label(text=frameRange, translate=False)
            else:
                layout.label(text='', translate=False,
                             icon_value=layout.icon(item))
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text='', icon_value=layout.icon(item))


class SHP_PT_Action(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SHP'
    bl_label = 'Shp Action'
    bl_idname = 'SHP_PT_action'
    bl_order = 2

    def draw(self, context):
        layout = self.layout
        action_settings = SHP_PG_ActionSettings.get_instance()
        if not action_settings:
            return

        row = layout.row(align=True)
        row.template_list(
            SHP_UL_action_list.bl_idname, '',
            action_settings, 'actions',
            action_settings, 'current_action_index')
        col = row.column(align=True)
        col.operator(SHP_OT_Action_Init.bl_idname,
                     icon='FILE_REFRESH', text='')
        col.operator(SHP_OT_Action_Add.bl_idname, icon='ADD', text='')
        col.operator(SHP_OT_Action_Remove.bl_idname, icon='REMOVE', text='')

        data = action_settings.get_current_action()
        if data:
            col = layout.column(align=True)
            row = col.row(align=True)
            row.prop(data, 'name_buf')
            row = col.row(align=True)
            row.prop(data, 'start')
            row.prop(data, 'end')

            col = layout.column(align=True)
            col.prop(data, 'fixed_direction')
            col = layout.column(align=True)
            row = col.row(align=True).split(factor=0.9)
            row.prop(data, 'direction')
            row.label(text=data.angle_text)
            col.prop(data, 'angle')

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='OBJECT_DATA', text="")
