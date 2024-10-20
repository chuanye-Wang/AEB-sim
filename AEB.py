import carla 
import sys
import time
carla_root = 'D:\Software\Carla\CARLA_0.9.15\WindowsNoEditor\PythonAPI\carla'
sys.path.append(carla_root)

from agents.navigation.global_route_planner import GlobalRoutePlanner # type:ignore
from agents.navigation.controller import VehiclePIDController
from agents.tools.misc import distance_vehicle
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

try:
    vehicle_bp = blue_print_lib.find("vehicle.tesla.cybertruck")
except IndexError:
    print('error')

cybertruck = world.spawn_actor(vehicle_bp, spawn_points[98])

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
    
#args_lateral_dict = {'K_P': 1.95, 'K_I': 0.05, 'K_D': 0.2, 'dt': 0.05}
args_lateral_dict = {'K_P': 1.95,'K_D': 0.2,'K_I': 0.07,'dt': 1.0 / 10.0}

#args_long_dict = {'K_P': 1.0, 'K_I': 0.05, 'K_D': 0, 'dt': 0.05}
args_long_dict = {'K_P': 1,'K_D': 0.0,'K_I': 0.75,'dt': 1.0 / 10.0}
controller = VehiclePIDController(cybertruck, args_lateral_dict, args_long_dict)

speed = 30
next_waypoint = way_points[1][0]
index = 1

try:
    for pi,pj in zip(way_points[:-1], way_points[1:]):
        pi_loc = pi[0].transform.location
        pj_loc = pj[0].transform.location
        debug.draw_line(pi_loc, pj_loc, thickness=0.3, color=carla.Color(0,0,225), life_time=50)


    while(True):
        ego_transform = cybertruck.get_transform()
        control = controller.run_step(speed, next_waypoint)
        dis_to_next_waypoint = distance_vehicle(next_waypoint, ego_transform)
        cybertruck.apply_control(control)

        if dis_to_next_waypoint < 1.5:
            index += 1
            next_waypoint = way_points[index][0]
        
        if index == len(way_points) - 1:
            break


finally:
    cybertruck.destroy()

