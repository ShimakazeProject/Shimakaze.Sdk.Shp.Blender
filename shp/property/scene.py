import math
import bpy

from .object import SHP_PG_Object

class SHP_PG_Scene(bpy.types.PropertyGroup):
    def on_enabled_changed(self, context: bpy.types.Context):
        self.on_target_changed(context)

    def on_target_changed(self, context: bpy.types.Context):
        if self.target:
            self.target.rotation_euler[2] = math.radians(225 if self.enabled else 0)
        elif self.old_target:
            # self.old_target.shp.direction = 0
            self.old_target.rotation_euler[2] = 0

        self.old_target = self.target

    def get_output(self):
        if not self.target:
            return '//'
        
        object: SHP_PG_Object = self.target.shp
        action = object.get_active_action()
        return self.output_template.replace('{action}', action.name).replace('{type}', object.type)

    enabled: bpy.props.BoolProperty(name='启用', update=on_enabled_changed)
    target: bpy.props.PointerProperty(name='Target', type=bpy.types.Object, update=on_target_changed)
    old_target: bpy.props.PointerProperty(type=bpy.types.Object)
    output_template: bpy.props.StringProperty(name='输出模板', default='//{action}/{type}_')
    output: bpy.props.StringProperty(name='输出路径', get=get_output)
    
    script_alpha: bpy.props.PointerProperty(name='透明脚本', type=bpy.types.Text)
    script_object: bpy.props.PointerProperty(name='对象脚本', type=bpy.types.Text)
    script_shadow: bpy.props.PointerProperty(name='阴影脚本', type=bpy.types.Text)
