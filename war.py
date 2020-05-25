import sys, pygame
import random

red = (255, 0, 0)
black = (0, 0, 0)
suits = (('♥', red), ('♣', black), ('♦', red),('♠', black))
ranks = {11:'J', 12:'Q', 13:'K', 14:'A'}
test = 'awe'

class Button(pygame.sprite.Sprite):
    def __init__(self, text):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100,30))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.text = text
        self.active = 1

        self.image.fill((255,255,255))
        pygame.draw.rect(self.image, (0,0,0), (0,0,100,30), 1)
        n = font_option.render(self.text, True, (0,0,0))
        text_rect = n.get_rect(center=(self.image.get_width()/2, self.image.get_height()/2))
        self.image.blit(n, text_rect)


class Card(pygame.sprite.Sprite):
    def __init__(self, rank, suit):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer

        # set rank and suit passed when creating object as an object attributes
        self.rank = rank
        self.suit = suit

        # to use object as a sprite we need to attributes - image and rect
        # image is a surface 50x70, rect is set to be the size of surface
        # rect is moved to position 100,100 on default
        self.image = pygame.Surface((50,70))
        self.rect = self.image.get_rect()
        self.rect.center = (100,100)

        # every card is facing down on default the card is just grey square
        # with a thin border
        self.up = 0
        self.image.fill((169,169,169))
        pygame.draw.rect(self.image, (0,0,0), (0,0,50,70), 1)


    def move_to(self, x,y):
        # chaning position of a card
        self.rect.center = (x,y)


    def flip(self):
        # flipping card
        # if attribute "up" is set to 1 then card will be filled with dark grey
        # so it looks like its flipped, if "up" is 0 then the card will be
        # flipped back - rank and suit will be drawn on to the card with a white background
        if self.up:
            self.image.fill((169,169,169))
        else:
            self.image.fill((255,255,255))

            if self.rank > 10:
                self.rank = ranks[self.rank]
            n = font.render(str(self.rank), True, (0,0,0))
            b = font.render(suits[self.suit-1][0], True, (0,0,0))
            self.image.blit(n, (0,0))
            self.image.blit(b, (0,25))

        pygame.draw.rect(self.image, (0,0,0), (0,0,50,70), 1)
        self.up = not self.up



def new_round():
    # random card from player's and enemy's deck is picked moved and flipped
    player_card = player.pop(random.randrange(len(player)))
    enemy_card = enemy.pop(random.randrange(len(enemy)))

    player_card.move_to(300, 400)
    enemy_card.move_to(300, 200)

    player_card.flip()
    enemy_card.flip()

    message[0] = 'wer'


def main():
    pygame.init()
    pygame.font.init()

    global font,font_option, screen
    font = pygame.font.SysFont("arial", 22)
    font_option = pygame.font.SysFont("arial", 14)

    screen = pygame.display.set_mode((800, 600))

    # create white background that is the size of the window
    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))

    # there will be 52 cards created 13 for every suit where card with number
    # 11 is a jack, 12 is a queen, 13 is a king and 14 is an ace
    # all the cards are append to card_list
    card_list = []
    for x in range(2, 15):
        for y in range(1,5):
            card_list.append(Card(x, y))

    # next all the cards are divided evenly between 2 players
    global player, enemy
    player = []
    enemy = []
    for _ in range(26):
        card1 = card_list.pop(random.randrange(len(card_list)))
        card2 = card_list.pop(random.randrange(len(card_list)))
        card1.move_to(600, 400)
        card2.move_to(600, 200)
        player.append(card1)
        enemy.append(card2)

    cards = pygame.sprite.LayeredUpdates(player, enemy)

    global message
    message = ['abc']

    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    while True:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in cards if s.rect.collidepoint(pos)]
                clicked_card = next(iter(clicked_sprites), None)
                if clicked_card in player:
                    start_round()

        textsurface = myfont.render(message[0], False, (0, 0, 0))
        screen.blit(textsurface,(0,0))

        cards.draw(screen)
        pygame.display.flip()


if __name__ == '__main__': main()
