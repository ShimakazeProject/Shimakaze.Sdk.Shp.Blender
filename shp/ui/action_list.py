import bpy

class SHP_UL_action_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, action, icon, active_data, active_propname, index):
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if action:
                layout.prop(action, 'name', text='', emboss=False, icon_value=layout.icon(action))
            else:
                layout.label(text='', translate=False, icon_value=layout.icon(action))
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text='', icon_value=layout.icon(action))
    
            