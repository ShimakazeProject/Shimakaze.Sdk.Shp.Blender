import bpy

from ... import property

class SHP_OT_HouseMaterial_Remove(bpy.types.Operator):
    bl_idname = 'shp.house_material_remove'
    bl_label = '移除所属色材质'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene: property.SHP_PG_Scene = context.scene.shp
        if not scene.target:
            return {'CANCELLED'}
        
        object: property.SHP_PG_Object = scene.target.shp


        object.house_materials.remove(object.active_house_material_index)
        object.active_house_material_index = max(0, object.active_house_material_index - 1)
        
        return {'FINISHED'}