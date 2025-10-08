import bpy

from .queue import SHP_PG_RenderQueue


class SHP_OT_RenderQueue_Add(bpy.types.Operator):
    bl_idname = 'shp.render_queue_add'
    bl_label = '添加渲染任务'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        render_queue = SHP_PG_RenderQueue.get_instance()
        if render_queue and render_queue.enqueue():
            return {'FINISHED'}

        return {'CANCELLED'}


class SHP_OT_RenderQueue_Remove(bpy.types.Operator):
    bl_idname = 'shp.render_queue_remove'
    bl_label = '从渲染队列中移除'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        render_queue = SHP_PG_RenderQueue.get_instance()
        if render_queue and render_queue.remove():
            return {'FINISHED'}

        return {'CANCELLED'}


class SHP_OT_RenderQueue_Render(bpy.types.Operator):
    bl_idname = 'shp.render_queue_render'
    bl_label = '渲染队列'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pass
