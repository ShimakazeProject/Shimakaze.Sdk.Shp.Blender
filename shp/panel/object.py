import bpy

from .. import property

class SHP_PL_Object(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SHP'
    bl_label = 'Shp 对象'
    bl_idname = 'SHP_PT_action'
    bl_order = 1

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
        action: property.SHP_PG_Action = object.get_active_action().shp
        
        col = layout.column(align=True)
        col.prop(object, 'target')
        col.prop(object, 'type')

        layout.template_list('SHP_UL_action_list', '', bpy.data,
                          'actions', object, 'active_action_index')

        outer_col = layout.column(align=True)
        row = outer_col.row(align=True)
        row.prop(action, 'frame_start')
        row.prop(action, 'frame_end')
        outer_col.prop(action, 'frame_count')
        
        row = outer_col.row(align=True)
        row.prop(action, 'directions')
        row.prop(action, 'direction')
        
        outer_col.prop(action, 'direction_count')
        outer_col.prop(action, 'angle_per_direction')
        row = outer_col.row(align=True).split(factor=0.9)
        row.prop(action, 'angle')
        row.label(text=action.angle_text)
        
        layout.operator('shp.keyframes_apply')

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='OBJECT_DATA', text="")