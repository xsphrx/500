import sys
import os
import pygame
import random
import time

red = (255, 0, 0)
black = (0, 0, 0)
suits = (('♥', red), ('♣', black), ('♦', red),('♠', black))
ranks = {11:'J', 12:'Q', 13:'K', 14:'A'}


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

            if self.rank > 10: cur_rank = ranks[self.rank]
            else: cur_rank = self.rank
            n = font.render(str(cur_rank), True, (0,0,0))

            b = font.render(suits[self.suit-1][0], True, suits[self.suit-1][1])
            self.image.blit(n, (0,0))
            self.image.blit(b, (0,25))

        pygame.draw.rect(self.image, (0,0,0), (0,0,50,70), 1)
        self.up = not self.up

    def flip_down(self):
        self.image.fill((169,169,169))
        pygame.draw.rect(self.image, (0,0,0), (0,0,50,70), 1)
        self.up = 0


def rearrange_cards():
    for i, x in enumerate(player):
        cards.change_layer(x,35+i)
        x.move_to(600, 400-i*0.5)
    for i, x in enumerate(enemy):
        cards.change_layer(x,35+i)
        x.move_to(600, 200-i*0.5)
    for i, x in enumerate(player_card):
        cards.change_layer(x,35+i)
        x.move_to(300+20*i, 400)
    for i, x in enumerate(enemy_card):
        cards.change_layer(x,35+i)
        x.move_to(300+20*i, 200)


def main():
    pygame.init()
    pygame.font.init()

    global font, screen
    font = pygame.font.SysFont("arial", 22)

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

    global cards, player_card, enemy_card
    cards = pygame.sprite.LayeredUpdates(player, enemy)

    player_card = []
    enemy_card = []

    global message
    message = ['']

    message_font = pygame.font.SysFont('Comic Sans MS', 30)

    rearrange_cards()

    while True:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in cards if s.rect.collidepoint(pos)]
                clicked_card = next(iter(clicked_sprites), None)
                if clicked_card in player:
                    if message[0] == 'its a draw':

                        player_card.append(player.pop(random.randrange(len(player))))
                        enemy_card.append(enemy.pop(random.randrange(len(enemy))))
                        player_card.append(player.pop(random.randrange(len(player))))
                        enemy_card.append(enemy.pop(random.randrange(len(enemy))))
                        player_card[-1].flip()
                        enemy_card[-1].flip()

                        rearrange_cards()

                        if player_card[-1].rank > enemy_card[-1].rank:
                            message[0] = 'player wins'

                        elif player_card[-1].rank < enemy_card[-1].rank:
                            message[0] = 'enemy wins'
                        else:
                            message[0] = 'its a draw'
                        break



                    if player_card:
                        for x in player_card: x.flip_down()
                        for x in enemy_card: x.flip_down()
                        if message[0] == 'player wins':
                            player += player_card
                            player += enemy_card
                            player_card = []
                            enemy_card = []
                        elif message[0] == 'enemy wins':
                            enemy += player_card
                            enemy += enemy_card
                            player_card = []
                            enemy_card = []




                    # random card from player's and enemy's deck is picked moved and flipped
                    player_card.append(player.pop(random.randrange(len(player))))
                    enemy_card.append(enemy.pop(random.randrange(len(enemy))))



                    player_card[0].flip()
                    enemy_card[0].flip()

                    rearrange_cards()

                    if player_card[0].rank > enemy_card[0].rank:
                        message[0] = 'player wins'

                    elif player_card[0].rank < enemy_card[0].rank:
                        message[0] = 'enemy wins'

                    else:
                        message[0] = 'its a draw'


        textsurface = message_font.render('enemy', False, (0, 0, 0))
        screen.blit(textsurface,(100,200))
        textsurface = message_font.render('player', False, (0, 0, 0))
        screen.blit(textsurface,(100,400))

        textsurface = message_font.render(message[0], False, (0, 0, 0))
        screen.blit(textsurface,(400,100))

        cards.draw(screen)
        pygame.display.flip()


if __name__ == '__main__': main()
