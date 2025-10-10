from __future__ import annotations
import bpy

from ..action import SHP_PG_ActionSettings, SHP_PG_Action


class SHP_PG_RenderTask(bpy.types.PropertyGroup):
    use_alpha: bpy.props.BoolProperty(name='Alpha')
    house_mode: bpy.props.BoolProperty(name='所属色模式')
    mode: bpy.props.EnumProperty(name='Mode', items=[
        ('Object', '对象', '渲染对象'),
        ('Shadow', '影子', '渲染影子'),
        ('Buildup', 'Buildup', 'Buildup'),
        ('Preview', 'Preview', 'Preview'),
        ('Reset', 'Reset', 'Reset'),
    ])
    action_name: bpy.props.StringProperty(name='Action')
    direction: bpy.props.IntProperty(name='物体方向')

    def record(self):
        from ..settings import SHP_PG_GlobalSettings
        settings = SHP_PG_GlobalSettings.get_instance()
        if not settings:
            return False

        action_settings: SHP_PG_ActionSettings = settings.action
        if not action_settings:
            return False

        action: SHP_PG_Action = action_settings.get_current_action()
        if not action:
            return False

        self.use_alpha = settings.use_alpha
        self.house_mode = settings.house_mode
        self.mode = settings.mode
        self.action_name = action.name
        return True

    def apply(self):
        from ..settings import SHP_PG_GlobalSettings
        settings = SHP_PG_GlobalSettings.get_instance()
        if not settings:
            return False

        action_settings: SHP_PG_ActionSettings = settings.action
        if not action_settings:
            return False

        action: SHP_PG_Action = action_settings.actions.get(self.action_name)

        settings.use_alpha = self.use_alpha
        settings.house_mode = self.house_mode
        settings.mode = self.mode

        action.apply_timeline(bpy.context)

    def clean(self):
        action: SHP_PG_Action = self.action_name
        if not action.fixed_direction:
            action.use_direction = False
            action.direction = 0
