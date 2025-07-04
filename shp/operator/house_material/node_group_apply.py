import bpy

from ... import property

class SHP_OT_HouseMaterial_NodeGroup_Apply(bpy.types.Operator):
    bl_idname = 'shp.house_material_node_group_apply'
    bl_label = '创建所属色节点组'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.reset_node_group(context)
        self.apply_node_group_to_materials(context)

        return {'FINISHED'}

    def apply_node_group_to_materials(self, context: bpy.types.Context):
        scene: property.SHP_PG_Scene = context.scene.shp
        if not scene.target:
            return {'CANCELLED'}
        
        object: property.SHP_PG_Object = scene.target.shp

        materials = object.get_materials()
        for mat in materials:
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
            iAlpha = from_node.outputs.find('Alpha')
            if iAlpha >= 0:
                links.new(from_node.outputs[iAlpha],
                          house_group_node.inputs['Alpha'])

    def reset_node_group(self, context: bpy.types.Context):
        # 创建一个新的节点组
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
