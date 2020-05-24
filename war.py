import sys, pygame
import random

red = (255, 0, 0)
black = (0, 0, 0)
suits = (('♥', red), ('♣', black), ('♦', red),('♠', black))
ranks = {11:'J', 12:'Q', 13:'K', 14:'A'}


class Card(pygame.sprite.Sprite):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image = pygame.Surface((50,70))
        self.image.fill((169,169,169))
        self.flipped = 1

        self.rect = self.image.get_rect()
        self.rect.center = (100,100)

    def move_to(self, x,y):
        self.rect.center = (x,y)

    def flip(self):
        if self.flipped:
            self.image.fill((169,169,169))
            self.flipped = not self.flipped
        else:
            self.image.fill((255,255,255))
            pygame.draw.rect(self.image, (0,0,0), (0,0,50,70), 1)

            if self.rank > 10:
                self.rank = ranks[self.rank]
            n = font.render(str(self.rank), True, (0,0,0))
            b = font.render(suits[self.suit-1][0], True, (0,0,0))
            self.image.blit(n, (0,0))
            self.image.blit(b, (0,25))



def start_round():
    player_card = player.pop(random.randrange(len(player)))
    enemy_card = enemy.pop(random.randrange(len(enemy)))

    player_card.move_to(300, 400)
    enemy_card.move_to(300, 200)

    player_card.flip()
    enemy_card.flip()

def main():
    pygame.init()
    pygame.font.init()

    global font
    font = pygame.font.SysFont("arial", 22)

    screen = pygame.display.set_mode((800, 600))

    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))

    card_list = []
    for x in range(2, 15):
        for y in range(1,5):
            card_list.append(Card(x, y))

    global player, enemy
    player = []
    enemy = []
    for _ in range(26):
        card1 = card_list.pop(random.randrange(len(card_list)))
        card2 = card_list.pop(random.randrange(len(card_list)))
        card1.move_to(600, 400)
        card2.move_to(600, 200)
        card1.flip()
        card2.flip()
        player.append(card1)
        enemy.append(card2)

    cards = pygame.sprite.LayeredUpdates(player, enemy)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in cards if s.rect.collidepoint(pos)]
                clicked_card = next(iter(clicked_sprites), None)
                if clicked_card in player:
                    start_round()

        screen.blit(background, (0, 0))
        cards.draw(screen)
        pygame.display.flip()


if __name__ == '__main__': main()
