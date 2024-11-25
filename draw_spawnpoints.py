import carla
import time

# 连接到CARLA服务器
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)


world = client.get_world()
map = world.get_map()

# 获取地图上的所有 spawn points
spawn_point = map.get_spawn_points()[7]
spawn_points = []
for i in range(100):
    spawn_point = carla.Transform()
    loc = world.get_random_location_from_navigation()  # 获取一个随机的可行走位置
    if (loc != None):
        spawn_point.location = loc
        spawn_points.append(spawn_point)
print(spawn_points)

# 获取世界的调试工具（debugger）
debug = world.debug

# 绘制所有 spawn points
for spawn_point in spawn_points:
    # 使用draw_point方法绘制每个spawn point的位置
    debug.draw_point(spawn_point.location, size=0.1, color=carla.Color(r=255, g=0, b=0), life_time=100)

# 给用户一些时间来查看效果
# time.sleep(5)

print("所有spawn points已被标记。")
