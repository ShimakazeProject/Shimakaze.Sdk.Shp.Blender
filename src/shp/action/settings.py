from __future__ import annotations
import typing
import bpy

from .item import SHP_PG_Action


class SHP_PG_ActionSettings(bpy.types.PropertyGroup):
    @staticmethod
    def get_instance() -> SHP_PG_ActionSettings | None:
        from ..settings import SHP_PG_GlobalSettings
        settings = SHP_PG_GlobalSettings.get_instance()
        if settings:
            return settings.action

    def init_actions(self, context: bpy.types.Context):
        # 明确类型
        frame_map: typing.Dict[str,  typing.Tuple[int, int]] = {}

        for marker in context.scene.timeline_markers:
            name = marker.name
            if name.endswith('_End'):
                base_name = name[:-4]
                start, end = frame_map.get(
                    base_name, (marker.frame, marker.frame))
                frame_map[base_name] = (start, marker.frame)  # 只更新 end
            else:
                base_name = name
                start, end = frame_map.get(
                    base_name, (marker.frame, marker.frame))
                frame_map[base_name] = (marker.frame, end)  # 只更新 start

        self.actions.clear()
        for item in frame_map:
            slot: SHP_PG_Action = self.actions.add()
            slot.name = item
            slot.name_buf = item
            (slot.start, slot.end) = frame_map.get(item)

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

    def update_timeline(self, context: bpy.types.Context):
        item = self.get_current_action()
        if item:
            item.update_timeline(context)

    actions: bpy.props.CollectionProperty(
        name='Action', type=SHP_PG_Action)

    current_action_index: bpy.props.IntProperty(
        name='Current Action', update=update_timeline)
