# Shimakaze.Sdk SHP Blender

使用说明

这个扩展适用于 Blender 4.2 以上版本, 与 template.blend[^template] 配合使用

在 3D 视图中找到 `SHP` 面板
1. 点击`启用`（此设置绑定窗口）

- `方向数/8`：此属性*8为实际的方向数 默认为1 表示这个动作有8个方向 填0表示只有一个方向
- `物体方向`：此属性修改`动画目标`的`欧拉旋转`的Z轴值 值为 `物体方向`*`每方向角度`

[^template]: 模板来自 [PPM](https://ppmforums.com/topic-36965/blender-templates-tdra-ts-ra2/) [revora](https://forums.revora.net/topic/97398-blender-templates-tdra-ts-ra2/)

## 所属色材质
所属色材质是为 [Shimakaze.Sdk.Shp.Maker](https://github.com/ShimakazeProject/Shimakaze.Sdk/tree/HEAD/src/shp/Shimakaze.Sdk.Shp.Maker) 工具设计的

右侧从上到下分别是 `创建所属色阻隔节点组` `添加选中材质` `从列表中移除材质`

`创建所属色阻隔节点组`：此按钮会创建一个名为 `HouseNodeGroup` 的节点组

在设置`类型`为`所属色`时 所有不在列表中的材质的`HouseNodeGroup`节点组的系数都会被设置为 `1`

这样设置后 场景中将只显示将要被渲染为所属色的部分
