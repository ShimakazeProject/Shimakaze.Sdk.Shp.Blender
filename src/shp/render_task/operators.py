import time
import bpy

from .queue import SHP_PG_RenderQueue


class SHP_OT_RenderQueue_Add(bpy.types.Operator):
    bl_idname = 'shp.render_queue_add'
    bl_label = '添加渲染任务'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        render_queue = SHP_PG_RenderQueue.get_instance()
        if not render_queue or not render_queue.enqueue():
            return {'CANCELLED'}

        return {'FINISHED'}


class SHP_OT_RenderQueue_Remove(bpy.types.Operator):
    bl_idname = 'shp.render_queue_remove'
    bl_label = '从渲染队列中移除'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        render_queue = SHP_PG_RenderQueue.get_instance()
        if not render_queue or not render_queue.remove():
            return {'CANCELLED'}

        return {'FINISHED'}


class SHP_OT_RenderQueue_Render(bpy.types.Operator):
    bl_idname = 'shp.render_queue_render'
    bl_label = '渲染队列'
    bl_options = {'REGISTER', 'UNDO'}

    __timer: bpy.types.Timer
    __lock = False
    __latest_name = ''
    __max_direction = 0
    __current_direction = 0

    def execute(self, context):
        from .. import SHP_PG_GlobalSettings

        bpy.app.handlers.render_complete.append(self.on_render_complete)
        bpy.app.handlers.render_cancel.append(self.on_render_cancel)
        self.__timer = context.window_manager.event_timer_add(
            1, window=context.window)

        settings = SHP_PG_GlobalSettings.get_instance()
        self.__latest_name = ''
        self.__max_direction = settings.direction_count
        self.__current_direction = 0

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        """处理渲染队列"""
        if event.type == 'TIMER':
            if self.__render_next():
                return {'RUNNING_MODAL'}
            else:
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def __cleanup_handlers(self):
        """安全移除 handlers"""
        bpy.context.window_manager.event_timer_remove(self.__timer)
        bpy.app.handlers.render_complete.remove(self.on_render_complete)
        bpy.app.handlers.render_cancel.remove(self.on_render_cancel)

    def __render_next(self):
        """处理下一个任务"""
        if self.__lock:
            return True

        self.__lock = True

        try:
            render_queue = SHP_PG_RenderQueue.get_instance()
            # 获取当前任务
            item = render_queue.peek()
            if self.__latest_name == item.name and self.__current_direction >= self.__max_direction:
                # 申领新任务
                item.clean()
                render_queue.dequeue()
                item = render_queue.peek()
                self.__current_direction

            if not item:
                # 队列为空，结束
                self.__cleanup_handlers()
                return False

            action = item.get_action()
            self.__latest_name = item.name
            item.apply(self.__current_direction)
            self.__current_direction += self.__max_direction if action.fixed_direction else 1

            bpy.ops.render.render('INVOKE_DEFAULT', animation=True)
        except Exception as e:
            self.__lock = False
            self.report({'ERROR'}, f"应用队列项失败: {e}")

        return True

    def on_render_cancel(self, *args):
        """渲染被用户取消时"""
        self.__cleanup_handlers()
        self.report({'INFO'}, "渲染队列已取消")

    def on_render_complete(self, *args):
        """渲染完成时"""
        time.sleep(1)
        self.__lock = False

    def cancel(self, context):
        """用户中断操作（如按 ESC）"""
        self.__cleanup_handlers()
        self.report({'INFO'}, "渲染队列已取消")
