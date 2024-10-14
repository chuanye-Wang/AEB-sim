import carla 

try:
    client = carla.Client("localhost",2000)

except Exception as e:
    print(e)

world = client.get_world()
map = world.get_map()

spawn_points = map.get_spawn_points()
# print(spawn_points)

# debug = world.debug

# for i in spawn_points:
#     debug.draw_point(i.location, size=0.5, color=carla.Color(255,255,0), life_time=10)

blue_print_lib = world.get_blueprint_library()

try:
    vehicle_bp = blue_print_lib.find("vehicle.tesla.cybertruck")
except IndexError:
    print('error')

car = world.spawn_actor(vehicle_bp, spawn_points[8])

import time
time.sleep(1)

car.set_autopilot(True)

time.sleep(10)
car.destroy()