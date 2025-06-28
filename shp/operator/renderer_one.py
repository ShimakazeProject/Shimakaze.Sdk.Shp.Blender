from typing import List, Tuple
import bpy

from .. import property

operator = None

def on_render_cancel(*args):
    global operator
    operator.cancel(bpy.context)

def on_render_complete(*args):
    global operator
    operator.busy = False

class SHP_OT_Renderer_One(bpy.types.Operator):
    bl_idname = 'shp.renderer_one'
    bl_label = '渲染当前动作'
    bl_options = {'REGISTER'}

    _timer: bpy.types.Timer = None
    busy = False
    counter = 0

    def modal(self, context, event):
        wm = context.window_manager
        if event.type == 'ESC':
            return self.cancel()
        elif not self.busy and event.type == 'TIMER':
            scene: property.SHP_PG_Scene = context.scene.shp
            if not scene.target:
                return {'CANCELLED'}

            object: property.SHP_PG_Object = scene.target.shp
            total = 3
            if self.counter >= total:
                wm.progress_end()
                object.type = 'object'
                return {'FINISHED'}

            wm.progress_update(self.counter)
            object.type = ['object', 'shadow', 'house'][self.counter]
            context.scene.render.filepath = scene.output
            self.counter += 1

            self.busy = True
            bpy.ops.render.render('INVOKE_DEFAULT', animation=True)

        return {'PASS_THROUGH'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        wm.progress_end()
        scene: property.SHP_PG_Scene = context.scene.shp
        if not scene.target:
            return {'CANCELLED'}

        object: property.SHP_PG_Object = scene.target.shp
        object.type = 'object'
        bpy.app.handlers.render_cancel.remove(on_render_cancel)
        bpy.app.handlers.render_complete.remove(on_render_complete)
        self.report({'WARNING'}, "任务已取消")
        return {'CANCELLED'}

    def finish(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        wm.progress_end()
        bpy.app.handlers.render_cancel.remove(on_render_cancel)
        bpy.app.handlers.render_complete.remove(on_render_complete)
        self.report({'INFO'}, "所有动画已渲染完成")

    def execute(self, context):
        global operator
        operator = self
        wm = context.window_manager

        self.busy = False
        bpy.app.handlers.render_cancel.append(on_render_cancel)
        bpy.app.handlers.render_complete.append(on_render_complete)
        wm.progress_begin(0, 3)
        self._timer = wm.event_timer_add(1, window=context.window)
        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}
