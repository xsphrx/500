import sys
import random
import math
import os
import getopt
import pygame
from pygame.locals import *
import pygame.gfxdraw
import random

pygame.init()

# 1 hearts
# 2 clubs
# 3 diamonds
# 4 spades

red = (255, 0, 0)
black = (0, 0, 0)
suits = (('♥', red), ('♣', black), ('♦', red),('♠', black))
ranks = {11:'J', 12:'Q', 13:'K', 14:'A'}

def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, (200, 200))
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except Exception as e:
        print(e)
    return image, image.get_rect()


def rearrange_cards():
    for i, x in enumerate(player):
        cards.change_layer(x,35+i)
        x.move_to((screen.get_width()-200)/len(player)*i + 100, screen.get_height()-40)
    for i, x in enumerate(enemy):
        x.move_to((screen.get_width()-200)/len(enemy)*i + 100, 40)
    for i, x in enumerate(pile):
        x.move_to(screen.get_width()-200, screen.get_height()/2-i*5)
    for i, x in enumerate(deck):
        x.move_to(screen.get_width()-100, screen.get_height()/2-i*0.5)

def pick_card():
    card = deck.pop(random.randrange(len(deck)))
    card.flip()
    player.append(card)
    rearrange_cards()

def pick_pile():
    player.append(pile)
    pile = []
    rearrange_cards()

def pick_from_pile():
    player.append(pile.pop(len(pile)-1))
    rearrange_cards()

def sort():
    print('sorting')
    player.sort(key=lambda x: (x.suit, x.rank))
    rearrange_cards()




class Option(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100,30))
        self.rect = self.image.get_rect()
        self.text = text

        self.image.fill((255,255,255))
        pygame.draw.rect(self.image, (0,0,0), (0,0,100,30), 1)
        n = font_option.render(self.text, True, (0,0,0))
        text_rect = n.get_rect(center=(self.image.get_width()/2, self.image.get_height()/2))
        self.image.blit(n, text_rect)

        self.active = 1
        self.rect.center = (x,y)

    def update(self):
        pass

    def change_text(self, text):
        self.text = text
        self.image.fill((255,255,255))
        pygame.draw.rect(self.image, (0,0,0), (0,0,100,30), 1)
        n = font_option.render(self.text, True, (0,0,0))
        text_rect = n.get_rect(center=(self.image.get_width()/2, self.image.get_height()/2))
        self.image.blit(n, text_rect)

    def move_to(self, x, y):
        self.rect.center = (x,y)

    def toggle_active(self):
        self.active = not self.active


class Card(pygame.sprite.Sprite):

    def __init__(self, rank, suit, up=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50,70))
        self.up = up
        self.rank = rank
        self.suit = suit
        self.image.fill((169,169,169))
        pygame.draw.rect(self.image, (0,0,0), (0,0,50,70), 1)
        self.up = 0

        self.rect = self.image.get_rect()
        self.rect.center = (0,0)


    def update(self):
        pass

    def move_to(self, x, y):
        self.rect.center = (x,y)

    def flip(self):
        if self.up:
            self.image.fill((169,169,169))
            pygame.draw.rect(self.image, (0,0,0), (0,0,50,70), 1)
            self.up = 0
        else:
            self.image.fill((255,255,255))
            pygame.draw.rect(self.image, (0,0,0), (0,0,50,70), 1)
            if self.rank > 10:
                n = font.render(ranks[self.rank], True, (0,0,0))
            else:
                n = font.render(str(self.rank), True, (0,0,0))
            icon = font.render(suits[self.suit-1][0], True, suits[self.suit-1][1])
            self.image.blit(n, (2,0))
            self.image.blit(icon, (2,25))
            self.up = 1

def main():
    global font
    global font_option
    font = pygame.font.SysFont("arial", 22)
    font_option = pygame.font.SysFont("arial", 14)

    # Initialise screen
    global screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('500')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))


    global deck
    deck = [(x, y) for x in range(2,15) for y in range(1, 5)]
    deck = [Card(*x) for x in deck]

    # player = [deck.pop(random.randrange(len(deck))) for _ in range(7)]
    # enemy = [deck.pop(random.randrange(len(deck))) for _ in range(7)]
    # pile = [deck.pop(random.randrange(len(deck)))]
    #
    # print(deck)
    # print(player)
    # print(enemy)

    global player, enemy, pile
    player = []
    enemy = []
    for _ in range(7):
        card = deck.pop(random.randrange(len(deck)))
        card.flip()
        player.append(card)
        enemy.append(deck.pop(random.randrange(len(deck))))

    pile = [deck.pop(random.randrange(len(deck)))]
    pile[0].flip()

    print(player)
    print(enemy)

    # Initialise sprites
    global cards
    cards = pygame.sprite.LayeredUpdates(player, enemy, pile, deck)


    option1 = Option('Meld / Lay off', screen.get_width()-100, screen.get_height()/2+100)
    option2 = Option('Sort', screen.get_width()-100, screen.get_height()/2+135)
    global options
    options = pygame.sprite.RenderPlain(option1, option2)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialise clock
    clock = pygame.time.Clock()

    rearrange_cards()

    game = {'player_round': 1, }

    # Event loop
    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in cards if s.rect.collidepoint(pos)]
                clicked_card = next(iter(clicked_sprites), None)
                if clicked_card in deck:
                    pick_card()
                elif clicked_card in pile:
                    pick_from_pile()
                elif clicked_card in player:
                    show_options_for_card(clicked_cardif)

                clicked_options = [s for s in options if s.rect.collidepoint(pos)]
                clicked_option = next(iter(clicked_options), None)
                if clicked_option in options:
                    if clicked_option.text == 'Sort':
                        print('sort')
                        sort()
                    elif clicked_option.text == 'Meld / Lay off':
                        print('meld')
                        meld_lay_off(clicked_option)

        screen.blit(background, (0, 0))
        cards.draw(screen)
        options.draw(screen)
        pygame.display.flip()

def meld_lay_off(option):
    option.change_text('Finish')


if __name__ == '__main__': main()
