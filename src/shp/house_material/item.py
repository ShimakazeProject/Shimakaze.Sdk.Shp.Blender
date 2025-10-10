from __future__ import annotations
import bpy


class SHP_PG_HouseMaterial(bpy.types.PropertyGroup):
    def update_material(self, context: bpy.types.Context):
        self.material: bpy.types.Material

        self.name = self.material.name

    material: bpy.props.PointerProperty(
        name='Material', type=bpy.types.Material, update=update_material)

    @staticmethod
    def apply(material: bpy.types.Material, value: float):
        from .settings import SHP_PG_HouseMaterialSettings

        nodes = material.node_tree.nodes
        # 获取 HouseNodeGroup
        house_group_node = nodes.get(SHP_PG_HouseMaterialSettings.group_name)
        if not house_group_node:
            print(f"找不到节点组 {SHP_PG_HouseMaterialSettings.group_name}")
            return False

        # 设置默认值
        house_group_node.inputs['Factor'].default_value = value
        return True
