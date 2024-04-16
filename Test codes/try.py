import pygame

VELOCITY         = 5
LERP_FACTOR      = 0.1
minimum_distance = 20
maximum_distance = 100

def FollowMe(pops, fpos):
    target_vector       = pygame.math.Vector2(pops)
    follower_vector     = pygame.math.Vector2(fpos)
    new_follower_vector = pygame.math.Vector2(fpos)
    print(target_vector)

    distance = follower_vector.distance_to(target_vector)
    if distance > minimum_distance:
        direction_vector    = (target_vector - follower_vector) / distance
        min_step            = max(0, distance - maximum_distance)
        max_step            = distance - minimum_distance
        # step_distance       = min(max_step, max(min_step, VELOCITY))
        step_distance       = min_step + (max_step - min_step) * LERP_FACTOR
        new_follower_vector = follower_vector + direction_vector * step_distance

    return (new_follower_vector.x, new_follower_vector.y) 



pygame.init()
window = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

lines = [((20, 300), (150, 20)), ((250, 20), (380, 250)), ((50, 350), (350, 300))] 
rect = pygame.Rect(180, 180, 40, 40)
speed = 5

follower = (100, 100)
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    player   = pygame.mouse.get_pos()
    follower = FollowMe(player, follower)

    keys = pygame.key.get_pressed()
    rect.x += (keys[pygame.K_d] - keys[pygame.K_a]) * speed
    rect.y += (keys[pygame.K_s] - keys[pygame.K_w]) * speed

    if any(rect.clipline(*line) for line in lines):
        color = "red"

    else:
        color = "green"


    window.fill(0)  
    pygame.draw.circle(window, color, player, 10)
    pygame.draw.circle(window, (255, 0, 0), (round(follower[0]), round(follower[1])), 10)
    pygame.draw.rect(window, color, rect)
    for line in lines:
        pygame.draw.line(window, "white", *line)
    pygame.display.flip()

pygame.quit()
exit()