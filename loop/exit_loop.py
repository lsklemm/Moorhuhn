import pygame


# EXIT
def exit_loop(screen, cursor_group, buttons):
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # -> back to Main Menu
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return 0


            elif event.type == pygame.MOUSEBUTTONDOWN:
                # EXIT the GAME
                if buttons.exit_buttons[0].collidepoint(pygame.mouse.get_pos()):
                    if event.button == 1:
                        running = False
                        return 1
                # back to Main Menu
                elif buttons.exit_buttons[1].collidepoint(pygame.mouse.get_pos()):
                    if event.button == 1:
                        running = False
                        return 2

        screen.fill((90, 22, 45))
        buttons.draw_text("Are you sure?", 50, 300, 100)
        buttons.draw_exit('Yes', 50, 300, 200)
        buttons.draw_exit('No', 50, 300, 300)

        # draw an image instead of REAL CURSOR
        cursor_group.draw(screen)
        cursor_group.update()

        pygame.display.flip()