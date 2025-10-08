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

    def apply(self):
        from ..settings import SHP_PG_GlobalSettings
        settings = SHP_PG_GlobalSettings.get_instance()
        action_settings: SHP_PG_ActionSettings = self.action_name
        for item in action_settings.actions:
            item: SHP_PG_Action
            if item.name == self.action_name:
                action: SHP_PG_Action = item

        settings.use_alpha = self.use_alpha
        settings.house_mode = self.house_mode
        settings.mode = self.mode

        action.update_timeline(bpy.context)

    def clean(self):
        action: SHP_PG_Action = self.action_name
        if not action.fixed_direction:
            action.use_direction = False
            action.direction = 0
