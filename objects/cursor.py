import pygame
import random

from settings.score_manager import ScoreImgManager

# CURSOR class
class Cursor(pygame.sprite.Sprite):
    def __init__(self, screen, img_path):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()

    # updates the position
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    # shot the CHICKEN
    def shoot_chicken(self, sounds, chickens_group, check_shot, score_manager, scores_group):
        for chicken in chickens_group:
            # looking for a shot chicken
            if self.rect.colliderect(chicken.rect) and chicken.alive:
                if check_shot:
                    # add random SHOT CHICKEN SOUND
                    index = random.randint(0, 2)
                    sounds.return_chick_hits(index).play()

                    # update SCORE
                    #scores_group.add(ScoreManager(self.screen))
                    #scores_group.shot(chicken)
                    score1 = ScoreImgManager(self.screen, score_manager)
                    score1.show = True
                    scores_group.add(score1)
                    for score in scores_group:
                        if score.shot:
                            score.shot(chicken)

                    # score.shot(chicken)

                    # CHICKEN is DEAD
                    chicken.alive = False
                    # break
                    return True

    # shot the PUMPKIN MAN
    def shoot_pumpkin(self, sounds, pumpkin, check_shot, score_manager, scores_group):
        # looking for a shot chicken
        if self.rect.colliderect(pumpkin.rect) and pumpkin.alive:
            if check_shot:
                sounds.pumpkin_shot_sound.play()


                # update SCORE
                score1 = ScoreImgManager(self.screen, score_manager)
                scores_group.add(score1)
                score1.show = True
                for score in scores_group:
                    if score.show:
                        score.shot(pumpkin)

                # CHICKEN is DEAD
                pumpkin.alive = False

                # break
                return True

    # shot the SIGN POST
    def shoot_sign_post(self, sounds, sign_post, check_shot, score_manager, scores_group):
        # looking for a shot chicken
        if self.rect.colliderect(sign_post.rect):
            if check_shot:
                #sounds.sign_post_shot_sound.play()

                # update SCORE
                score1 = ScoreImgManager(self.screen, score_manager)
                scores_group.add(score1)
                score1.show = True
                for score in scores_group:
                    if score.show:
                        score.shot(sign_post)

                # shot the SIGH POST
                if sign_post.shot:
                    sign_post.shot = False
                else:
                    sign_post.shot = True

                # break
                return True