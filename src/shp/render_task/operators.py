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

    # 类变量，防止重复运行
    _is_running = False
    _should_remove = False

    @classmethod
    def poll(self, context):
        return not self._is_running  # 防止重复运行

    def execute(self, context):
        if self._is_running:
            return {'CANCELLED'}

        self._is_running = True

        # 注册 handlers（只加一次）
        if self.on_render_complete not in bpy.app.handlers.render_complete:
            bpy.app.handlers.render_complete.append(self.on_render_complete)
        if self.on_render_cancel not in bpy.app.handlers.render_cancel:
            bpy.app.handlers.render_cancel.append(self.on_render_cancel)

        self.on_render_complete()

        return {'FINISHED'}

    def on_render_cancel(self, *args):
        """渲染被用户取消时"""
        self._cleanup_handlers()
        self._is_running = False

    def on_render_complete(self, *args):
        """渲染完成时"""
        if not self._is_running:
            return

        render_queue = SHP_PG_RenderQueue.get_instance()

        if self._should_remove:
            render_queue.dequeue()
            self._should_remove = False
        if item := render_queue.peek():
            self._should_remove = True
            try:
                item.apply()
                bpy.ops.render.render('INVOKE_DEFAULT', animation=True)
            except Exception as e:
                self.report({'ERROR'}, f"应用队列项失败: {e}")
                # 继续处理下一个
                self.on_render_complete()
        else:
            self._cleanup_handlers()
            self._is_running = False

    def _cleanup_handlers(self):
        """安全移除 handlers"""
        if self.on_render_complete in bpy.app.handlers.render_complete:
            bpy.app.handlers.render_complete.remove(self.on_render_complete)
        if self.on_render_cancel in bpy.app.handlers.render_cancel:
            bpy.app.handlers.render_cancel.remove(self.on_render_cancel)

    def cancel(self, context):
        """用户中断操作（如按 ESC）"""
        self._cleanup_handlers()
        self._is_running = False
        self.report({'INFO'}, "渲染队列已取消")
