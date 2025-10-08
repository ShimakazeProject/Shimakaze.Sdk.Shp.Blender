from __future__ import annotations
import typing
import bpy

from .item import SHP_PG_HouseMaterial
from ..object import SHP_PG_ObjectSettings


class SHP_PG_HouseMaterialSettings(bpy.types.PropertyGroup):
    @staticmethod
    def get_instance() -> SHP_PG_HouseMaterialSettings | None:
        from ..settings import SHP_PG_GlobalSettings
        settings = SHP_PG_GlobalSettings.get_instance()
        if settings:
            return settings.house_material

    @staticmethod
    def get_house_materials_from_objects(objects: typing.Iterable[bpy.types.Object]):
        """获取对象所属色材质"""
        materials: typing.Set[bpy.types.Material] = set()
        for object in objects:
            for slot in object.material_slots:
                mat = slot.material
                if mat:
                    materials.add(mat)

        return materials

    @staticmethod
    def apply_house_materials(list: typing.Iterable[bpy.types.Material], value: float):
        """应用所属色材质值"""
        for material in list:
            nodes = material.node_tree.nodes

            # 获取 HouseNodeGroup
            group_name = "HouseNodeGroup"
            house_group_node = nodes.get(group_name)
            if not house_group_node:
                print(f"找不到节点组 {group_name}")
                continue

            # 设置默认值
            house_group_node.inputs['Factor'].default_value = value

    def init_materials(self, context: bpy.types.Context):
        group_name = 'HouseNodeGroup'

        # 获取或创建节点组
        node_group = context.blend_data.node_groups.get(group_name)
        if not node_group:
            node_group = context.blend_data.node_groups.new(
                name=group_name, type='ShaderNodeTree')

        # 清空旧节点，确保是干净的节点组
        node_group.nodes.clear()
        node_group.links.clear()
        for item in list(node_group.interface.items_tree):
            if (item.item_type == 'SOCKET'):
                node_group.interface.remove(item)

        # 创建输入/输出节点
        group_in: bpy.types.NodeGroupInput = node_group.nodes.new(
            'NodeGroupInput')
        group_in.location = (-400, 0)
        group_out: bpy.types.NodeGroupOutput = node_group.nodes.new(
            'NodeGroupOutput')
        group_out.location = (400, 0)

        node_group.interface.new_socket(
            name='Factor', socket_type='NodeSocketFloat', in_out='INPUT')
        node_group.interface.new_socket(
            name='Shader', socket_type='NodeSocketShader', in_out='INPUT')
        node_group.interface.new_socket(
            name='Alpha', socket_type='NodeSocketFloat', in_out='INPUT')
        node_group.interface.new_socket(
            name='Shader', socket_type='NodeSocketShader', in_out='OUTPUT')

        mix = node_group.nodes.new('ShaderNodeMixShader')
        mix.location = (200, 0)

        mix2 = node_group.nodes.new('ShaderNodeMixShader')
        mix2.location = (0, -100)
        transparent = node_group.nodes.new('ShaderNodeBsdfTransparent')
        transparent.location = (-200, -100)
        holdout = node_group.nodes.new('ShaderNodeHoldout')
        holdout.location = (-200, -200)

        node_group.links.new(group_in.outputs[0], mix.inputs[0])
        node_group.links.new(group_in.outputs[1], mix.inputs[1])
        node_group.links.new(group_in.outputs[2], mix2.inputs[0])

        node_group.links.new(mix.outputs[0], group_out.inputs[0])

        node_group.links.new(transparent.outputs[0], mix2.inputs[1])
        node_group.links.new(holdout.outputs[0], mix2.inputs[2])
        node_group.links.new(mix2.outputs[0], mix.inputs[2])

        objects = SHP_PG_ObjectSettings.get_instance().get_objects()
        for mat in self.get_house_materials_from_objects(objects):
            # 获取材质的节点树
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links

            # 查找输出节点
            output_node = None
            for node in nodes:
                if node.type == 'OUTPUT_MATERIAL':
                    output_node = node
                    break

            if not output_node:
                print(f'材质 {mat.name} 没有找到输出节点')
                continue

            # 创建或获取 HouseNodeGroup
            group_name = 'HouseNodeGroup'
            node_group = bpy.data.node_groups.get(group_name)
            if not node_group:
                print(f'找不到节点组 {group_name}')
                continue

            # 添加 HouseNodeGroup 实例到材质节点树
            house_group_node = nodes.new(type='ShaderNodeGroup')
            house_group_node.name = group_name
            house_group_node.label = group_name
            house_group_node.node_tree = node_group
            house_group_node.location = (
                output_node.location.x - 150, output_node.location.y)

            # 设置默认值（可选）
            house_group_node.inputs['Factor'].default_value = 0
            house_group_node.inputs['Alpha'].default_value = 1

            # 断开原有与输出节点的链接
            for link in output_node.inputs['Surface'].links:
                link: bpy.types.NodeLink
                from_socket = link.from_socket
                from_node = link.from_node
                links.remove(link)

            # 连接 HouseNodeGroup 到输出节点
            links.new(
                house_group_node.outputs['Shader'], output_node.inputs['Surface'])
            links.new(from_socket, house_group_node.inputs['Shader'])
            alpha = from_node.outputs.get('Alpha')
            if alpha:
                links.new(alpha,
                          house_group_node.inputs['Alpha'])

    def add_material(self, context: bpy.types.Context):
        mat = context.active_object.active_material
        if not mat:
            return False

        for item in self.house_materials:
            if item.material == mat:
                return False

        slot: SHP_PG_HouseMaterial = self.house_materials.add()
        slot.material = mat
        self.current_house_material_index += 1

        return True

    def remote_material(self, context: bpy.types.Context):
        if self.current_house_material_index < 0 or self.current_house_material_index >= len(self.house_materials):
            return False

        self.house_materials.remove(self.current_house_material_index)
        self.current_house_material_index = max(
            0, self.current_house_material_index - 1)

        return True

    house_materials: bpy.props.CollectionProperty(
        name='所属色材质', type=SHP_PG_HouseMaterial)
    current_house_material_index: bpy.props.IntProperty(
        name='当前选中的所属色材质')
