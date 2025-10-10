from __future__ import annotations
import bpy

from .operators import SHP_OT_RenderQueue_Add, SHP_OT_RenderQueue_Remove, SHP_OT_RenderQueue_Render

from .task import SHP_PG_RenderTask

from .queue import SHP_PG_RenderQueue


class SHP_UL_render_list(bpy.types.UIList):
    bl_idname = 'SHP_UL_render_list'

    def draw_item(self, context, layout: bpy.types.UILayout, data, item: SHP_PG_RenderTask, icon, active_data, active_propname, index):
        if self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text=item.name, icon_value=layout.icon(item))
            return

        layout.label(text=item.name,
                     icon_value=layout.icon(item))


class SHP_PT_RenderQueue(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SHP'
    bl_label = 'Shp 渲染器队列'
    bl_idname = 'SHP_PT_render_queue'
    bl_order = 4

    def draw(self, context):
        layout = self.layout
        render_queue = SHP_PG_RenderQueue.get_instance()
        if not render_queue:
            return

        row = layout.row(align=True)
        row.template_list(
            SHP_UL_render_list.bl_idname, '',
            render_queue, 'render_queue',
            render_queue, 'current_render_queue_index')
        col = row.column(align=True)
        col.operator(SHP_OT_RenderQueue_Add.bl_idname, icon='ADD', text='')
        col.operator(SHP_OT_RenderQueue_Remove.bl_idname,
                     icon='REMOVE', text='')

        col = layout.column(align=True)
        col.operator(SHP_OT_RenderQueue_Render.bl_idname,
                     icon='RENDER_ANIMATION')

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='MATERIAL_DATA', text="")
