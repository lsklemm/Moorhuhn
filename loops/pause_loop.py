import pygame


# PAUSE on PLAY mode
def pause_loop(screen, sounds, buttons, cursor):
    running = True
    # turn off the image of the REAL 'CURSOR'
    pygame.mouse.set_visible(False)

    sounds.main_theme_sound.play(-1)

    bg = pygame.transform.scale(pygame.image.load('img/pause_background/pause.png'), (800,600))
    bg_rect = bg.get_rect()

    while running:
        screen.fill((255, 204, 255))
        screen.blit(bg, bg_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sounds.main_theme_sound.stop()
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons.pause_buttons[0].collidepoint(pygame.mouse.get_pos()):
                    if event.button == 1:
                        sounds.main_theme_sound.stop()
                        sounds.button_click_sound.play()
                        running = False
                        return 1
                elif buttons.pause_buttons[1].collidepoint(pygame.mouse.get_pos()):
                    if event.button == 1:
                        sounds.main_theme_sound.stop()
                        sounds.button_click_sound.play()
                        running = False
                        # set the REAL CURSOR back
                        #pygame.mouse.set_visible(True)
                        return 2


        buttons.draw_pause('Main Menu', 50, 200, 200)
        buttons.draw_pause('Exit', 50, 200, 100)


        # draw an image instead of REAL CURSOR
        # and update its position
        cursor.draw(screen)
        cursor.update()
        pygame.display.flip()