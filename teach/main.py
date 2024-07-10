import pygame


clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Samolet444")
icon = pygame.image.load('images/plane.png')
pygame.display.set_icon(icon)


backround = pygame.image.load('images/backround.png').convert()


walk_left = [
    pygame.image.load('images/gamer/gamer_left/gamer_left1.png').convert_alpha(),
    pygame.image.load('images/gamer/gamer_left/gamer_left2.png').convert_alpha(),
    pygame.image.load('images/gamer/gamer_left/gamer_left3.png').convert_alpha(),
    pygame.image.load('images/gamer/gamer_left/gamer_left4.png').convert_alpha(),

]
walk_right = [
    pygame.image.load('images/gamer/gamer_right/gamer_right1.png').convert_alpha(),
    pygame.image.load('images/gamer/gamer_right/gamer_right2.png').convert_alpha(),
    pygame.image.load('images/gamer/gamer_right/gamer_right3.png').convert_alpha(),
    pygame.image.load('images/gamer/gamer_right/gamer_right4.png').convert_alpha(),

]



foe = pygame.image.load('images/tumbleweed.png').convert_alpha()
#foe_x,y = (1220, 512)
foe_list_in_game = []

gamer_anim_count = 0

backround_x = 0

player_speed = 9
player_x = 400
player_y = 500

jump = False
jump_count = 8

bg_sounds = pygame.mixer.Sound('sounds/bg_volume.mp3')
bg_sounds.play()

foe_timer = pygame.USEREVENT + 1

pygame.time.set_timer(foe_timer, 3000)

lable = pygame.font.Font('fonts/MOSCOW2024.otf', 50)
lose_lable = lable.render('You are very big loser!!))',  False, ('Black'))
restart_lable = lable.render('NEW GAME',  False, ('Blue'))
restart_lable_rect = restart_lable.get_rect(topleft=(470, 300))


bullets_many = 3
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets = []
bullet_dt = pygame.image.load('images/bullet_dt.png').convert_alpha()

gameplay = True

running = True
while running:


    screen.blit(backround, (backround_x, 0))
    screen.blit(backround, (backround_x + 1200, 0))
    screen.blit(bullet_dt, (10, 10))

    if gameplay:


        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if foe_list_in_game:
            for (i, el) in enumerate(foe_list_in_game):
                screen.blit(foe, el)
                el.x -= 20

                if el.x < -10:
                    foe_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[gamer_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[gamer_anim_count], (player_x, player_y))


        if keys[pygame.K_LEFT] and player_x > 20:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 1180:
            player_x += player_speed

        if not jump:
            if keys[pygame.K_SPACE]:
                jump = True
        else:
            if jump_count >=-8:
                if jump_count > 0:
                    player_y -= (jump_count**2)/2
                else:
                    player_y += (jump_count**2)/2
                jump_count -= 1
            else:
                jump = False
                jump_count = 8




        if gamer_anim_count == 3:
            gamer_anim_count = 0
        else:
            gamer_anim_count += 1

        if backround_x == -1200:
            backround_x = 0
        else:
            backround_x -= 8



        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x,  el.y))
                el.x += 4

                if el.x > 1201:
                    bullets.pop(i)

                if foe_list_in_game:
                    for (index, foe_el) in enumerate(foe_list_in_game):
                        if el.colliderect(foe_el):
                            foe_list_in_game.pop(index)
                            bullets.pop(i)

    else:
        screen.fill('Red')
        screen.blit(lose_lable, (260, 250))
        screen.blit(restart_lable, restart_lable_rect)


        mouse = pygame.mouse.get_pos()
        if restart_lable_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] == 1:
            gameplay =True
            player_x = 400
            foe_list_in_game.clear()
            bullets.clear()
            bullets_many = 3

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == foe_timer:
            foe_list_in_game.append(foe.get_rect(topleft=(1220, 519)))

        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_w and bullets_many > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 35)))
            bullets_many -= 1

    clock.tick(8)