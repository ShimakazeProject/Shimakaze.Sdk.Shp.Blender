from __future__ import annotations
import bpy

from .item import SHP_PG_HouseMaterial
from .settings import SHP_PG_HouseMaterialSettings


class SHP_UL_house_material_list(bpy.types.UIList):
    bl_idname = 'SHP_UL_house_material_list'

    def draw_item(self, context, layout: bpy.types.UILayout, data, item: SHP_PG_HouseMaterial, icon, active_data, active_propname, index):
        mat: bpy.types.Material = item.material
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if mat:
                layout.prop(mat, 'name', text='', emboss=False,
                            icon_value=layout.icon(mat))
            else:
                layout.label(text='', translate=False,
                             icon_value=layout.icon(mat))
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text='', icon_value=layout.icon(mat))


class SHP_PT_HouseMaterial(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SHP'
    bl_label = 'Shp 所属色材质'
    bl_idname = 'SHP_PT_house_material'
    bl_order = 3

    def draw(self, context):
        from .operators import SHP_OT_HouseMaterial_Init, SHP_OT_HouseMaterial_Add, SHP_OT_HouseMaterial_Remove, SHP_OT_HouseMaterial_Set_0, SHP_OT_HouseMaterial_Set_1

        layout = self.layout
        house_material_settings = SHP_PG_HouseMaterialSettings.get_instance()
        if not house_material_settings:
            return

        row = layout.row(align=True)
        row.template_list(
            SHP_UL_house_material_list.bl_idname, '',
            house_material_settings, 'house_materials',
            house_material_settings, 'current_house_material_index')
        col = row.column(align=True)
        col.operator(SHP_OT_HouseMaterial_Init.bl_idname,
                     icon='MATERIAL_DATA',
                     text='')
        col.operator(SHP_OT_HouseMaterial_Add.bl_idname, icon='ADD', text='')
        col.operator(SHP_OT_HouseMaterial_Remove.bl_idname,
                     icon='REMOVE', text='')

        row = layout.row(align=True)
        row.operator(SHP_OT_HouseMaterial_Set_1.bl_idname, icon='HIDE_ON')
        row.operator(SHP_OT_HouseMaterial_Set_0.bl_idname, icon='HIDE_OFF')

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='MATERIAL_DATA', text="")
