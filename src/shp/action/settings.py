from __future__ import annotations
import bpy

from .item import SHP_PG_Action


class SHP_PG_ActionSettings(bpy.types.PropertyGroup):
    @staticmethod
    def get_instance() -> SHP_PG_ActionSettings | None:
        from ..settings import SHP_PG_GlobalSettings
        if settings := SHP_PG_GlobalSettings.get_instance():
            return settings.action

    def update_timeline(self, context: bpy.types.Context):
        if item := self.get_current_action():
            item.apply_timeline(context)

    actions: bpy.props.CollectionProperty(
        name='Action', type=SHP_PG_Action)

    current_action_index: bpy.props.IntProperty(
        name='Current Action', update=update_timeline)

    def init_actions(self, context: bpy.types.Context):
        frames = filter(
            lambda item: not item.name.endswith('_End'),
            context.scene.timeline_markers)

        self.actions.clear()
        for start in frames:
            end = context.scene.timeline_markers.get(f'{start.name}_End')
            slot: SHP_PG_Action = self.actions.add()
            slot.name = start.name
            slot.name_buf = start.name
            slot.start = start.frame
            slot.end = end.frame if end else start.frame

        return True

    def add_action(self, context: bpy.types.Context):
        self.actions.add()
        return True

    def remove_action(self, context: bpy.types.Context):
        if self.current_action_index < 0 or self.current_action_index >= len(self.actions):
            return False

        action = self.get_current_action()
        start = context.scene.timeline_markers.get(action.name)
        end = context.scene.timeline_markers.get(action.end_name)
        context.scene.timeline_markers.remove(start)
        context.scene.timeline_markers.remove(end)

        self.actions.remove(self.current_action_index)
        self.current_action_index = max(
            0, self.current_action_index - 1)

        return True

    def get_current_action(self) -> SHP_PG_Action | None:
        if self.current_action_index < 0 or self.current_action_index >= len(self.actions):
            return None

        item: SHP_PG_Action = self.actions[self.current_action_index]
        return item
