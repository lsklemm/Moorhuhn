import sys
import time

import pygame.event

from settings.buttons import*
from settings.timer import Timer
from objects_imports import *
from objects.background import *
from objects.trees import *


from random import randint
from objects.background import *

# PLAY mode
def play_loop(clock, screen, sounds, buttons, cursor, cursor_group, chickens_group, ammo, ammo_group, score_manager, scores_group, pumpkin, sign_post, big_chicken_group, mill):

    # background SOUND
    sounds.play_background.play(-1)

    # to check that we are still playing
    running = True
    # to check last 10 sec of the PLAY
    timer = Timer()

    # turn off the image of the REAL 'CURSOR'
    pygame.mouse.set_visible(False)

    # initialize time value
    # to know if we have to start counting time
    init_time = 0

    big_chick_timer = 0

    ammo_count = -1

    tree1 = Tree(screen, 'img/tree/trunkBig1.png', 300, 200)
    tree2 = Tree(screen, 'img/tree/trunkSmall1.png',1900, 100)
    camera1 = Camera(0,0)
    camera2 = Camera(0, 100)
    camera3 = Camera(0, 150)


    running = True
    while running:
        dt = clock.tick(60)
        # for screen moving
        cursor_x = cursor.rect.x
        if cursor_x >= 750 and cursor_x <= 800:
            # obj = []
            # obj.append(chickens_group, big_chicken_group, mill, pumpkin, sign_post)
            # camera1.move(50)
            # camera2.move(50)
            # camera3.move(50)
            if camera1.move(50) and camera2.move(50) and camera3.move(50):
                chickens_group.update(dt, 'move_r')
                big_chicken_group.update('move_r')

                mill.update('move_r')
                pumpkin.update('move_r')
                sign_post.update('move_r')
                tree1.update('move_r')
                tree2.update('move_r')

        elif cursor_x <= 20 and cursor_x >= -20:

            # camera2.move(-50)
            # camera3.move(-50)
            if camera1.move(-50) and camera2.move(-50) and camera3.move(-50):
                chickens_group.update(dt, 'move_l')
                big_chicken_group.update('move_l')

                mill.update('move_l')
                pumpkin.update('move_l')
                sign_post.update('move_l')
                tree1.update('move_l')
                tree2.update('move_l')
        # else:
        #     pumpkin.update('no')
        #
        #     chickens_group.update(dt, 'no')
        #
        #     # updates SIGN POST
        #     sign_post.update('no')
        #     big_chicken_group.update('no')
        #     mill.update('no')

        screen.fill((90,100,45))
        screen.blit(bg1, (-camera1.rect[0], camera1.rect[1]))
        screen.blit(bg2, (-camera2.rect[0], camera2.rect[1]))
        screen.blit(green, (-camera3.rect[0], camera3.rect[1]))

        # Returns milliseconds between each call to 'tick'. The convert time to seconds



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sounds.play_background.stop()
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sounds.play_background.stop()
                    running = False
                    return 1, 0
                # reload ammo if it is necessary
                elif event.key == pygame.K_SPACE:
                    if ammo.count < 8:
                        ammo_count = ammo.update(screen, ammo_group)

            # if event.type == pygame.MOUSEMOTION:




            # add new CHICKEN on the screen0
            elif event.type == pygame.USEREVENT:
                y1 = randint(150,500)
                chickens_group.add(Chicken(screen, y1))
                #chickens_group.add(Chicken(screen, randint(150,500)))




            # checks if we have shot a CHICKEN
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # check for AMMO amount
                check_shot, ammo_count = ammo.shot()
                x, y = event.pos
                # if we shot SIGN POST
                if cursor.shoot_big_chicken(sounds, cursor, big_chicken_group, check_shot, score_manager, scores_group):
                    continue
                    # if we shot the CHICKEN
                elif cursor.shoot_chicken(sounds, chickens_group, check_shot, score_manager, scores_group):
                    break
                elif cursor.shoot_mill(cursor, x, y, sounds, mill, check_shot, score_manager, scores_group):
                    break
                elif cursor.shoot_sign_post(sounds, sign_post, check_shot, score_manager, scores_group):
                    continue
                # if we shot the PUMPKIN MAN
                elif cursor.shoot_pumpkin(sounds, pumpkin, check_shot, score_manager, scores_group):
                    break


        # --------- BIG CHICKEN POP UPS ---------
        big_chick_timer += 1
        if big_chick_timer == 40:
            sounds.big_chicken_pops_up_sound.play()
            x = randint(100, 1700)
            big_chicken_group.add(BigChicken(screen, (x, 450)))
            big_chick_timer = -300



        # --------- COUNT PLAY TIME ---------
        # in purpose to make sure that we start counting only ones
        # when we start the play_loop
        init_time += 1
        if init_time == 1:
            start_time = time.time()
        play_time = round(time.time() - start_time)

        # shows LEFT PLAY TIME
        buttons.draw_text(f'Time: {90 - play_time}', 30, 82, 20)



        # --------- CHECK LEFT TIME ---------
        # if the timer is got down to 0
        play_time_check = timer.time_check(sounds, play_time)
        if play_time_check == 1:
            sounds.play_background.stop()
            sounds.game_over_sound.play()
            running = False
            # go to the BEST SCORE mode
            return 2, score_manager.return_score()


        # --------------- UPDATE -----------------------
        # updates PUMPKIN state
        pumpkin.update('no')



        # update MILL
        mill.update('no')

        # updates FLY CHICKEN/S state
        chickens_group.draw(screen)
        chickens_group.update(dt, 'no')

        # updates SIGN POST
        sign_post.update('no')

        # shows SCORE progress
        buttons.draw_text(f'Score: {score_manager.return_score()}', 30, 700, 20)
        # updates SCORE progress
        scores_group.update()

        tree1.update('no')

        tree2.update('no')

        # update BIG CHICKEN
        big_chicken_group.update('no')

        # update AMMO
        ammo_group.update(dt, ammo_count)


        # draw an image instead of REAL CURSOR
        cursor_group.draw(screen)
        cursor_group.update()

        pygame.display.flip()