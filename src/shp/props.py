import math
import typing
import bpy


class SHP_PG_MaterialItem(bpy.types.PropertyGroup):
    material: bpy.props.PointerProperty(
        name='Material', type=bpy.types.Material)


class SHP_PG_ObjectItem(bpy.types.PropertyGroup):
    object: bpy.props.PointerProperty(
        name='Object', type=bpy.types.Object)


class SHP_PG_HideObject(bpy.types.PropertyGroup):
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

    def get_output(self):
        mode = "House" if self.house_mode else self.mode
        path = self.output_template.replace(
            '{direction}', f"{self.direction}").replace('{mode}', mode)
        return path

    def update_output(self, context: bpy.types.Context):
        path = self.get_output()
        if context.scene.render.filepath != path:
            context.scene.render.filepath = path

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

        return signs[self.direction % len(signs)]

    def on_direction_changed(self, context: bpy.types.Context):
        for item in self.objects:
            item: SHP_PG_ObjectItem
            item.object.rotation_euler[2] = math.radians(self.angle + 225)

        self.update_output(context)

        # 这里可以安全地进行视图刷新或数据更新
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()

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

    def on_house_mode_changed(self, context: bpy.types.Context):
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

    def on_render_settings_changed(self, context: bpy.types.Context):
        if self.use_alpha:
            bpy.context.scene.node_tree.nodes["Alpha"].check = True
            bpy.context.scene.render.image_settings.color_mode = 'RGBA'
        else:
            bpy.context.scene.node_tree.nodes["Alpha"].check = False
            bpy.context.scene.render.image_settings.color_mode = 'RGB'
        self.init_render_settings(self.mode)
        self.update_output(context)

    enabled: bpy.props.BoolProperty(name='enabled')

    use_alpha: bpy.props.BoolProperty(
        name='Alpha', update=on_render_settings_changed)
    house_mode: bpy.props.BoolProperty(
        name='所属色模式', update=on_house_mode_changed)
    mode: bpy.props.EnumProperty(name='Mode', items=[
        ('Object', '对象', '渲染对象'),
        ('Shadow', '影子', '渲染影子'),
        ('Buildup', 'Buildup', 'Buildup'),
        ('Preview', 'Preview', 'Preview'),
        ('Reset', 'Reset', 'Reset'),
    ], update=on_render_settings_changed)

    output_template: bpy.props.StringProperty(
        name='输出模板', default='//{direction}/{mode}_')
    output: bpy.props.StringProperty(name='Output Path', get=get_output)

    house_materials: bpy.props.CollectionProperty(
        name='所属色材质', type=SHP_PG_MaterialItem)
    active_house_material_index: bpy.props.IntProperty(
        name='当前选中的所属色材质')

    objects: bpy.props.CollectionProperty(
        name='对象', type=SHP_PG_ObjectItem)
    active_object_index: bpy.props.IntProperty(
        name='当前选中的对象')

    directions: bpy.props.IntProperty(
        name='方向数/8', min=0, default=1, update=on_directions_changed)
    direction_count: bpy.props.IntProperty(
        name='方向数量', get=get_direction_count)
    angle_per_direction: bpy.props.FloatProperty(
        name='每方向角度', get=get_angle_per_direction)
    direction: bpy.props.IntProperty(name='物体方向', update=on_direction_changed)
    angle: bpy.props.FloatProperty(name='物体角度', get=get_angle)
    angle_text: bpy.props.StringProperty(name='物体方向', get=get_angle_text)
