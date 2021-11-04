import pygame

from game.characters.charactersSpriteSheetDict import CHAR_SPRITE_SHEET_DICT as CHAR_DICT


class PlayerSprite(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        # Sprite-image management
        self.sprite_sheet = pygame.image.load("./" + CHAR_DICT["main_character"])
        self.make_image(self.get_image(0, 0))
        self.rect = self.image.get_rect()
        self.imagesDict = self.make_image_dict()

        # position management
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * .5, 12)
        self.old_position = self.position.copy()
        self.curr_direction = 'down'
        self.number_steps_curr_direction = 0
        self.moving_speed = 6
    # Sprite-image management

    def make_image_dict(self, x: int = 0):
        imagesDict = {
            'down': self.get_image(x, 0),
            'left': self.get_image(x, 32),
            'right': self.get_image(x, 64),
            'up': self.get_image(x, 96)
        }
        return imagesDict

    def make_image(self, im):
        self.image = im
        self.image.set_colorkey([0, 0, 0])

    def update_direction_sprite(self, direction):
        match self.number_steps_curr_direction % 4:
            case 0:
                return self.make_image(self.make_image_dict(x=0)[direction])
            case 1 | 3:
                return self.make_image(self.make_image_dict(x=32)[direction])
            case 2:
                return self.make_image(self.make_image_dict(x=64)[direction])

    def get_image(self, x: int, y: int) -> pygame.Surface:
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    # position management

    def change_direction(self, direction: str):
        return self.make_image(self.imagesDict[direction])

    def save_location(self):
        self.old_position = self.position.copy()

    def move(self, direction: str):
        if self.curr_direction != direction:
            self.curr_direction = direction
            self.number_steps_curr_direction = 0
            self.change_direction(direction)
        else:
            self.number_steps_curr_direction += 1
            self.update_direction_sprite(direction=direction)

        match direction:
            case "right":
                self.position[0] += self.moving_speed
            case "left":
                self.position[0] -= self.moving_speed
            case "up":
                self.position[1] -= self.moving_speed
            case "down":
                self.position[1] += self.moving_speed
            case _:
                pass

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midtop

    def move_back(self):
        self.position = self.old_position
        self.update()
