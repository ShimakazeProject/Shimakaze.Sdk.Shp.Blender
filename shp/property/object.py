import math
from typing import List
import bpy

from .material_item import SHP_PG_MaterialItem


class SHP_PG_Object(bpy.types.PropertyGroup):

    def on_target_changed(self, context: bpy.types.Context):
        print(context)

    def on_type_changed(self, context: bpy.types.Context):
        scene = context.scene.shp
        if scene.script_alpha:
            text: bpy.types.Text = scene.script_alpha
        if text:
            exec(text.as_string())
        if self.type == 'object' and scene.script_object:
            text: bpy.types.Text = scene.script_object
        elif self.type == 'shadow' and scene.script_shadow:
            text: bpy.types.Text = scene.script_shadow
        elif self.type == 'house' and scene.script_object:
            text: bpy.types.Text = scene.script_object
        if text:
            exec(text.as_string())

        materials = self.get_materials()
        for material in materials:
            skip = False
            for item in self.house_materials:
                if item.material == material:
                    skip = True
                    break
            if skip:
                continue

            nodes = material.node_tree.nodes

            # 获取 HouseNodeGroup
            group_name = "HouseNodeGroup"
            index = nodes.find(group_name)
            if index == -1:
                print(f"找不到节点组 {group_name}")
                continue

            house_group_node = nodes[index]

            # 设置默认值
            house_group_node.inputs['Factor'].default_value = 1 if self.type == 'house' else 0

    def get_materials(self):
        list: List[bpy.types.Object] = [self.target]
        for item in self.target.children_recursive:
            list.append(item)

        materials: List[bpy.types.Material] = []
        for item in list:
            for slot in item.material_slots:
                mat = slot.material
                if not mat or not mat.use_nodes:
                    continue
                materials.append(mat)

        return materials

    def on_active_action_changed(self, context: bpy.types.Context):
        obj: bpy.types.Object = self.target
        if not obj:
            return

        obj.animation_data.action = self.get_active_action()
        obj.animation_data.action.shp.on_frame_changed(context)
        obj.animation_data.action.shp.on_direction_changed(context)

    def get_active_action(self):
        if self.active_action_index >= len(bpy.data.actions):
            self.active_action_index = len(bpy.data.actions) - 1
        action: bpy.types.Action = bpy.data.actions[self.active_action_index]
        return action

    target: bpy.props.PointerProperty(
        name='动画目标', type=bpy.types.Object, update=on_target_changed)

    house_materials: bpy.props.CollectionProperty(
        name='所属色材质', type=SHP_PG_MaterialItem)
    active_house_material_index: bpy.props.IntProperty(name='当前选中的所属色材质')
    type: bpy.props.EnumProperty(name='类型', items=[
        ('object', '对象', '渲染对象'),
        ('shadow', '影子', '渲染影子'),
        ('house', '所属色', '渲染所属色'),
    ], update=on_type_changed)

    active_action_index: bpy.props.IntProperty(
        name='当前选中的动作', update=on_active_action_changed)
