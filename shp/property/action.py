import math
import bpy

class SHP_PG_Action(bpy.types.PropertyGroup):
    def on_frame_changed(self, context: bpy.types.Context):
        context.scene.frame_start = self.frame_start
        context.scene.frame_end = self.frame_end
        
    def get_frame_count(self):
        return self.frame_end - self.frame_start + 1
    def on_directions_changed(self, context: bpy.types.Context):
        self.on_direction_changed(context)

    def get_direction_count(self):
        return max(self.directions * 8, 1)

    def get_angle_per_direction(self):
        return 360 / max(self.direction_count, 8)

    def get_angle(self):
        return self.direction * self.angle_per_direction

    def get_angle_text(self):
        if self.direction_count > 16:
            return

        if self.direction_count == 16:
            signs = ['N', 'NNW', 'NW', 'WNW', 'W', 'WSW', 'SW', 'SSW',
                     'S', 'SSE', 'SE', 'ESE', 'E', 'ENE', 'NE', 'NNE']
        else:
            signs = ['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE']

        return signs[self.direction]

    def on_direction_changed(self, context: bpy.types.Context):
        target = context.scene.shp.target.shp.target
        if not target:
            return

        target.rotation_euler[2] = math.radians(self.angle)
        # 这里可以安全地进行视图刷新或数据更新
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

    frame_start: bpy.props.IntProperty(name='起始帧', update=on_frame_changed)
    frame_end: bpy.props.IntProperty(name='结束帧', update=on_frame_changed)
    frame_count: bpy.props.IntProperty(name='帧数', get=get_frame_count)

    directions: bpy.props.IntProperty(
        name='方向数/8', min=0, default=1, update=on_directions_changed)
    direction_count: bpy.props.IntProperty(
        name='方向数量', get=get_direction_count)
    angle_per_direction: bpy.props.FloatProperty(
        name='每方向角度', get=get_angle_per_direction)

    direction: bpy.props.IntProperty(name='物体方向', update=on_direction_changed)
    angle: bpy.props.FloatProperty(name='物体角度', get=get_angle)
    angle_text: bpy.props.StringProperty(name='物体方向', get=get_angle_text)
