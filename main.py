import pygame
from sys import exit

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"Score: {current_time}",False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)

pygame.init()
# creating a screen window with specific dimensions
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0

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

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (600, 300))
# snail_x_pos = 600

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
# rectangles!
# player_rect = pygame.Rect(left,top,width,height) you could do this, but it is uncommon because you want to make it the same
# exact size as your surface. So, we do this...
player_rect = player_surf.get_rect(midbottom = (80,300))
# this draws a rectangle around the surface, then we can give it information on where to be placed
# use topleft, midtop, topright, midleft, midright, bottomleft, midbottom, bottomright, and center to specify which point
# on the rectangle you would like to place and then use the coordinate system to specify where to place that point
player_gravity = 0

# Into Screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

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

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    snail_rect = snail_surface.get_rect(midbottom = (600, 300))
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
        display_score()


        # Snail
        snail_rect.x -= 4
        if snail_rect.right <= 0:
            snail_rect.left = 800
        screen.blit(snail_surface, snail_rect)
        # this could be useful some times for measuring things by seeing exactly where an object is
        # print(player_rect.left)


        # Player
        # this is an easy way to mimic gravity, obviously its not realistic but it's fine, itll look fine
        player_gravity += 1
        player_rect.y += player_gravity
        # important to do this before you draw the character so it is smooth
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        # collision
        if snail_rect.colliderect(player_rect):
            game_active = False
    
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)

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