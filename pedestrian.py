import carla
import random
import time

def create_walker(world):

    blueprint_library = world.get_blueprint_library()
    walker_bp = random.choice(blueprint_library.filter('walker.pedestrian.*'))
    
    spawn_point = world.get_map().get_spawn_points()[7]

    walker = world.spawn_actor(walker_bp, spawn_point)
    return walker

def control_walker(walker):
    walker_control = carla.WalkerControl()

    walker_control.speed = 1.0
    walker_control.direction = carla.Vector3D(1.0, 1.0, 0.0)  # 控制方向（沿y轴移动）
    
    walker.apply_control(walker_control)
    
    time.sleep(5)


def main():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(10)
        world = client.get_world()

        walker = create_walker(world)

        spec = world.get_spectator()
        spec.set_transform(walker.get_transform()) 
        control_walker(walker)

        time.sleep(5)

    finally:
        print("Cleaning up")
        walker.destroy()

if __name__ == "__main__":
    main()
