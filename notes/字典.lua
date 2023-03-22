--by:う丶青木
--ps:删减版随手笔记
-----------------------------------------常用函数------------------------------------------------
GLOBAL.TheWorld												--获取世界
GLOBAL.unpack												--解包表格
components													--组件模块
return														--返回结果
break														--直接跳出循环
SpawnPrefab("ash")											--产卵预设实体
local x,y,z = ConsoleWorldPosition():Get()					--指针坐标
local x,y,z = inst.Transform:GetWorldPosition()				--获取实体坐标
inst.Transform:SetPosition(0,0,0)
local pos = inst:GetPosition()								--获取实体坐标【Vector3()】
x, y = TheSim:GetScreenPos(x,y,z)							--获取世界坐标 到 屏幕上的像素坐标点
local qm = GLOBAL.TheSim:FindEntities(x, 0, z, 1, {"_combat","_health","locomotor","_inventoryitem"}, {"locomotor","FX","NOCLICK","DECOR","INLIMBO","nightmarecreature"})
local qm = FindEntity(inst, 8, function(guy)
for k,v in pairs(ents) do									--循环乱序读取
for i,v in ipairs(ents) do									--循环顺序读取
while true do Sleep(0.1) end								--循环
repeat Sleep(0.1) until true								--循环
inst.persists = false										--不持续存在
local maxw,maxh = GLOBAL.TheSim:GetScreenSize()				--获取句柄最大尺寸
distsq(Vector3(0,0,0), inst:GetPosition()) > 2*2			--测距
inst:GetDistanceSqToPoint(0,0,0) > 2*2						--测距
inst:FacePoint(x,y,z)													--面向点
inst:ForceFacePoint(x,y,z)												--强制面向点
function()													--函数fn
inst:Remove()												--实体删除
UserToPlayer('う丶青木')									--获取玩家
GetPlayer()													--获取玩家
ThePlayer													--获取玩家
ThePlayer.userid											--获取玩家的KU_ID
self:GetGUID()												--获取实体标识符ID
Ents[guid]													--获取标识符ID的实体
inst:AddTag("NOCLICK")										--不可被点击，查看
inst:AddTag("NOBLOCK")										--不可被查看	建造不会被遮挡
inst:AddTag("notarget")										--不能被作为目标
inst:AddTag("CLASSIFIED")									--增加保密标签
inst:RemoveTag("pollinator")
inst:HasTag("player")										--判定有"player"标签
inst:HasTag("playerghost")									--判定有"playerghost"标签
inst:IsStandState("quad")									--判定有"quad" 行为标签
inst:SetStandState("quad")									--设置增加"quad" 行为标签
inst.sg:RemoveStateTag("busy")								--设置取消"busy" 行为标签
math.random()												--获取随机数
function GetRandomMinMax(min, max)
    return min + math.random()*(max - min)
end
weighted_random_choice({qm=20,mp=10})						--获取质量随机数
inst:SetPrefabNameOverride("qm")							--重设预设物名字
GLOBAL.STRINGS.NAMES[string.upper("qm")]
GLOBAL.FRAMES												--33毫秒
fx.entity:SetParent(A.entity)								--跟随实体
inst:IsValid()												--是否为有效单位
inst:IsInLimbo()											--是否被库存
inst.entity:IsVisible()										--实体是否显示状态
inst.entity:SetInLimbo(true)								--设置离开状态
inst.prefab == "wes"										--实体预设名
inst:SetDeployExtraSpacing(4)								--设置额外间距
inst:AddComponent("talker")									--添加"话语者"组件
inst:RemoveComponent("talker")								--删除"话语者"组件
inst.OnEntityWake = onwake									--实体激活时调用	if inst.entity:IsAwake() then
inst.OnEntitySleep = onsleep								--实体休眠时调用
inst.entity:SetCanSleep(false)								--不会进入休眠状态

print(TheWorld.minimap.MiniMap:MapPosToWorldPos(0,0,0))		--从地图到世界的向量获取
print(TheWorld.minimap.MiniMap:WorldPosToMapPos(0,0,0))

GetPlayer().sg:GoToState("corpse",true)						--扑街
inst:ShowActions(false)										--禁止行为
----------------------------------------------克隆

----------------------------------------------
MakeInventoryPhysics(inst)									--增加物理性【物品】
RemovePhysicsColliders(inst)								--取消物理性碰撞
inst.Physics:SetActive(false)								--关闭物理碰撞效果
inst._ispathfinding:set(false)								--自动寻路
inst.Physics:SetMass(0)										--自由落体速率   0为不掉落，默认1	质量
inst.Physics:SetSphere(.5)									--物理范围
inst.Physics:SetFriction(.1)								--设置摩擦
inst.Physics:SetDamping(0)									--设置阻尼
inst.Physics:SetRestitution(.5)								--设置恢复
inst.Physics:SetCollisionGroup(COLLISION.ITEMS)				--设置碰撞组
inst.Physics:ClearCollisionMask()							--清除冲突面
inst.Physics:CollidesWith(COLLISION.WORLD)					--增加冲突面
inst.Physics:CollidesWith(COLLISION.OBSTACLES)				--增加冲突面
inst.Physics:SetCapsule(rad, 1)								--物理碰撞体积，碰撞高度
inst.Physics:SetCylinder(.6, 2)								--中空类型的物理性

inst.Physics:GetMass()										--获取质量
inst.Physics:GetRadius()									--获取物理碰撞范围
inst.Physics:Teleport(x,y,z)								--物理传送
--------------------------------------------------------------抓取角度

-----------
  	--向内牵引
inst.Physics:SetMotorVelOverride(0,0,0)						--物理运行覆盖
inst.Physics:ClearMotorVelOverride()
inst.Physics:Stop()											--停止物理性运动
inst.Physics:SetMotorVel(0,0,0)
local x,y,z = inst.Physics:GetMotorVel						--获取电机速度
local cur_speed = self.inst.Physics:GetMotorSpeed()			--获取电机转速
Vector3(inst.Physics:GetVelocity()):LengthSq() >= 1			--电机速率
inst.Physics:SetCollisionCallback(OnCollide)				--碰撞时执行
function OnCollide(inst, other) end
inst.Physics:SetCollisionCallback(nil)						--清空碰撞回调
--物理性时间预测公式:例:

--------------获取角度

----------------------照明
inst.entity:AddLight()
inst.Light:Enable(true)										-- 开启照明    false为关闭
inst.Light:SetIntensity(.75)								-- 光照强度.99为强光
inst.Light:SetColour(200 / 255, 150 / 255, 50 / 255)
inst.Light:SetFalloff(0.5)									-- 最大范围再向外辐射的光效，1几乎不辐射
inst.Light:SetRadius(6)										-- 照明范围
inst.Light:EnableClientModulation(false)					-- false 不读取客户端的设置，  true 读取客户端本地数据
-------------------------追随图层
local inst = SpawnPrefab("ash")
inst.entity:AddFollower()
inst.Follower:FollowSymbol(A.GUID, "swap_object", 50, -25, 0)		---左0右偏移,  -上0下偏移
-------------------------协程 and 计时器
inst:DoTaskInTime(1.5, inst.Remove)
inst:DoTaskInTime(10, function()  end)
inst:DoPeriodicTask(30, function()  end, 0, owner)
inst:DoTaskInTime(10, function()  end, owner)
inst.pzz = inst:StartThread(function() while true do Sleep(0.1) end end)
inst.pzz:Cancel()
inst.pzz:SetList(nil)
inst.pzz = nil
																				--取消计时器
if inst.qm_jsq then
	inst.qm_jsq:Cancel()
	inst.qm_jsq = nil
end
---------------------------表 and 元表
test = {["a"] = 1,["b"] = 2,["c"] = 3,["d"] = 4,["e"] = 5,["f"] = 6}
test = {a = 1,b = 2,c = 3,d = 4,e = 5,f = 6}
test[a] == 1

next(test) == nil																--索引表内数据，是否为nil表
test = {1,2,3,4,5,6,}
test = {[1] = 1,[2] = 2,[3] = 3,[4] = 4,[5] = 5,[6] = 6}
#test																			--返回  最大序列
#(test)																			--返回  最大序列
test[#test]																		--选取表内最大键位值
table.getn(test)																--返回数组的总数量			结果 6 
table.insert(test, "7")															--把"7"加入到表内[默认排在最后序列]
table.insert(test, 2, "7")														--把"7"插入到[2]号键位
local a = table.remove(test, 7)													--从表中剔除键位[7]的值，并返回该值	【自动排序】
table.sort(test,function(a,b) return a>b end)									--按规则排序表
table.sort(test)																--使用【默认规则】排序
table.contains(test, "7")														--在表中索引"7",  有该值返回结果 true
local str = tostring(test)														--连接表内所有的字符串

local A = getmetatable(GetPlayer().AnimState).__index							--获取元表
for k,v in pairs(A) do 
	print(k) 
end

															--打印表  "return {"11",b={"22",c={"33"}}}"
----------------------------------------图片切图公式

---------------------------------监听事件
inst:ListenForEvent("qm_cc", function(owner, data)  end, owner)					--设置监听“qm_cc”事件【被监听者为owner】
inst:PushEvent("qm_cc", {q = "1", m = inst, cc = 9})							--推动事件给监听器
																				--取消所有针对“qm_cc”的监听


inst:RemoveAllEventCallbacks()													--取消全部监听
-------------------------------------------定身 and 解放

---------------------------------武器充能----------------

											--10秒CD
									--关闭武器AOE许可
---------------------------------------------------------击退
								--平滑击退
		--高飞摔倒击退
		--小跳击飞
------------------------模拟鼠标左键点击的操作行为函数

---查看行为函数

--查看菜单id



				--菜单制作


			--脱落手持物品【整组】
			--脱落手持物品【单个】
		--获取装备上的背包
										--传送指定槽物品去C容器
				--右键行为物品
-------------------------------------------------------正向判定有效地形

    --1,2,3  正向，空间，侧向【+左翼，-右翼】

------------------------------------------------属性递减公式

----------------------------------射线区域判定法---------------------------------

-----------开始计算偏移------------

------------------------------------------------------------------------------------官方射线函数【未测试】
					--(原点,终点,宽度,测试点)		返回 true or false
----------------------------------------------实体附加字体【客户端成像】
inst.entity:AddLabel()
inst.Label:SetFontSize(50)										--字体大小
inst.Label:SetFont(DEFAULTFONT)									--字体库
inst.Label:SetWorldOffset(0, 3, 0)								--偏移量【世界坐标系数】
inst.Label:SetUIOffset(0, 0, 0)									--偏移量【像素坐标系数】
inst.Label:SetColour(1, 1, 1)									--设置颜色
inst.Label:Enable(true)											--设置开启显示
inst.Label:SetText("1111")
-----------------------------------------------实体附加图层【客户端成像】
inst.entity:AddImage()
inst.Image:SetTexture("images/inventoryimages.xml", "spear_rose.tex") 
inst.Image:SetTint(1,1,1,1) 
inst.Image:SetWorldOffset(0,3,0) 								-- 左右  上下  ？？
inst.Image:SetUIOffset(12,0,0) 									-- 左右  上下  ？？
inst.Image:Enable(true) 
-----------------------------------------------客户端保存数据字符串
					--名字，字符串，ENCODE_SAVES，回调


-----读取字符串

-----擦除字符串

----------------------------------------------------动画处理
if inst.AddAnimState:IsCurrentAnimation("open_loop") then				--判定当前播放的动画
inst:ListenForEvent("animover", inst.Remove)							--监听动画结束，动画结束后删除
inst.entity:AddAnimState()												--创建图像动画集
inst.AnimState:SetBank("ceshi")											--设置动画组
inst.AnimState:SetBuild("ceshi")										--设置动画图层包
inst.AnimState:PlayAnimation("sway_loop_agro", true)					--指定播放动作
inst.AnimState:PushAnimation("dart_long", false)						--播放完上一段动画后播放本动画
inst.AnimState:OverrideSymbol("swap_object", "swap_qmwq", "swap_qm7")	--覆盖图层包
inst.AnimState:OverrideMultColour(0, 0, 0, 1)							--覆盖颜色
inst.AnimState:SetAddColour(0, 1, 0, 1)									--设置增加颜色
inst.AnimState:GetAddColour()											--获取被增加的颜色
inst.AnimState:SetMultColour(0, 1, 0, 1)								--设置颜色
inst.AnimState:GetMultColour()											--获取颜色
				--设置图层样式，  OnGround=1, 地皮    Default=0,默认
											--设置旋转角度
				
								--设置图层覆盖优先度	1=地皮
											--同上			1=最低优先度
										--设置实体规模大小
										--设置自身光照等级	0-1	1=夜幕不遮挡	0=随夜幕变暗
											--设置闪耀(作祟效果)    false为关闭
inst.AnimState:GetCurrentAnimationLength() + FRAMES						--获取当前动画时间长度
inst.AnimState:GetCurrentAnimationTime									--获取当前动画时间
local k = 1 - inst.AnimState:GetCurrentAnimationTime() / inst.AnimState:GetCurrentAnimationLength()
									--设置播放动画到50%的帧数位置
inst.AnimState:GetCurrentFacing()										--获取当前动画的朝向
inst.AnimState:SetHighlightColour(r, g, b, 0)							--设置高亮色彩
								--设置图像宽和高，负数为旋转90°
											--快进播放
							--设置动画播放速率	1=默认	.5=变慢50%
											--设置图层[长],[宽]度
							--设置淡出效果(恢复状态为 0, 0.1, 1.0)
inst.AnimState:AddOverrideBuild("fossilized")							--添加覆盖建设
inst.AnimState:ClearOverrideBuild("fossilized")							--明确覆盖建设
																		--淡出参数(叠加图大小),(叠加图扩散大小),(透明度，位深)
					--获取Symbol的坐标点

inst.AnimState:SetBloomEffectHandle("shaders/anim_bloom_ghost.ksh")		--全屏泛光[低光]  [高光为"shaders/anim.ksh"]
-------------------------------------------------------系统时间
										---->  12/17/16			通用
									---->  00:58:10			通用
								---->  12/17/2016		通用
								---->  2016/12/17		通用
							---->  2016/12/17  00:58:10	通用
					---->  2016-12-17 00:58:10	通用
							---->  20161217 005810		通用
	--获取指定日期的秒数	通用
										---->   获取世界随机种子
-----------------------------------------------------读写  【保护】非官方允许的文件，禁止读写 = =！

----------------------------------------------------------------单独重置一个世界

----------------------------------------获取所有连接的世界[当前世界不计算在内]

------------------------------------------------------实体保存函数
local function OnSave_qm11(inst,data)
	if inst.OldOnSave_qm11 ~= nil then
		inst.OldOnSave_qm11(inst,data)
	end
end

local function OnLoad_qm11(inst,data)
	if inst.OldOnLoad_qm11 ~= nil then
		inst.OldOnLoad_qm11(inst,data)
	end
	if data ~= nil then
	    
	end
end

inst.OldOnSave_qm11 = inst.OnSave
inst.OnSave = OnSave_qm11
inst.OldOnLoad_qm11 = inst.OnLoad
inst.OnLoad = OnLoad_qm11
----------------------------------------------------四象边线
------------方形
local B = 34  -- 范围
local C = "ash"
local pt = Vector3ConsoleWorldPosition()
for k = 0, 69 do  -- 数量长度
	SpawnPrefab(C).Transform:SetPosition(pt.x - B + k * 1,0,pt.z - B)
	SpawnPrefab(C).Transform:SetPosition(pt.x + B,0,pt.z + B - k * 1)
	SpawnPrefab(C).Transform:SetPosition(pt.x + B - k * 1,0,pt.z + B)
	SpawnPrefab(C).Transform:SetPosition(pt.x - B,0,pt.z - B + k * 1)
end
----------单边↖
local C = "ash"
local pt = ConsoleWorldPosition()
for k = 0, 10 do
	SpawnPrefab(C).Transform:SetPosition(pt.x,0,pt.z - k * 1)
end
----------单边↗
local C = "ash"
local pt = ConsoleWorldPosition()
for k = 0, 10 do
	SpawnPrefab(C).Transform:SetPosition(pt.x - k * 1,0,pt.z)
end
----------单边↙
local C = "ash"
local pt = ConsoleWorldPosition()
for k = 1, 10 do
	SpawnPrefab(C).Transform:SetPosition(pt.x + k * 1,0,pt.z)
end
----------单边↘
local C = "ash"
local pt = ConsoleWorldPosition()
for k = 1, 10 do
	SpawnPrefab(C).Transform:SetPosition(pt.x,0,pt.z + k * 1)
end
-----------------------------------------------------弹出网页
				-- 弹网页,设置弹窗面积

---------------------------------------------------------地图相关
inst:SetGroundTargetBlockerRadius(radius)									--设置目标拦截半径
local v = ConsoleWorldPosition()
if TheWorld.Map:IsPassableAtPoint(v:Get()) then								--判断是否是有效地皮
(TheWorld.Map:IsAboveGroundAtPoint(pos:Get()) and not TheWorld.Map:IsGroundTargetBlocked(pos))
					--获取地皮中心点
local tile = TheWorld.Map:GetTileAtPoint(v:Get())							--获取瓷砖类型
local tx, ty = TheWorld.Map:GetTileCoordsAtPoint(v:Get())					--获取瓷砖的坐标
TheWorld.Map:SetTile(tx,ty, DIPI)											--设置瓷砖类型
TheWorld.Map:RebuildLayer( tile, tx, ty )									--刷新瓷砖
TheWorld.Map:RebuildLayer( DIPI, tx, ty )									--更新瓷砖
local minimap = TheWorld.minimap.MiniMap
minimap:RebuildLayer(tile, tx, ty)
minimap:RebuildLayer(DIPI, tx, ty)
TheWorld:PushEvent("ms_setsnowlevel", TheWorld.state.snowlevel + .5)		--调整地面积雪覆盖程度
TheWorld.Map:SetFromString(savedata.map.tiles)								--设置世界瓷砖信息
TheWorld.Map:ResetVisited() 												--复位【？】
TheWorld.Map:SetPhysicsWallDistance(0) 
TheWorld.Map:Finalize(0)													--客户端执行后可以更新世界地皮
TheWorld.Map:GetSize()														--获取地图大小  450  450
TheWorld.Map:SetSize(450,450)												--设置地图大小(重启会崩)
			◆0.0


	◆1.0	◆1.1	◆0.1


			◆2.2

坐标-2,0,-2   瓷砖为193,193	计算公式【(193 * 4 + 2) * -1】 为地图最大坐标瓷砖点 -774,0,-774【0,0瓷砖点】 
地图最大面积为【193*2】386,386
local mrx, mry = TheWorld.Map:GetTileCoordsAtPoint(0,0,0) 
local tx, ty = TheWorld.Map:GetTileCoordsAtPoint(ConsoleWorldPosition():Get()) 
local sx, sy = ( tx - mrx ) * 4, ( ty - mry ) * 4 
c_announce(sx.." <= X | Y => "..sy)
-----------
        save.map.prefab = ground.worldprefab
        save.map.tiles = ground.Map:GetStringEncode()
        save.map.nav = ground.Map:GetNavStringEncode()
        save.map.width, save.map.height = ground.Map:GetSize()
        save.map.topology = ground.topology
        save.map.generated = ground.generated
        save.map.persistdata, new_refs = ground:GetPersistData()
        save.meta = ground.meta
        save.map.hideminimap = ground.hideminimap
---------------------------------------------------------客户端部分
													--离开场景
														--回到场景
								--客户端时间轴速度调整
					--地图无法探索记录，并且清除探索过的迷雾
												--开启【退格键】功能
TheSim:SetRenderPassDefaultEffect( RENDERPASS.BLOOM, "shaders/anim_bloom.ksh" )	--设置渲染默认效果
TheSim:SetErosionTexture( "images/erosion.tex" )								--设置侵蚀的纹理
																	--退出客户端【关闭】Shutdown()
TheSim:LoadFont(v.filename, v.alias)											--读取字体
TheSim:SetupFontFallbacks(v.alias, v.fallback)									--安装字体【？】
TheSim:AdjustFontAdvance(v.alias, v.adjustadvance)								--调整字体【？】
TheSim:UnloadFont(v.alias)														--卸载字体
									--关闭mod	遍历ModManager.mods	if v.modinfo.id == "名字"
inst:SetCameraDistance()														--设置相机的距离，拉近，拉远 【无参数 = 默认， 参数 =12  拉近】
					--发送远程控制台指令
TheNet:SendRemoteExecute(fnstr, x, z)
local maxw, maxh = TheSim:GetScreenSize()										--获取句柄大小 w=宽 h=高	1960 x 1280
inst:FacePoint(Point(x,y,z))													--面向点
local angle = inst.Transform:GetRotation()										--获取实体的面向角度   0-180   正负
local dsq = distsq(hp, pt)														--获取目标之间的距离
if TheWorld:HasTag("cave") then													--世界是否有"洞穴"标签
inst:GetDisplayName()															--获取玩家名字
inst.Network:GetUserID()														--获取玩家ID
if not inst:HasTag("burnt") then												-- 如果不是烧坏的
if not inst.sg:HasStateTag("idle") then											-- 如果不是【空闲】状态
if not inst.sg:HasStateTag("moving") then										-- 如果不是【移动】状态
local inst = inst.components.stackable:Get()									-- 从堆叠中获得一个
inst.components.inventoryitem:GetGrandOwner()									-- 获取物品的宿主
inst:ScreenFade(false, 2)														-- 黑屏效果   2秒渐变
inst:ScreenFade(true, .5)														-- 黑屏恢复   .5秒渐变
inst:EnableCameraFocus(true)													--设置为相机的焦点
																	--隐藏地图（战争迷雾全部遮盖）
TheWorld.meta.session_identifier												--服务器存档目录 6ADQ6ZXCFQWASD 文件夹  
								--客户端时间轴速度调整
local pos = TheInput:GetScreenPosition()										--获取指针在屏幕上的像素坐标  pos.x   pos.y
local a = TheInput:AddKeyDownHandler(GLOBAL.KEY_F2, function() end)				--监听按键按下
local a = TheInput:AddKeyUpHandler(GLOBAL.KEY_F2, function() end)				--监听按键弹起
local a = TheInput:AddTextInputHandler(fn)										--监听文本输入
local a = TheInput:AddKeyHandler(fn)											--监听任意按键
																				--移除监听
if a ~= nil then
	a:Remove()
	a = nil
end
a.fn = function() end															--重构功能
self.aa:RemoveHandler(a)														--移除监听
-----------------------------------------HUD-----------------------------------------
ThePlayer.HUD.controls.crafttabs:Hide()											--制作栏
ThePlayer.HUD.controls.inv:Hide()												--道具栏
ThePlayer.HUD.controls.containerroot_side:Hide()								--背包栏
ThePlayer.HUD.controls.item_notification:Hide()									--未知

if type(str) == "number" then													--判断变量是数字
if type(str) == "table" then													--判断变量是表
if type(str) == "string" then													--判断变量是字符串
if type(str) == "function" then													--判断变量是函数

local mubiao = FindEntity(inst, radius, fn, musttags, canttags, mustoneoftags) -- 获取最近的一个目标
--【目标单位{内部自动获取目标坐标}】【范围】【fn(v[被搜索的目标变量],inst[自身目标变量])判定true或fales{ nil为真 }】
--【必须同时有1和2标签，可以nil】【不能有3或4标签，可以nil】【至少有一个标签5或者6，可以nil】

AI    RunAway(self.inst, { fn = ShouldKite, tags = { "_combat", "_health" }, notags = { "INLIMBO" } }, 3, 5)),
--[自己]◆[table=={FindEntity(自己,3,fn,{tags},{notags},{oneoftags})}]◆最小搜索范围◆逃跑距离

----------------------------------------- 掉落模块
inst:AddComponent("locomotor")
inst.components.lootdropper.numrandomloot = nil           
inst.components.lootdropper.chanceloot = nil
inst.components.lootdropper.chanceloottable = nil
inst.components.lootdropper.ifnotchanceloot = nil
inst.components.lootdropper.loot = nil

inst.components.lootdropper.loot = {"","",""}
inst.components.lootdropper:AddRandomLoot(nil, 5)
inst.components.lootdropper:AddRandomLoot("carrot", 10)
inst.components.lootdropper:AddRandomLoot("meat", 10)
inst.components.lootdropper:AddRandomLoot("manrabbit_tail", 1)
inst.components.lootdropper.numrandomloot = 1
------------------------------------------- 赋名模块
inst:AddTag("_named")
inst:AddComponent("named")
inst.components.named.possiblenames = {"11","22"}
inst.components.named:PickNewName()

inst.components.named:SetName("111")
inst.replica.named:SetName("111")
STRINGS.NAMES[string.upper(inst.prefab)]
------------------------------------------- 生存天数 模块
if inst.components.age:GetAgeInDays() > 39 then								--如果玩家生存天数 大于 39天
GetPlayer().Network:SetPlayerAge(100)										--生存天数设置100天 【伪显示】
GetPlayer().components.age.saved_age = GetPlayer().components.age.saved_age + 16*30*5000		--生存天数增加5000天

------------------------------------------- 熔炉复活模块
inst:AddComponent("revivablecorpse")										--死后有尸体
inst:AddComponent("spectatorcorpse")										--有此组件可以执行救治复活

ThePlayer:AddComponent("revivablecorpse") 
ThePlayer:AddComponent("spectatorcorpse") 

local ex_fns = require "prefabs/player_common_extensions" 
ThePlayer:ListenForEvent("respawnfromcorpse", ex_fns.OnRespawnFromPlayerCorpse) 
ThePlayer:PushEvent("respawnfromcorpse", { source = reviver, user = reviver })




-------------------------------------------Widget---------------------------------------------
Widget:IsDeepestFocus()										--是否被指针聚焦【如果焦点在子实体上，返回false】		返回值true
Widget:OnMouseButton(button, down, x, y)					--在被点击时候调用
Widget:MoveToBack()											--搬到底层
Widget:MoveToFront()										--搬到前段
Widget:OnFocusMove(dir, down)								--在被指针聚焦时调用
Widget:IsVisible()											--是否为显示状态
Widget:OnRawKey(key, down)									--在被聚焦时候，按键行为fn
Widget:OnTextInput(text)									--在被输入字符串时候调用
Widget:ScaleTo(from, to, time, fn)							--变换大小【动画】【指定从大小，变换到大小，时间，完成后调用【可nil】】
Widget:MoveTo(from, to, time, fn)							--移动位置【动画】【指定从位置，移动到位置，时间，完成后调用【可nil】】
Widget:CancelMoveTo(run_complete_fn)						--|取消移动【可nil】
Widget:TintTo(from, to, time, fn)							--变换颜色【动画】
Widget:ForceStartWallUpdating()								--强制启动动画完成之前的设定
Widget:ForceStopWallUpdating()								--强制停止动画效果
Widget:GetParent()											--获取父体
Widget:GetChildren()										--获取子表 返回 {}
Widget:RemoveChild(child)									--删除指定子体
Widget:KillAllChildren()									--删除全部子体
Widget:AddChild(child)										--增加指定子体
Widget:Hide()												--实体显示
Widget:OnHide()												--在实体被显示时候调用
Widget:Show()												--实体隐藏
Widget:OnShow()												--在实体被隐藏时候调用
Widget:Kill()												--删除自己
Widget:GetWorldPosition()									--获取在世界上的坐标
Widget:GetPosition()										--获取被附加后的偏移坐标
Widget:GetLocalPosition()									--获取被附加后的偏移坐标【同上，函数功能一模一样】
Widget:Nudge(offset)										--在现有偏移坐标上 + offset坐标
Widget:SetPosition(pos, y, z)								--设置坐标
Widget:UpdatePosition(x, y)									--设置坐标【同上】
Widget:SetRotation(angle)									--设置旋转
Widget:SetScaleMode(mode)									--设置缩放模式【0原始	1满屏	2均衡	3固定比例	4非动态】
Widget:SetScale(pos, y, z)									--设置大小比例【0-1】
Widget:HookCallback(event, fn)								--设置监听事件【self.callbacks[event] = fn】
Widget:SetVAnchor(anchor)									--设置位置【上下便宜  0居中,1顶对齐,2底对齐】
Widget:SetHAnchor(anchor)									--设置位置【左右偏移  0居中,1左对齐,2右对其】
Widget:StartUpdating()										--开启循环更新【:OnUpdate(dt)】
Widget:StopUpdating()										--停止循环更新【:OnUpdate(dt)】
Widget:SetFadeAlpha(alpha, skipChildren)					--设置透明度【参数2，为nil时，子体同步设置】
Widget:SetCanFadeAlpha(fade, skipChildren)					--设置可以被调整透明度【true or false ，true or nil，为nil时，子体同步设置】
Widget:SetClickable(val)									--设置可否被点击【true or false】
Widget:SetOnClick(function() end)							--被点击时调用
Widget:FollowMouse()										--开启跟随指针
Widget:StopFollowMouse()									--停止跟随指针
Widget:GetScale()											--获得大小比例【优先获取父体】	
Widget:GetLooseScale()										--获取大小比例【自己】
Widget:GetDeepestFocus()									--获取被指针聚焦的实体【优先级：子体】
Widget:GetFocusChild()										--获取被指针聚焦的实体【子体】
Widget:ClearFocus()											--取消被聚焦状态【调用self:OnLoseFocus() 和 self.onlosefocusfn()】
Widget:SetFocus()											--设置聚焦状态【调用self:OnGainFocus() 和 self.ongainfocusfn()】
Widget:SetHoverText(text, params)							--设置指针悬停信息
--[[
A:SetHoverText("111",{})						--参数2详细↓
A:ClearHoverText()								--删除悬停信息
{	font		=	DEFAULTFONT,				--悬停文本字体
	size		=	28,							--文本字体大小
	region_h	=	1000,						--设置区域
	region_w	=	40,							--设置区域
	wordwrap	=	true,						--自动换行
	offset_x	=	0,							--坐标偏移
	offset_y	=	0,							--坐标偏移
	colour		=	{1,1,1,1},					--设置色彩
	bg		=	true,							--悬停开启背景框  false为不启用
	bg_atlas	=	"images/frontend.xml",		--设置xml
	bg_texture	=	"scribble_black.tex",		--设置tex
}
]]
--删除悬停信息
--剪切图层
--例：
--血条缩减效果


TheFrontEnd													--scripts\frontend.lua		句柄屏幕控制器
TheFrontEnd:GetFocusWidget()								--获取指针焦点下的Widget
TheFrontEnd:GetHUDScale()									--获取焦点装置的大小【？】
TheFrontEnd:SetFadeLevel(alpha, time, time_total)			--屏幕透明度调整
TheFrontEnd:PushScreen(screen)								--推动显示 local a = require "widgets/zongkong" TheFrontEnd:PushScreen(a)

--------------------------------------------------Text-----------------------------------------------------------
self:AddChild(Text(DEFAULTFONT, 25, "1111" or nil))
DEFAULTFONT												--默认字体(小描边，字体和数字和符号自动转化全角)
DIALOGFONT												--对话框字体
TITLEFONT												--标题字体
UIFONT													--界面字体
BUTTONFONT												--按钮字体(无描边，数字比汉字高)
NEWFONT													--新字体(无描边)
NEWFONT_SMALL
NEWFONT_OUTLINE
NEWFONT_OUTLINE_SMALL
NUMBERFONT												--数字体(有描边)
TALKINGFONT
SMALLNUMBERFONT											--小字体(有描边,数字略模糊)
BODYTEXTFONT
CODEFONT

Text:SetColour(r, g, b, a)								--设置字体颜色
Text:GetColour()										--获取字体颜色 local r, g, b, a
Text:SetHorizontalSqueeze(squeeze)						--挤压【0-1】
Text:SetFadeAlpha(a, skipChildren)						--设置透明度【最后 * a】
Text:SetAlpha(a)										--指定透明度
Text:SetFont(font)										--设置字体库
Text:SetSize(sz)										--设置字体大小
Text:SetRegionSize(w,h)									--设置区域大小【像素级】
Text:GetRegionSize()									--获取区域大小【没被指定时，会自动计算字符串总大小】
Text:SetString(str)										--设置显示字符串
Text:GetString()										--获取被设置的字符串  返回 ""
Text:SetTruncatedString(str, maxwidth, maxchars, ellipses)		--设置最大字符串字数【字符串，最大区域长度，最大字数，true or "..."】
Text:SetVAlign(anchor)									--字体上下对齐【】
Text:SetHAlign(anchor)									--字体左右对齐【ANCHOR_LEFT=左】
Text:EnableWordWrap(enable)								--设置自动换行【true】
Text:EnableWhitespaceWrap(enable)						--启用“空格换行”	【true】

----------------------------------------------TextEdit----------------------------------------------
self:AddChild( TextEdit( DEFAULTFONT, 25, "" ) )
TextEdit:SetIdleTextColour(r,g,b,a)						--设置非输入状态时的字体颜色
TextEdit:SetEditTextColour(r,g,b,a)						--设置在输入状态时的字体颜色
TextEdit:SetEditCursorColour(r,g,b,a)					--设置光标的颜色
TextEdit:SetString(str)									--指定字符串
TextEdit:SetAllowNewline(allow_newline)					--允许换行【true】
TextEdit:SetForceEdit(true)								--设置“正在编辑”状态 【true】
TextEdit:SetEditing(true)								--设置“能被编辑”状态 【true】
TextEdit:OnMouseButton(button, down, x, y)				--在点击时调用
TextEdit:ValidateChar(text)								--验证字符串【？】
TextEdit:ValidatedString(str)							--过滤掉【？】
TextEdit:SetCharacterFilter("1234567890")				--输入限制【仅限此类字符串】
TextEdit:EnableScrollEditWindow(true)					--滚动编辑窗口
TextEdit:SetPassControlToScreen(CONTROL_CANCEL, true)	--设置传递控制到屏幕[输入时，按键在游戏内有操作行为]
TextEdit.OnStopForceEdit = function() self:Close() end	--在停止编辑后调用
TextEdit:EnableRegionSizeLimit(enable)					--是否开启区域限制【默认false】

----------------------------------------------Image-------------------------------------------------------
self:AddChild( Image("images/textboxes.xml", "textbox_long.tex") )
Image:SetAlphaRange(min, max)							--设置可以被透明的最小和最大值
Image:SetTexture("images/textboxes.xml", "textbox_long.tex")		--设定成像
Image:SetMouseOverTexture(atlas, tex)					--设置指针悬停时的图像
Image:SetDisabledTexture(atlas, tex)					--设置禁用时的图像
Image:SetSize(w,h)										--设置图像大小比例
Image:GetSize()											--获取图像大小比例
Image:ScaleToSize(w, h)									--按设定像素 / 原始大小比例
Image:SetTint(r,g,b,a)									--设置颜色覆盖
Image:SetFadeAlpha(a, skipChildren)						--按比例设置透明度
Image:SetVRegPoint(anchor)
Image:SetHRegPoint(anchor)
Image:SetUVScale(xScale, yScale)
Image:SetBlendMode(BLENDMODE.Additive)					--设置混合模式（0-6）


---------------------------------------------饥荒表情包
牙齿		:faketeeth:			|??|
便便		:poop:				|??|
箱子		:chest:				|??|
农场		:farm:				|??|
小切		:chester:			|??|
墓碑		:grave:				|??|
幽灵		:ghost:				|??|
爱心		:heart:				|??|
火焰		:fire:				|??|
火腿棍		:hambat:			|??|
灯泡		:lightbulb:			|??|
烹饪锅		:crockpot:			|??|
猪头		:pig:				|??|
大脑		:sanity:			|??|
科技		:sciencemachine:	|??|
红宝石		:redgem:			|??|
蜘蛛网		:wed:				|??|
牛头		:beefalo:			|??|
锤子		:hammer:			|??|
饥肠		:hunger:			|??|
骷髅		:skull:				|??|
高顶帽		:tophat:			|??|
红骷髅		:arcane:			|??|
巨鹿眼		:eyeball:			|??|
双剑							|??|
火把							|??|
金块							|??|
胳膊							|??|
----------------------------------------------------TheNet数据
TheNet:Kick(UserToClientID(params.user), TUNING.VOTE_KICK_TIME or nil)			--踢掉指定玩家
TheNet:Ban(clientid)																			--ban掉指定玩家
TheNet:BanForTime(clientid, seconds)															--ban掉指定玩家，多久时间
---------------------ban掉某位玩家【限时】
local na = {"","","",""} 
for k,v in pairs(TheNet:GetClientTable()) do 
	if v and table.contains(na,v.name) then 
		print(v.name,"\t",v.userid) 
		TheNet:BanForTime(v.userid, 60*10) 
	end 
end 
----------------------
TheNet:GetPVPEnabled()												-- 是否开启PVP
if TheNet:GetIsServer() then										--判定是否为专用服务器（和TheWorld.ismastersim）
if TheNet:GetIsClient() then										--判定是否为客户端（和not TheWorld.ismastersim功能一样）
if TheNet:IsDedicated() then										--判定是否为[不是](专用服务器)
if GetWorld():IsCave() then											--是否是洞穴世界
TheNet:Announce("1",AllPlayers[1].entity,nil,"mod")					--公告
"vote" 					= 踢人
leave_game 				= 离开游戏
join_game  				= 加入游戏
death      				= 死亡幽灵图标
resurrect  				= 复活
"mod"      				= 人脸面具
kicked_from_game  		= 踢人【脚丫】
banned_from_game		= ban人【锤子】
dice_roll				= 骰子
TheNet:Kick(inst.userid)											--踢掉指定玩家
local tabl = TheNet:GetClientTable()								--获得客户表
TheNet:GetClientTableForUser(inst.userid)							--获取玩家的客户表
if v.performance == nil or TheNet:GetServerIsClientHosted() then	--获取服务器是客户端托管的
TheNet:Say("111111", true, false)									--聊天框右边显示  第2个true，无冒号，    false时  带冒号
TheNet:GetServerGameMode()											--获取服务器游戏模式
TheNet:Talker("11111", inst.entity)									--玩家"头上冒字" 白色字
TheNet:GetServerName()												-- 获取服务器名字
TheNet:GetServerMaxPlayers()										-- 获取服务器最大玩家数      【服务器开放的最大人数上限】
TheNet:GetServerHasPassword()										-- 获取服务器密码
TheNet:GetServerHasPresentAdmin()									-- 获取服务器是否有管理
TheNet:GetServerModsEnabled()										-- 获取服务器mods启用
(TheNet:GetServerClanID() ~= "" and "CLAN")							-- 获得服务器族标识
if TheNet:GetServerGameMode() == "lavaarena" then					-- 获得服务器模式
TheNet:IsOnlineMode()												-- 获得服务器是否为“在线模式”  + not 为“离线模式” 
TheNet:GetServerClanAdmins()										-- 获得服务器家族的管理员
TheNet:GetUserID()													-- 获取服务器的ID
TheNet:DoneLoadingMap()												-- 完成加载地图
TheNet:GetServerModNames()											-- 获取服务器开启的mods的名称
TheNet:ServerModSetup(product_id)									-- 服务器安装mods模块
TheNet:ServerModCollectionSetup(collection_id)						-- ？？？？
TheNet:SetServerTags(BuildTagsStringCommon(tagsTable))				-- 设置服务器标签
TheNet:GetDefaultServerName()										-- 获得服务器默认名字
TheNet:GetDefaultServerPassword()									-- 获得服务器默认密码
TheNet:GetDefaultServerDescription()								-- 获得服务器默认描述
TheNet:GetDefaultClanID()											-- 获得服务器默认ID  ？？？
TheNet:GetDefaultClanAdmins()										-- 获得服务器默认管理员列表
TheNet:GetLocalUserName()											-- 获取服务器角色名字 [host]
TheNet:DeserializeLocalUserSessionMinimap()							-- 清楚地图  【未知】
TheNet:SetIsClientInWorld(inst.userid, true)						-- 设置世界组成员  true  false    【未知】
TheShard:GetShardId() == "2"										-- 获取当前世界ID
GLOBAL.DeleteUserSession(player)									-- 重生时清理玩家数据TheNet:DeleteUserSession(player.userid)
GLOBAL.SerializeUserSession(player)									-- 把玩家数据保存
GLOBAL.TheShard:StartMigration(player.userid, 1) 					-- 强制迁移玩家去1世界【但不会进行修正数据】
if not TheShard:IsSlave() then										-- 不是从属世界
if TheShard:IsMaster() then											-- 是主世界
local str = TheWorld.GroundCreep:GetAsString()						-- 获取瓷砖字符串
TheWorld.GroundCreep:SetFromString(str)								-- 设置瓷砖字符串
TheWorld.Map:ResetVisited()											-- 复位
TheWorld.Map:SetPhysicsWallDistance(0.75)--0) -- TEMP for STREAM		-- 设置物理墙的检测距离
TheWorld.Map:Finalize(1)											-- 地图完成
TheWorld.Map:SetNavFromString(savedata.map.nav)						-- 设置巡径导航

													-- 沙箱中运行
AddModRPCHandler("qm_jn", "shifa", function(player,biaoji,x,z,target,tal)	end)	--RPC预设
SendModRPCToServer(GLOBAL.MOD_RPC["qm_jn"]["shifa"],"F2",x,z,nil,talb)			--RPC发送

TheSim:QueryServer
if TheSim:WorldPointInPoly(x, z, node.poly) then					
---------------------------------------------------------特殊事件监听
inst:ListenForEvent("animover", inst.Remove)						-- 监听动画结束后
inst:ListenForEvent("onremove", inst.Jomr)							-- 监听删除时
inst:ListenForEvent("onbuilt", onbuilt)								-- 监听在建造后触发
inst:ListenForEvent("clocktick", function()  end, TheWorld)			-- 监听时钟 （附加判定黑天白天）
inst:ListenForEvent("death", function()  end)						-- 监听死亡触发
inst:ListenForEvent("freeze", function()  end)						-- 监听冻结触发
inst:ListenForEvent("attacked", function()  end)					-- 监听被击触发
inst:StopWatchingWorldState("isday", OnIsDay)						-- 停止监听世界（天明）
inst:WatchWorldState("isday", ToggleUpdate)							-- 监听世界（天明）
inst:WatchWorldState("isnight", OnIsNight)							-- 监听世界（入夜）
inst:WatchWorldState("isnight", OnIsNight)
inst:WatchWorldState("isnight", OnIsNight)
inst:WatchWorldState("isfullmoon", OnToggleWere)					-- 监听世界（月圆）
inst:WatchWorldState("isautumn", OnAutumn)							-- 监听世界（入秋）
inst:WatchWorldState("israining", OnIsRaining)						-- 监听世界（下雨）
inst:ListenForEvent("killed", function() end)						-- 监听杀死目标 
TheWorld:PushEvent("ms_setclocksegs", {day=a,dusk=b,night=c})		-- 推动世界事件
inst:ListenForEvent("qm_xjjl", function(world, j) julifn(inst, j) end, TheWorld)	-- 监听世界时间

inst.entity:AddMiniMapEntity()
inst.MiniMapEntity:SetIcon(name..".png")
inst.MiniMapEntity:SetPriority(10)
inst.MiniMapEntity:SetCanUseCache(false)
inst.MiniMapEntity:SetDrawOverFogOfWar(true)
----------------------------------------------------Mod部分函数API
AddStategraphPostInit("wilson", function(sg)						--玩家.sg
AddPlayerPostInit(function(inst) 									--所有玩家
AddPrefabPostInitAny(function(inst)									--所有预设物
AddPrefabPostInit("abigail",function(inst)							--预设物
AddComponentPostInit("health", function(self, inst)					--模块
AddClassPostConstruct("widgets/customizationtab", function(self)	--类
------------------------------------------------------------------

----------------------------------------------------------各类计算公式
														--提高100%效果
-----
									--限界75%后递减  110%

------------

-----------

-----------

------------------------------------------------------------字符串相关




-----------------------------
魔法字符
.(点): 与任何字符配对
%a: 与任何字母配对
%c: 与任何控制符配对(例如\n)
%d: 与任何数字配对
%l: 与任何小写字母配对
%p: 与任何标点(punctuation)配对
%s: 与空白字符配对
%u: 与任何大写字母配对
%w: 与任何字母/数字配对
%x: 与任何十六进制数配对
%z: 与任何代表0的字符配对
%x(此处x是非字母非数字字符): 与字符x配对. 主要用来处理表达式中有功能的字符(^$()%.[]*+-?)的配对问题, 例如%%与%配对
[数个字符类]: 与任何[]中包含的字符类配对. 例如[%w_]与任何字母/数字, 或下划线符号(_)配对
[^数个字符类]: 与任何不包含在[]中的字符类配对. 例如[^%s]与任何非空白字符配对

+      匹配前一字符1次或多次
*      匹配前一字符0次或多次
-      匹配前一字符0次或多次
?      匹配前一字符0次或1次

'+'，匹配一个或多个字符，总是进行最长的匹配。比如，模式串 '%a+' 匹配一个或多个字母或者一个单词：


'*' 与 '+' 类似，但是他匹配一个字符0次或多次出现.一个典型的应用是匹配空白。
比如，为了匹配一对圆括号()或者括号之间的空白，可以使用 '%(%s*%)'。（ '%s*' 用来匹配0个或多个空白。由于圆括号在模式中有特殊的含义，
所以我们必须使用 '%' 转义他。）再看一个例子，'[_%a][_%w]*' 匹配Lua程序中的标示符：字母或者下划线开头的字母下划线数字序列。
'-' 与 '*' 一样，都匹配一个字符的0次或多次出现，但是他进行的是最短匹配。某些时候这两个用起来没有区别，但有些时候结果将截然不同。
比如，如果你使用模式 '[_%a][_%w]-' 来查找标示符，你将只能找到第一个字母，因为 '[_%w]-' 永远匹配空。另一方面，假定你想查找C程序中的注释，
很多人可能使用 '/%*.*%*/'（也就是说 "/*" 后面跟着任意多个字符，然后跟着 "*/" ）。然而，由于 '.*' 进行的是最长匹配，
这个模式将匹配程序中第一个 "/*" 和最后一个 "*/" 之间所有部分：

test = "int x; /* x */ int y; /* y */"
print(string.gsub(test, "/%*.*%*/", "<COMMENT>"))
    --> int x; <COMMENT>
	
test = "int x; /* x */ int y; /* y */"
print(string.gsub(test, "/%*.-%*/", "<COMMENT>"))
    --> int x; <COMMENT> int y; <COMMENT>
---------------------------------------------------------------解析数据
self.item = "opalpreciousgem"
if STRINGS.CHARACTER_NAMES[self.item] then
	local character_item = "skull_"..self.item
	itematlas = DEFAULT_ATLAS
	itemimage = character_item .. ".tex"
elseif AllRecipes[self.item] and AllRecipes[self.item].atlas and AllRecipes[self.item].image then
			itematlas = AllRecipes[self.item].atlas
			itemimage = AllRecipes[self.item].image
elseif PREFABDEFINITIONS[self.item] then
	for _,asset in ipairs(PREFABDEFINITIONS[self.item].assets) do
		if asset.type == "INV_IMAGE" then
			itemimage = asset.file..'.tex'
		elseif asset.type == "ATLAS" then
			itematlas = asset.file
		end
	end
end
------
if PREFABDEFINITIONS["xtsp"] then 
	for k,v in pairs(PREFABDEFINITIONS["xtsp"].assets) do 
		if v.type == "IMAGE" then 
			local itemimage = v.file 
			print(itemimage) 
		elseif v.type == "ATLAS" then 
			local itematlas = v.file 
			print(itematlas) 
		end 
	end 
end
-----------------------------------------------------------------------添加行为
SCENE = --args: inst, doer, actions, right					--场景
USEITEM = --args: inst, doer, target, actions, right		--使用项目
POINT = --args: inst, doer, pos, actions, right				--地面
EQUIPPED = --args: inst, doer, target, actions, right		--装备
INVENTORY = --args: inst, doer, actions, right				--库存
ISVALID = --args: inst, action, right						--是有效的


AddAction("QM_XINGWEI", "青木行为实例", function(act)
	if act.doer ~= nil and act.target ~= nil and act.doer:HasTag("player") and act.target.components.fasttravel and not act.target:HasTag("burnt") and not act.target:HasTag("fire") then
		act.target.components.fasttravel:SelectDestination(act.doer)
		return true
	end
end)

AddComponentAction("SCENE", "fasttravel", function(inst, doer, actions, right)
	if right then
		if inst:HasTag(FTSignTag) and not inst:HasTag("burnt") and not inst:HasTag("fire") then
			table.insert(actions, GLOBAL.ACTIONS.DESTINATION)
		end
	end
end)

AddStategraphActionHandler("wilson", GLOBAL.ActionHandler(GLOBAL.ACTIONS.DESTINATION, "give"))
AddStategraphActionHandler("wilson_client", GLOBAL.ActionHandler(GLOBAL.ACTIONS.DESTINATION, "give"))
----------------------
local tp_action = AddAction("SOULMATETP", "传送戒指", function(act)
	if act.invobject and act.invobject.components.soulteleporter then
        return act.invobject.components.soulteleporter:TeleportAction(act.doer)
    end
end)

function SetupTeleportActions(inst, doer, actions)
	table.insert(actions, GLOBAL.ACTIONS.SOULMATETP)
end
AddComponentAction("INVENTORY", "soulteleporter", SetupTeleportActions)
--------------------------------------------滤镜
local bb = { 
	day = "images/colour_cubes/mole_vision_on_cc.tex", 
	dusk = "images/colour_cubes/mole_vision_on_cc.tex", 
	night = "images/colour_cubes/mole_vision_on_cc.tex", 
	full_moon = "images/colour_cubes/mole_vision_on_cc.tex", 
} 
local cc = ThePlayer.components.playervision 
cc:ForceNightVision(true) 
cc:SetCustomCCTable(bb) 
cc:UpdateCCTable() 

local cc = ThePlayer.components.playervision 
cc:ForceNightVision(false) 
cc:SetCustomCCTable(nil) 
cc:UpdateCCTable() 
--------------------------------------------------------AI
require "behaviours/chaseandattack"
require "behaviours/leash"
require "behaviours/wander"
require "behaviours/doaction"
require "behaviours/runaway"

local QM_AI_1 = Class(Brain, function(self, inst)
    Brain._ctor(self, inst)
end)

function QM_AI_1:OnStart()
    local root =
        PriorityNode(
        {
			--循环判定执行
			WhileNode(function()
					return self.inst.components.combat.target ~= nil
						and (self.inst.sg:HasStateTag("running") or
							not self.inst.components.combat.target:IsNear(self.inst, 6))
				end,
				"RamAttack", ChaseAndRam(self.inst, MAX_CHASE_TIME, CHASE_GIVEUP_DIST, MAX_CHARGE_DIST)),
			--逃离(实体,标签 or {fn,tags={},notags={},oneoftags={}}, 判定距离,逃离最大距离,fn(mubiao))
			RunAway(self.inst, "player", MIN_RUNAWAY, MAX_RUNAWAY),
			
			--进攻(实体，最大追逐时间，放弃距离[^2]，最大攻击次数【峰值后会被设置为nil目标】，fn(self.inst)【目标为nil时重新搜索目标】，false or true)
			ChaseAndAttack(self.inst,5,10),
			
			--返回记录点(实体，记录点，最大脱离距离【自动^2】，返回带指定范围内【^2】，true or false【跑步，走步】)
			Leash(self.inst, HomePoint, 20, 10),
		
			--漫步(实体，获取坐标[三维向量]，最大距离，{minwalktime=最小随机时间,randwalktime=随机行走时间,minwaittime=最小等待时间,randwaittime=等待时间, fn=Get方向,fn=Set方向})
			Wander(self.inst, GetNoLeaderHomePos, 20,{
				minwalktime = .5,
				randwalktime = 2,
				minwaittime = 5,
				randwaittime = 10,
    		}),
			--做执行
			ActionNode(function() self.inst.components.combat:SetAttackPeriod(TUNING.ANTLION_MAX_ATTACK_PERIOD) end),
			
			--判定执行
			IfNode(
				function()
					return not self.inst.sg:HasStateTag("busy")
						and FindLeader(self) == nil
				end,
				"No Leader",
				ActionNode(function() self.inst.sg:GoToState("deactivate") end)),
			
			--做行为
			DoAction(self.inst, function() return BaseDestroy(self.inst) end, "DestroyBase", true),
        }, .25)
    self.bt = BT(self.inst, root)
end

function QM_AI_1:OnInitializationComplete()							--AI初始化时调用
	if self.inst.components.knownlocations == nil then
		self.inst:AddComponent("knownlocations")
	end
	if not self.inst.components.knownlocations:GetLocation("qm_yuandian") then
		self.inst.components.knownlocations:RememberLocation("qm_yuandian", self.inst:GetPosition())
	end
end

return QM_AI_1
---------------------------------------------------------------------行为状态
    State{
        name = "pound",
        tags = { "busy" },

        onenter = function(inst)
			inst.components.locomotor:StopMoving()
			inst.sg:SetTimeout(15 * FRAMES)
        end,

        events =
        {
            EventHandler("animover", function(inst)
                if inst.AnimState:AnimDone() then
                    inst.sg:GoToState("pound_post")
                end
            end),
        },

        timeline =
        {
            TimeEvent(2*FRAMES, function(inst)

            end),
        },

        onupdate = function(inst)
		
        end,
		
        ontimeout = function(inst)
            inst.sg:GoToState("idle", true)
        end,
		
        onexit = function(inst)
			inst._DSZS = nil
			inst.Chuanjia = 0
			inst.components.locomotor:Stop()
        end,
		
        ontimeout = function(inst)
            inst.sg:GoToState("idle", true)
        end,
		
    },
-------------------------------------------------------------------Notpepad正则表达式
查找	【--[[][[].*[]][]]】    匹配--[[任意字符]]		单行
查找	--.*]					
查找	^[\t ]*\n					匹配空行
表达式 说明 
/t 制表符. 
/n 新行. 
. 匹配任意字符. 
| 匹配表达式左边和右边的字符. 例如, "ab|bc" 匹配 "ab" 或者 "bc". 
[] 匹配列表之中的任何单个字符. 例如, "[ab]" 匹配 "a" 或者 "b". "[0-9]" 匹配任意数字. 
[^] 匹配列表之外的任何单个字符. 例如, "[^ab]" 匹配 "a" 和 "b" 以外的字符. "[^0-9]" 匹配任意非数字字符. 
* 其左边的字符被匹配任意次(0次，或者多次). 例如 "be*" 匹配 "b", "be" 或者 "bee". 
+ 其左边的字符被匹配至少一次(1次，或者多次). 例如 "be+" 匹配 "be" 或者 "bee" 但是不匹配 "b". 
? 其左边的字符被匹配0次或者1次. 例如 "be?" 匹配 "b" 或者 "be" 但是不匹配 "bee". 
^ 其右边的表达式被匹配在一行的开始. 例如 "^A" 仅仅匹配以 "A" 开头的行. 
$ 其左边的表达式被匹配在一行的结尾. 例如 "e$" 仅仅匹配以 "e" 结尾的行. 
() 影响表达式匹配的顺序，并且用作表达式的分组标记. 
/ 转义字符. 如果你要使用 "/" 本身, 则应该使用 "//". 
---------------------------------------------------------------------打印表

------------------------------------------------------内存优化
											--立马执行一次垃圾回收
												--得到当前应用的当前内存消耗，返回值是用Kb计算的
											--重启垃圾回收功能
	--进行一次垃圾回收迭代。第二个参数值越大，一次迭代的时间越长；如果本次迭代是垃圾回收的最后一次迭代则此函数返回 true
												--停止垃圾回收运行
-----------------------------------------------------------------判定距离差，伤害增益公式
															--优先设定一次最大距离
															--设置增益量
											--判定起始位置
												--判定测试位置
									--获取距离差		差值 = 
			--获取区间差值百分比	0.28125		
									--获取最终增益量  倍的伤害增益【远 = 强】

											--获取最终增益量  倍的伤害增益【近 = 强】
-------------------------------------------------------------------------------------------












