from __future__ import annotations
import math
import typing
import bpy


class SHP_PG_MaterialItem(bpy.types.PropertyGroup):
    material: bpy.props.PointerProperty(
        name='Material', type=bpy.types.Material)


class SHP_PG_ObjectItem(bpy.types.PropertyGroup):
    object: bpy.props.PointerProperty(
        name='Object', type=bpy.types.Object)


class SHP_PG_MarkerItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name='Name')
    name_buf: bpy.props.StringProperty(
        name='Name', update=update_name)
    end_name: bpy.props.StringProperty(get=get_end_name)
    start: bpy.props.IntProperty(name="Start", update=update_start)
    end: bpy.props.IntProperty(name="End", update=update_end)

    fixed_direction: bpy.props.BoolProperty(
        name='仅使用同一方向', update=update_direction)
    use_direction: bpy.props.BoolProperty(
        name='使用方向', update=update_direction)  # 给渲染使用
    direction: bpy.props.IntProperty(name='物体方向', update=update_direction)
    angle: bpy.props.FloatProperty(name='物体角度', get=get_angle)
    angle_text: bpy.props.StringProperty(name='物体方向', get=get_angle_text)

    def get_end_name(self):
        return self.end_name

    def update_name(self, context: bpy.types.Context):
        old_name = self.name
        new_name = self.name_buf
        marker = context.scene.timeline_markers.get(old_name)
        if marker:
            marker.name = new_name
        else:
            context.scene.timeline_markers.new(self.name, frame=self.start)

        marker = context.scene.timeline_markers.get(self.end_name)
        if marker:
            marker.name = f"{new_name}_End"
        else:
            context.scene.timeline_markers.new(
                self.end_name, frame=self.end)
        self.name = new_name

    def update_start(self, context: bpy.types.Context):
        value = self.start
        marker = context.scene.timeline_markers.get(self.name)
        if marker:
            marker.frame = value
        else:
            context.scene.timeline_markers.new(self.name, frame=value)

    def update_end(self, context: bpy.types.Context):
        value = self.end
        marker = context.scene.timeline_markers.get(self.end_name)
        if marker:
            marker.frame = value
        else:
            context.scene.timeline_markers.new(self.end_name, frame=value)

    def get_angle(self):
        settings = SHP_PG_RenderSettings.get_instance()
        return self.direction * settings.angle_per_direction

    def get_angle_text(self):
        settings = SHP_PG_RenderSettings.get_instance()
        if settings.direction_count > 16:
            return

        if settings.direction_count == 16:
            signs = ['N', 'NNW', 'NW', 'WNW', 'W', 'WSW', 'SW', 'SSW',
                     'S', 'SSE', 'SE', 'ESE', 'E', 'ENE', 'NE', 'NNE']
        else:
            signs = ['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE']

        index = self.direction % len(signs)
        if settings.reverse and input != 0:
            index = len(signs) - index

        return signs[index]

    def update_direction(self, context: bpy.types.Context):
        settings = SHP_PG_RenderSettings.get_instance()
        settings.update_output(context)

        radians = math.radians(self.angle + 225) \
            if self.fixed_direction or self.use_direction \
            else 0
        for item in settings.objects:
            item: SHP_PG_ObjectItem
            item.object.rotation_euler[2] = radians

        # 这里可以安全地进行视图刷新或数据更新
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

    def update_timeline(self, context: bpy.types.Context):
        context.scene.frame_start = self.start
        context.scene.frame_end = self.end
        context.scene.frame_current = self.start
        self.update_direction(context)


class SHP_PG_RenderSettings(bpy.types.PropertyGroup):
    use_alpha: bpy.props.BoolProperty(
        name='Alpha', update=update_render_type)
    house_mode: bpy.props.BoolProperty(
        name='所属色模式', update=update_house_mode)
    mode: bpy.props.EnumProperty(name='Mode', items=[
        ('Object', '对象', '渲染对象'),
        ('Shadow', '影子', '渲染影子'),
        ('Buildup', 'Buildup', 'Buildup'),
        ('Preview', 'Preview', 'Preview'),
        ('Reset', 'Reset', 'Reset'),
    ], update=update_render_type)

    output_template: bpy.props.StringProperty(
        name='输出模板', default='//{action}/{mode}/{direction}/', update=update_output)
    output: bpy.props.StringProperty(name='Output Path', get=get_output)

    house_materials: bpy.props.CollectionProperty(
        name='所属色材质', type=SHP_PG_MaterialItem)
    active_house_material_index: bpy.props.IntProperty(
        name='当前选中的所属色材质')

    objects: bpy.props.CollectionProperty(
        name='对象', type=SHP_PG_ObjectItem)
    active_object_index: bpy.props.IntProperty(
        name='当前选中的对象')

    markers: bpy.props.CollectionProperty(
        name='Marker', type=SHP_PG_MarkerItem)
    active_marker_index: bpy.props.IntProperty(
        name='Current Marker', update=update_timeline)

    reverse: bpy.props.BoolProperty(
        name='Reverse', description='反转方向（用于SHP载具）', update=update_direction)
    directions: bpy.props.IntProperty(
        name='方向数/8', min=0, default=1, update=update_direction)

    direction_count: bpy.props.IntProperty(
        name='方向数量', get=get_direction_count)
    angle_per_direction: bpy.props.FloatProperty(
        name='每方向角度', get=get_angle_per_direction)

    @staticmethod
    def get_instance() -> typing.Union[SHP_PG_RenderSettings | None]:
        index = bpy.data.texts.find("Shimakaze.Sdk.RenderSettings")
        if index < 0:
            return None

        shp: SHP_PG_RenderSettings = bpy.data.texts[index].shp
        return shp

    def init_render_settings(type: typing.Literal['Object', 'Shadow', 'Buildup', 'Preview', 'Reset'], engine: typing.Literal['Cycles', 'Eevee', None]):
        if engine == None:
            if bpy.context.scene.render.engine.find('CYCLES') >= 0:
                engine = 'Cycles'
            elif bpy.context.scene.render.engine.find('EEVEE') >= 0:
                engine = 'Eevee'
            else:
                raise Exception("不支持的渲染引擎")

        match bpy.context.scene.name:
            case "Red Alert 2": suffix = "RA2"
            case "Red Alert 2 - Infantry": suffix = "RA2.INF"
            case "Red Alert 2 - Effects": suffix = "RA2.FX"
            case "Tiberian Sun": suffix = "TS"
            case "Tiberian Sun - Infantry": suffix = "TS.INF"
            case "Tiberian Sun - Effects": suffix = "TS.FX"
            case "ReWire": suffix = "RW"
            case "ReWire - Infantry": suffix = "RW.INF"
            case "ReWire - Effects": suffix = "RW.FX"
            case "Red Alert / Tiberian Dawn": suffix = "RA1"
            case "Red Alert / Tiberian Dawn - Infantry": suffix = "RA1.INF"
            case "Red Alert / Tiberian Dawn - Effects": suffix = "RA1.FX"
            case "Dune 2000": suffix = "D2K"
            case "Dune 2000 - Infantry": suffix = "D2K.INF"
            case "Dune 2000 - Effects": suffix = "D2K.FX"
            case "C&C Remastered": suffix = "RM"
            case "C&C Remastered - Infantry": suffix = "RM.INF"
            case "C&C Remastered - Effects": suffix = "RM.FX"
            case _: suffix = "RA2.INF"

        for object in [
            f"Plane.holdout.{suffix}",
            f"Plane.holdout2.{suffix}",
            f"Plane.shadow.{suffix}",
            f"Plane.shadow2.{suffix}",
            f"Plane.blue.{suffix}",
            f"Plane.grey.{suffix}",
            f"Plane.ambient.{suffix}",
            f"Sun.{suffix}",
            f"Sun.shadow.{suffix}",
        ]:
            if object in bpy.data.objects:
                bpy.data.objects[object].hide_render = True

        for node in [
            "Object",
            "Buildup.Cycles",
            "Buildup.Eevee",
            "Shadow.Cycles",
            "Shadow.Eevee",
            "Preview.Cycles",
            "Preview.Eevee",
        ]:
            if node in bpy.context.scene.node_tree.nodes:
                bpy.context.scene.node_tree.nodes[node].check = False

        bpy.context.scene.cycles.filter_width = 0.9
        bpy.context.scene.render.filter_size = 0.8
        bpy.context.scene.world.use_nodes = True
        bpy.context.scene.eevee.use_gtao = True
        bpy.context.scene.render.use_single_layer = True
        match type:
            case 'Buildup':
                bpy.data.objects[f"Plane.holdout2.{suffix}"].hide_render = False
                bpy.data.objects[f"Sun.{suffix}"].hide_render = False
                bpy.context.scene.node_tree.nodes[f"Buildup.{engine}"].check = True
            case 'Object':
                if engine == 'Cycles':
                    bpy.data.objects[f"Plane.ambient.{suffix}"].hide_render = False
                bpy.data.objects[f"Sun.{suffix}"].hide_render = False
                bpy.context.scene.node_tree.nodes["Object"].check = True
            case 'Preview':
                if engine == 'Cycles':
                    bpy.data.objects[f"Plane.holdout.{suffix}"].hide_render = False
                elif engine == 'Eevee':
                    bpy.data.objects[f"Plane.holdout2.{suffix}"].hide_render = False
                    bpy.data.objects[f"Plane.shadow2.{suffix}"].hide_render = False

                bpy.data.objects[f"Plane.shadow.{suffix}"].hide_render = False
                bpy.data.objects[f"Sun.{suffix}"].hide_render = False
                bpy.context.scene.eevee.use_gtao = False
                bpy.context.scene.node_tree.nodes[f"Preview.{engine}"].check = True
            case 'Shadow':
                if engine == 'Cycles':
                    bpy.data.objects[f"Plane.holdout.{suffix}"].hide_render = False
                    bpy.data.objects[f"Plane.shadow.{suffix}"].hide_render = False
                    bpy.data.objects[f"Sun.{suffix}"].hide_render = False
                elif engine == 'Eevee':
                    bpy.data.objects[f"Plane.shadow.{suffix}"].hide_render = False
                    bpy.data.objects[f"Sun.shadow.{suffix}"].hide_render = False
                    bpy.context.scene.world.use_nodes = False
                    bpy.context.scene.eevee.use_gtao = False

                bpy.context.scene.cycles.filter_width = 0.01
                bpy.context.scene.render.filter_size = 0.01
                bpy.context.scene.render.use_single_layer = False
                bpy.context.scene.node_tree.nodes[f"Shadow.{engine}"].check = True
            case 'Reset':
                bpy.data.objects[f"Plane.grey.{suffix}"].hide_render = False
                bpy.data.objects[f"Sun.{suffix}"].hide_render = False

    def update_output(self, context: bpy.types.Context):
        if context.scene.render.filepath == self.output:
            return
        context.scene.render.filepath = self.output

    def update_render_type(self, context: bpy.types.Context):
        self.update_output(context)
        bpy.context.scene.node_tree.nodes["Alpha"].check = self.use_alpha
        bpy.context.scene.render.image_settings.color_mode = 'RGBA' if self.use_alpha else 'RGB'
        self.init_render_settings(self.mode)

    def update_house_mode(self, context: bpy.types.Context):
        self.update_output(context)
        for material in self.get_materials():
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
            house_group_node.inputs['Factor'].default_value = 1 if self.house_mode else 0

    def get_output(self):
        mode = "House" if self.house_mode else self.mode
        path = self.output_template \
            .replace('{direction}', f"{self.direction}") \
            .replace('{direction_text}', f"{self.angle_text}") \
            .replace('{action}', f"{self.get_current_marker().name}") \
            .replace('{mode}', mode)
        return path

    def get_direction_count(self):
        return max(self.directions * 8, 1)

    def get_angle_per_direction(self):
        tmp = 360 / max(self.direction_count, 8)
        return -tmp if self.reverse else tmp

    def update_direction(self, context: bpy.types.Context):
        item = self.get_current_marker()
        if item:
            item.update_direction(context)

    def get_materials(self):
        list: typing.List[bpy.types.Object] = []
        for item in self.objects:
            obj: bpy.types.Object = item.object
            list.append(obj)
            for child in obj.children_recursive:
                list.append(child)

        materials: typing.List[bpy.types.Material] = []
        for item in list:
            for slot in item.material_slots:
                mat = slot.material
                if not mat or not mat.use_nodes:
                    continue
                materials.append(mat)

        return materials

    def add_objects(self, context: bpy.types.Context):
        if len(context.selected_objects) < 1:
            return False

        for object in context.selected_objects:
            exists = False
            for item in self.objects:
                if item.object == object:
                    exists = True

            if exists:
                continue

            slot: SHP_PG_ObjectItem = self.objects.add()
            slot.object = object
            self.active_object_index += 1

        return True

    def remote_object(self, context: bpy.types.Context):
        if self.active_object_index < 0 or self.active_object_index >= len(self.objects):
            return False

        self.objects.remove(self.active_object_index)
        self.active_object_index = max(
            0, self.active_object_index - 1)

        return True

    def add_material(self, context: bpy.types.Context):
        mat = context.active_object.active_material
        if not mat:
            return False

        for item in self.house_materials:
            if item.material == mat:
                return False

        slot: SHP_PG_MaterialItem = self.house_materials.add()
        slot.material = mat
        self.active_house_material_index += 1

        return True

    def remote_material(self, context: bpy.types.Context):
        if self.active_house_material_index < 0 or self.active_house_material_index >= len(self.house_materials):
            return False

        self.house_materials.remove(self.active_house_material_index)
        self.active_house_material_index = max(
            0, self.active_house_material_index - 1)

        return True

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

        for mat in self.get_materials():
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

    def init_markers(self, context: bpy.types.Context):
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

        self.markers.clear()
        for item in frame_map:
            slot: SHP_PG_MarkerItem = self.markers.add()
            slot.name = item
            slot.name_buf = item
            (slot.start, slot.end) = frame_map.get(item)

        return True

    def add_marker(self, context: bpy.types.Context):
        self.markers.add()
        return True

    def remove_marker(self, context: bpy.types.Context):
        if self.active_marker_index < 0 or self.active_marker_index >= len(self.markers):
            return False

        self.markers.remove(self.active_marker_index)
        self.active_marker_index = max(
            0, self.active_marker_index - 1)

        return True

    def get_current_marker(self):
        item: SHP_PG_MarkerItem = self.markers[self.active_marker_index]
        return item

    def update_timeline(self, context: bpy.types.Context):
        item = self.get_current_marker()
        if not item:
            return

        item.update_timeline(context)
