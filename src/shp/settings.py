from __future__ import annotations
import typing
import bpy

from .object.item import SHP_PG_Object

from .render_task import SHP_PG_RenderQueue
from .house_material import SHP_PG_HouseMaterialSettings
from .action import SHP_PG_ActionSettings
from .object import SHP_PG_ObjectSettings


class SHP_PG_GlobalSettings(bpy.types.PropertyGroup):
    @staticmethod
    def get_instance() -> SHP_PG_GlobalSettings | None:
        """获取场景实例"""
        return bpy.context.scene.shp

    action: bpy.props.PointerProperty(
        name='Action', type=SHP_PG_ActionSettings)

    object: bpy.props.PointerProperty(
        name='Object', type=SHP_PG_ObjectSettings)

    house_material: bpy.props.PointerProperty(
        name='House Material', type=SHP_PG_HouseMaterialSettings)

    render_queue: bpy.props.PointerProperty(
        name='Render Queue', type=SHP_PG_RenderQueue)

    def update_render_type(self, context: bpy.types.Context):
        self.update_output(context)
        object_settings: SHP_PG_ObjectSettings = self.object
        objects = object_settings.get_objects()
        materials = SHP_PG_HouseMaterialSettings.get_house_materials_from_objects(
            objects)
        house_materials = map(lambda slot: slot.material,
                              self.house_material.house_materials)
        if self.house_mode:
            SHP_PG_HouseMaterialSettings.apply_house_materials(materials, 1)
        else:
            SHP_PG_HouseMaterialSettings.apply_house_materials(materials, 0)

        SHP_PG_HouseMaterialSettings.apply_house_materials(house_materials, 0)

        context.scene.node_tree.nodes["Alpha"].check = self.use_alpha
        context.scene.render.image_settings.color_mode = 'RGBA' if self.use_alpha else 'RGB'
        self.init_render_settings(self.mode, None)

    use_alpha: bpy.props.BoolProperty(
        name='Alpha', update=update_render_type)
    house_mode: bpy.props.BoolProperty(
        name='所属色模式', update=update_render_type)
    mode: bpy.props.EnumProperty(name='Mode', items=[
        ('Object', '对象', '渲染对象'),
        ('Shadow', '影子', '渲染影子'),
        ('Buildup', 'Buildup', 'Buildup'),
        ('Preview', 'Preview', 'Preview'),
        ('Reset', 'Reset', 'Reset'),
    ], update=update_render_type)
    actived_mode: bpy.props.StringProperty(
        name='Actived Mode', get=lambda self: "House" if self.house_mode else self.mode)

    def get_output(self):
        mode = self.actived_mode
        action_settings: SHP_PG_ActionSettings = self.action
        action = action_settings.get_current_action()
        path: str = self.output_template
        path = path.replace('{mode}', mode)

        direction = action.direction
        angle_text = action.angle_text
        if self.direction_count == 1:
            direction = self.direction
            angle_text = self.angle_text

        if action:
            path = path.replace('{direction}', f"{direction}")
            path = path.replace('{direction_text}', f"{angle_text}")
            path = path.replace('{action}', f"{action.name}")
        return path

    output: bpy.props.StringProperty(name='Output Path', get=get_output)

    def update_output(self, context: bpy.types.Context):
        if context.scene.render.filepath == self.output:
            return
        context.scene.render.filepath = self.output

    output_template: bpy.props.StringProperty(
        name='Output', default='//{action}/{mode}/{direction}/', update=update_output)

    def update_direction(self, context: bpy.types.Context):
        action_settings: SHP_PG_ActionSettings = self.action
        action = action_settings.get_current_action()
        if action:
            action.update_direction(context)
        else:
            object_settings: SHP_PG_ObjectSettings = self.object
            radians = math.radians(self.angle + 225) \
                if self.fixed_direction or self.use_direction \
                else 0
            for item in object_settings.objects:
                item: SHP_PG_Object
                item.object.rotation_euler[2] = radians

            # 这里可以安全地进行视图刷新或数据更新
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()

    reverse: bpy.props.BoolProperty(
        name='Reverse', description='反转方向（用于SHP载具）', update=update_direction)
    directions: bpy.props.IntProperty(
        name='方向数/8', min=0, default=1, update=update_direction)

    direction_count: bpy.props.IntProperty(
        name='方向数量', get=lambda self: max(self.directions * 8, 1))
    angle_per_direction: bpy.props.FloatProperty(
        name='每方向角度', get=lambda self: (360 / max(self.direction_count, 8)) * (-1 if self.reverse else 1))

    direction: bpy.props.IntProperty(name='物体方向', update=update_direction)
    angle: bpy.props.FloatProperty(
        name='物体角度', get=lambda self: self.direction * self.angle_per_direction)
    angle_text: bpy.props.StringProperty(
        name='物体方向', get=lambda self: SHP_PG_GlobalSettings.calc_angle_text(self.direction_count, self.direction, self.reverse))

    @staticmethod
    def init_render_settings(
            type: typing.Literal['Object', 'Shadow', 'Buildup', 'Preview', 'Reset'],
            engine: typing.Literal['Cycles', 'Eevee', None] = None):
        """初始化渲染设置"""
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

    @staticmethod
    def calc_angle_text(direction_count: int, direction: int, reverse: bool = False):
        direction_count = max(direction_count, 8)
        index = direction % direction_count

        if direction_count > 16:
            return f'{index}'

        if reverse and index != 0:
            index = direction_count - index

        if direction_count == 16:
            signs = ['N', 'NNW', 'NW', 'WNW', 'W', 'WSW', 'SW', 'SSW',
                     'S', 'SSE', 'SE', 'ESE', 'E', 'ENE', 'NE', 'NNE']
        else:
            signs = ['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE']

        return signs[index]
