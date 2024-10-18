import carla 
import sys
carla_root = 'D:\Software\Carla\CARLA_0.9.15\WindowsNoEditor\PythonAPI\carla'
sys.path.append(carla_root)

from agents.navigation.global_route_planner import GlobalRoutePlanner # type:ignore


try:
    client = carla.Client("localhost",2000)

except Exception as e:
    print(e)

world = client.get_world()
map = world.get_map()

spawn_points = map.get_spawn_points()
# print(spawn_points)

debug = world.debug

blue_print_lib = world.get_blueprint_library()

# try:
#     vehicle_bp = blue_print_lib.find("vehicle.tesla.cybertruck")
# except IndexError:
#     print('error')

# cybertruck = world.spawn_actor(vehicle_bp, spawn_points[9])

samp_res = 2
try:
    grp = GlobalRoutePlanner(map, samp_res)
except Exception:
    print('damn')

start_point = 98
distination_point = 27

start_loc = spawn_points[start_point].location
dis_loc = spawn_points[distination_point].location

way_points = grp.trace_route(start_loc,dis_loc)

for this_wp, _ in way_points:
    world.debug.draw_string(this_wp.transform.location,'O',draw_shadow=False, color=carla.Color(0,0,225), life_time = 10)