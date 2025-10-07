import bpy


class SHP_UL_material_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
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


class SHP_UL_object_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        obj: bpy.types.Object = item.object
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if obj:
                layout.prop(obj, 'name', text='', emboss=False,
                            icon_value=layout.icon(obj))
            else:
                layout.label(text='', translate=False,
                             icon_value=layout.icon(obj))
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text='', icon_value=layout.icon(obj))


class SHP_UL_marker_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        item: bpy.types.TimelineMarker
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if item:
                end = item
                for i in data.timeline_markers:
                    if i.name == f"{item.name}_End":
                        end = i

                frameRange = f"{item.frame}" if item.frame == end.frame else f"{item.frame}-{end.frame}"

                row = layout.row()
                row.prop(item, 'name', text='', emboss=False,
                         icon_value=layout.icon(item))
                row.label(text=frameRange, translate=False)
            else:
                layout.label(text='', translate=False,
                             icon_value=layout.icon(item))
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text='', icon_value=layout.icon(item))
