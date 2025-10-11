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

        # 获取 HouseNodeGroup
        for node in material.node_tree.nodes:
            print(node.label)
            if node.label != SHP_PG_HouseMaterialSettings.group_name:
                continue

            # 设置默认值
            node.inputs['Factor'].default_value = value

        return True
