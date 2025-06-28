import bpy

from .. import property


class SHP_OT_Keyframes_Apply(bpy.types.Operator):
    bl_idname = 'shp.keyframes_apply'
    bl_label = '应用关键帧'
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene: property.SHP_PG_Scene = context.scene.shp
        if not scene.target:
            return {'CANCELLED'}

        object: property.SHP_PG_Object = scene.target.shp
        action: property.SHP_PG_Action = object.get_active_action().shp
        target: bpy.types.Object = object.target

        fpd = action.frame_count / action.direction_count
        if action.direction_count == 1:
            target.keyframe_insert(
                'rotation_euler', index=2, frame=0)
        else:
            for direction in range(action.direction_count):
                frame = direction * fpd
                action.direction = direction
                target.keyframe_insert(
                    'rotation_euler', index=2, frame=frame)
                fcu = target.animation_data.action.fcurves.find("rotation_euler", index=2)
                if fcu:
                    for kp in fcu.keyframe_points:
                        kp.interpolation = 'CONSTANT'
            action.direction = 0

        return {'FINISHED'}
