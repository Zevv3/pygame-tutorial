import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"Score: {current_time}",False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    """
    Takes all the obstacles from list and moves the 5 pixels to the left, returns the new list
    """
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            # move left 5 pixels every frame or whatever
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle_rect.x > -100]
        
        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle in obstacles:
            if player.colliderect(obstacle): return False
    return True

def player_animation():
    """
    play walking animation if player is on floor,
    display jump surface if player is not on floor
    """
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        # slowly increase the index
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()
# creating a screen window with specific dimensions
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

# similar to a display surface, a regular surface requires dimensions 
# Note that to add text, you first have to create an image of the text and then place that on a surface to be displayed
    # creating text:
    # 1. create a font (text size and style)
        # test_font = pygame.font.Font(font type, font size) None for font type will be the default pygame font
    # 2. write text on a surface
        # text_font = test_font.render('text here', anti aliasing (True/False) (false will be pixely, true is smooth), color)
    # 3. blit the text surface
    # above: 
# the convert() method converts the png files into something pygame can work with more easily, increasing perfomance
# if it looks weird, use convert_alpha() method
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
score_surf = test_font.render('My game', False, (64,64,64))
score_rect = score_surf.get_rect(center = (400, 50))

# Obstacles
# snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]
# we dont need this rect anymore now that we have the obstacle_rect
# snail_rect = snail_surf.get_rect(midbottom = (600, 300))
# snail_x_pos = 600

# fly
fly_frame_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
# rectangles!
# player_rect = pygame.Rect(left,top,width,height) you could do this, but it is uncommon because you want to make it the same
# exact size as your surface. So, we do this...
player_rect = player_surf.get_rect(midbottom = (80,300))
# this draws a rectangle around the surface, then we can give it information on where to be placed
# use topleft, midtop, topright, midleft, midright, bottomleft, midbottom, bottomright, and center to specify which point
# on the rectangle you would like to place and then use the coordinate system to specify where to place that point
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
# rotozoom will rotate and zoom... here rotate by 0 degrees, scale x2
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400, 340))

# Timers
# we use userevent+1 because some things (like userevent) are reserved pygame names or something, so here we specify as a different one? yeah i understand this really well (it's in the docs for more info)
obstacle_timer = pygame.USEREVENT + 1
# 900 is .900 seconds (900ms)
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,300)

while True:
    # event loop: checking for possible player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # exit method is a more secure way to break the loop than using a break statement
            exit()
        # This is another way of checking the mouse
        # if event.type == pygame.MOUSEBUTTONUP:
            # print('mouse up')
            # MOUSEBUTTONDOWN does the same, but on the initial press
        # pygame.MOUSEMOTION also works, event.pos is useful for showing the position an event takes place
        # checking if mouse is over player rectangle using the event loop:
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos):
        #         print('collision')
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20
            # checking player input using the event loop gives more control because you check first if any button was pressed, then check which button
            # you can also use KEYUP and there are probably others idk
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
            if event.type == obstacle_timer:
                # randint here will either give 0 or 1, otherwise known as false or true, respectively
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100), 210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    snail_rect = snail_surf.get_rect(midbottom = (600, 300))
                    player_rect = player_surf.get_rect(midbottom = (80,300))
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)
                    

    if game_active:
        # blit stands for bloack image transfer - fancy way to say putthing
        # a surface onto another surface - our regular surface onto the display surface
        # pass in your new surface and the location
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        # drawing with rectangles - pass arguments for surface to draw on, color, then rectangle you want to draw, there are more optional arguments such as width and border radius
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        # drawing a line:
        # pygame.draw.line(screen, 'Gold', (0,0), pygame.mouse.get_pos(), 10)
        # drawing a circle:
        # pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50,200,100,100))
        # screen.blit(score_surf, score_rect)
        # snail_x_pos -= 4
        score = display_score()


        # Snail
        # snail_rect.x -= 4
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surf, snail_rect)
        # this could be useful some times for measuring things by seeing exactly where an object is
        # print(player_rect.left)

        # New Obstacle logic:
        # create a list of obstacle rectangles, everytime the timer triggers, we add a new rectabgle to the list, we move
        # every rectangle in that list to the left on every frame, and we delete rectangles that are too far left



        # Player
        # this is an easy way to mimic gravity, obviously its not realistic but it's fine, itll look fine
        player_gravity += 1
        player_rect.y += player_gravity
        # important to do this before you draw the character so it is smooth
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        # we dont need this with our new obstacle logic
        # if snail_rect.colliderect(player_rect):
        #     game_active = False
        game_active = collisions(player_rect, obstacle_rect_list)
    
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        # resets player position if player jumped on death
        player_rect.midbottom = (800, 300)
        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

    # keys = pygame.key.get_pressed()
    # the documentation has all the codes for all the keys, this is space bar, returns 0 or 1
    # if keys[pygame.K_SPACE]:
    #     print('jump')
    # You can also do this in the event loop




    # colliderect returns either a 0 or a 1
    # 0 if no collision, 1 if collision
    # if player_rect.colliderect(snail_rect):
    #     print('collision')
    # .collidepoint is another pretty important method for using the mouse in game
    # rect1.collidepoint((x,y)) - checks if a position is inside the rectangle
    # how do we get the mouse position? with either pygame.mouse or through the event loop
    # pygame.mouse gives mouse position, clicks, buttons, visibility, etc -> get press and get position
    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint((mouse_pos)):
    #     print(pygame.mouse.get_pressed())




    # Draw all our elements
    # and update everything
    # this method will take the new elements and whatnot and update them on the display
    pygame.display.update()
    # clock.tick(60) sets the max fps to 60
    # for the minimum, you have to just make sure there's never too 
    # much on screen that would slow it down
    clock.tick(60)