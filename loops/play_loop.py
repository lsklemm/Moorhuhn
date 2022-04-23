import sys
import time

from settings.buttons import*
from settings.timer import Timer
from objects_imports import *


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

    while running:
        screen.fill((90,100,45))
        screen.blit(bg1, background1)
        screen.blit(bg2, background2)
        screen.blit(bg3, background3)

        # Returns milliseconds between each call to 'tick'. The convert time to seconds
        dt = clock.tick(60)


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
                    return 1
                # reload ammo if it is necessary
                elif event.key == pygame.K_SPACE:
                    if ammo.count < 8:
                        ammo_count = ammo.update(screen, ammo_group)

            # add new CHICKEN on the screen0
            elif event.type == pygame.USEREVENT:
                y1 = randint(50,500)
                chickens_group.add(Chicken(screen, y1))
                chickens_group.add(Chicken(screen, randint(50,500)))

            # if event.type == pygame.USEREVENT + 2000:
            #     print('new big')
            #     #y1 = randint(50,500)
            #     chicken = BigChicken(screen)
            #     chicken.show = True
            #     big_chicken_group.add(chicken)
            #     sounds.big_chicken_pops_up_sound.play()


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



        # updates PUMPKIN state
        pumpkin.update()

        # updates CHICKEN/S state
        chickens_group.draw(screen)
        chickens_group.update(dt)

        # updates SIGN POST
        sign_post.update()

        # shows SCORE progress
        buttons.draw_text(f'Score: {score_manager.return_score()}', 30, 700, 20)

        # updates SCORE progress
        scores_group.update()

        # --------- BIG CHICKEN POP UPS ---------
        big_chick_timer += 1
        if big_chick_timer == 40:
            sounds.big_chicken_pops_up_sound.play()
            x = randint(100, 750)
            big_chicken_group.add(BigChicken(screen, (x, 500)))
            big_chick_timer = -300



        big_chicken_group.update()
        mill.update()

        ammo_group.update(dt,ammo_count)

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

        # draw an image instead of REAL CURSOR
        cursor_group.draw(screen)
        cursor_group.update()

        pygame.display.flip()