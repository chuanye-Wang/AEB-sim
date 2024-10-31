import carla
import random
import time
import pygame

client = carla.Client("localhost", 2000)
client.set_timeout(10.0)
world = client.get_world()

try:
    blueprint_library = world.get_blueprint_library()
    vehicle_blueprint = blueprint_library.find("vehicle.tesla.cybertruck")
    spawn_points = world.get_map().get_spawn_points()
    spawn_point = random.choice(spawn_points)
    vehicle = world.spawn_actor(vehicle_blueprint, spawn_point)

    spectator = world.get_spectator()
    spectator_tf = spectator.get_transform()
    vehicle_transform = vehicle.get_transform() 
    
    spectator_location = carla.Location(
    x=vehicle_transform.location.x,
    y=vehicle_transform.location.y,
    z=vehicle_transform.location.z + 12
    )
    spectator_rotation = carla.Rotation(pitch=-90)

    spectator.set_transform(carla.Transform(spectator_location, spectator_rotation))
#####################################################################################

    pygame.init()
    width = 800
    height = 500
    display = pygame.display.set_mode((width,height))

    # Find the blueprint of the sensor.
    cam_blueprint = world.get_blueprint_library().find('sensor.camera.rgb')
    # Modify the attributes of the blueprint to set image resolution and field of view.
    cam_blueprint.set_attribute('image_size_x', f'{width}')
    cam_blueprint.set_attribute('image_size_y', f'{height}')
    cam_blueprint.set_attribute('fov', '110')
    # Set the time in seconds between sensor captures
    # blueprint.set_attribute('sensor_tick', 0)
    cam_tf = carla.Transform(carla.Location(x=1.5, z=2.4))
    camera_actor = world.spawn_actor(cam_blueprint, cam_tf, attach_to=vehicle)

    import numpy as np
    def py_show(image):
        image_array = np.frombuffer(image.raw_data, dtype=np.uint8)
        image_array = image_array.reshape(image.height,image.width,4)
        image_array = image_array[:,:,:3]
        image_array = image_array[:,:,::-1]
        
        surface = pygame.surfarray.make_surface(image_array.swapaxes(0,1))
        display.blit(surface,(0,0))
        pygame.display.flip()
        pass

    camera_actor.listen(lambda image: py_show(image))

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if(event == pygame.QUIT):
                running = False
        clock.tick(30)

finally:
    camera_actor.stop()
    camera_actor.destroy()
    vehicle.destroy()
    pygame.quit()