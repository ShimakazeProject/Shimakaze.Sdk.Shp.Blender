from pydoc import text
import bpy

class SHP_UL_material_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        mat: bpy.types.Material = item.material
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if mat:
                layout.prop(mat, 'name', text='', emboss=False, icon_value=layout.icon(mat))
            else:
                layout.label(text='', translate=False, icon_value=layout.icon(mat))
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text='', icon_value=layout.icon(mat))
    
            