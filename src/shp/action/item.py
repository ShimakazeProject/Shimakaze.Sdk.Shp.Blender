from __future__ import annotations
import math
import bpy


class SHP_PG_Action(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name='Name')

    @staticmethod
    def update_marker_name(context: bpy.types.Context, name: str, new_name: str | None = None, frame: int | None = None):
        marker = context.scene.timeline_markers.get(name)
        if not marker:
            marker = context.scene.timeline_markers.new(name)

        if new_name:
            marker.name = new_name
        if frame:
            marker.frame = frame

    def update_name(self, context: bpy.types.Context):
        old_name = self.name
        new_name = self.name_buf

        SHP_PG_Action.update_marker_name(
            context, old_name,
            new_name=new_name,
            frame=self.start)
        if self.start is not self.end:
            SHP_PG_Action.update_marker_name(
                context, f"{old_name}_End",
                new_name=f"{new_name}_End",
                frame=self.end)

        self.name = new_name

    def update_start(self, context: bpy.types.Context):
        SHP_PG_Action.update_marker_name(
            context, self.name,
            frame=self.start)

    def update_end(self, context: bpy.types.Context):
        SHP_PG_Action.update_marker_name(
            context, self.end_name,
            frame=self.end)

    def get_angle(self):
        from ..settings import SHP_PG_GlobalSettings
        settings = SHP_PG_GlobalSettings.get_instance()
        if settings.direction_count == 1:
            return settings.angle

        return self.direction * settings.angle_per_direction

    def get_angle_text(self):
        from ..settings import SHP_PG_GlobalSettings
        settings = SHP_PG_GlobalSettings.get_instance()
        if settings.direction_count == 1:
            return settings.angle_text

        return SHP_PG_GlobalSettings.calc_angle_text(
            settings.direction_count,
            self.direction,
            settings.reverse,
        )

    def update_direction(self, context: bpy.types.Context):
        from ..object import SHP_PG_ObjectSettings, SHP_PG_Object
        from ..settings import SHP_PG_GlobalSettings
        settings = SHP_PG_GlobalSettings.get_instance()
        object_settings: SHP_PG_ObjectSettings = settings.object
        settings.update_output(context)

        radians = 0
        if settings.direction_count == 1 or self.fixed_direction or self.use_direction:
            radians = math.radians(self.angle + 225)

        for item in object_settings.objects:
            item: SHP_PG_Object
            item.object.rotation_euler[2] = radians

        # 这里可以安全地进行视图刷新或数据更新
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

    name_buf: bpy.props.StringProperty(
        name='Name', update=update_name)
    end_name: bpy.props.StringProperty(get=lambda self: f"{self.name}_End")
    start: bpy.props.IntProperty(name="Start", update=update_start)
    end: bpy.props.IntProperty(name="End", update=update_end)

    fixed_direction: bpy.props.BoolProperty(
        name='固定方向', update=update_direction)
    use_direction: bpy.props.BoolProperty(
        name='使用方向', update=update_direction)  # 给渲染使用
    direction: bpy.props.IntProperty(name='物体方向', update=update_direction)
    angle: bpy.props.FloatProperty(name='物体角度', get=get_angle)
    angle_text: bpy.props.StringProperty(name='物体方向', get=get_angle_text)

    def apply_timeline(self, context: bpy.types.Context):
        context.scene.frame_current = self.start
        context.scene.frame_start = self.start
        context.scene.frame_end = self.end
        self.update_direction(context)
