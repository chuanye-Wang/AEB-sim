import carla 
import sys
import time
carla_root = 'D:\Software\Carla\CARLA_0.9.15\WindowsNoEditor\PythonAPI\carla'
sys.path.append(carla_root)

from agents.navigation.global_route_planner import GlobalRoutePlanner # type:ignore
from agents.navigation.controller import VehiclePIDController
from agents.tools.misc import distance_vehicle, is_within_distance

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

speed = 40
next_waypoint = way_points[1][0]
index = 1

obs_car_bp = blue_print_lib.find('vehicle.tesla.model3')
obs_car = world.spawn_actor(obs_car_bp, spawn_points[49])

spectator = world.get_spectator()


try:
    for pi,pj in zip(way_points[:-1], way_points[1:]):
        pi_loc = pi[0].transform.location
        pj_loc = pj[0].transform.location
        debug.draw_line(pi_loc, pj_loc, thickness=0.3, color=carla.Color(0,0,225), life_time=50)


    while(True):
        judge = is_within_distance(obs_car.get_transform(), cybertruck.get_transform(), 25, [-50,50])
        if judge:
            control.throttle = 0
            control.brake = 0.5
            control.hand_brake = False
            cybertruck.apply_control(control)
            break

        ego_transform = cybertruck.get_transform()
        control = controller.run_step(speed, next_waypoint)
        dis_to_next_waypoint = distance_vehicle(next_waypoint, ego_transform)
        cybertruck.apply_control(control)

        # spec_transform = carla.Transform(ego_transform.location + carla.Location(x=-0.5,y=-0.3,z=1.8),ego_transform.rotation)
        # spectator.set_transform(spec_transform)

        spec_transform = carla.Transform(ego_transform.location + carla.Location(z=30),carla.Rotation(pitch=-90))
        spectator.set_transform(spec_transform)

        if dis_to_next_waypoint < 1.5:
            index += 1
            next_waypoint = way_points[index][0]
        
        if index == len(way_points) - 1:
            break
        pass

    time.sleep(5)

finally:
    cybertruck.destroy()
    obs_car.destroy()
