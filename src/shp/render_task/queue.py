from __future__ import annotations
import bpy

from ..action.item import SHP_PG_Action

from .task import SHP_PG_RenderTask


class SHP_PG_RenderQueue(bpy.types.PropertyGroup):
    @staticmethod
    def get_instance() -> SHP_PG_RenderQueue | None:
        from ..settings import SHP_PG_GlobalSettings
        settings = SHP_PG_GlobalSettings.get_instance()
        if settings:
            return settings.render_queue

        return True

    render_queue: bpy.props.CollectionProperty(
        name='Render Queue', type=SHP_PG_RenderTask)
    current_render_queue_index: bpy.props.IntProperty(
        name='Current Render Task')

    def enqueue(self):
        slot: SHP_PG_RenderTask = self.render_queue.add()
        return slot.record()

    def peek(self):
        if len(self.render_queue) < 1:
            return None

        slot: SHP_PG_RenderTask = self.render_queue[0]

        return slot

    def dequeue(self):
        if len(self.render_queue) < 1:
            return
        self.render_queue.remove(0)
        self.current_render_queue_index = max(
            0, self.current_render_queue_index - 1)

    def remove(self):
        if self.current_render_queue_index < 0 or self.current_render_queue_index >= len(self.render_queue):
            return False
        self.render_queue.remove(self.current_render_queue_index)
        self.current_render_queue_index = max(
            0, self.current_render_queue_index - 1)