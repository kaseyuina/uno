from uno_objects import card
from uno_objects import player
import random
import pygame
import os

pygame.init()

# Setting up game screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Uno")

image_directory = "images"
image_size = (140, 200)
images = {}

x = 20
y = 50

for filename in os.listdir(image_directory):
    if filename.endswith(".png"):
        path = os.path.join(image_directory, filename)
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, image_size)
        x += image_size[0] + 10
        if x > SCREEN_WIDTH:
            x = 50
            y += image_size[1] + 10
        images[image] = (x, y)

f = open("uno_cards.txt", "r")
cards = f.readlines()
f.close()

uno_cards = []
card_pile = []
order = True
card_cleared = False
turn = 0
add_turn = 1
top_card = [card(0, 0, 0)]
draw_num = 0

num_of_players = int(input("Number of players (between 2 - 10): "))
players = [0] * num_of_players

# Storing contents of uno_cards.txt to card object
for line in range(len(cards)):
    card_detail = cards[line].split(",")
    uno_cards.append(card(card_detail[0], card_detail[1], card_detail[2]))

#Shuffling the deck
random.shuffle(uno_cards)

#Assigning CPU flag to each player
for i in range(num_of_players):
    if i == 0:
        players[i] = player([], 0, False)
    else:
        players[i] = player([], 0, True)

#Dealing cards
for i in range(7):
    for j in range(num_of_players):
        players[j].cards.append(uno_cards[0])
        uno_cards.pop(0)

#Showing top card of the pile
while int(uno_cards[0].points) > 10:
    random.shuffle(uno_cards)

top_card[0] = uno_cards[0]
uno_cards.pop(0)

def show_top_card():
    print("*Top card is: [" + top_card[0].color + " " + str(top_card[0].number) + "]*")

#Randomly select who starts the game
turn = random.randint(0, num_of_players-1)
print("Player" + str(turn + 1) + " starts the game")
print()

#Loop until one player finishes
while card_cleared == False:
    add_turn = 1
    print("=================================")
    print("Player" + str(turn + 1) + "'s turn")
    print("Order: ", end="")
    if order == True:
        for i in range(len(players)):
            print("Player" + str((i + turn) % num_of_players + 1), end=" -> ")
    else:
        for i in range(len(players), 0, -1):
            print("Player" + str((i + turn) % num_of_players + 1), end=" -> ")
    print()
    print()
    if players[turn].cpu == False:
        show_top_card()
        players[turn].display_cards()
        card_effect = False
        selected_cards = [0]
        while card_effect == False:
            if draw_num > 0:
                print(str(top_card[0].number + " was used."))
                selected_cards = [int(tok) for tok in input("Select " + str(top_card[0].number) + " from your hand, or type 0 to draw " + str(draw_num) + " cards: ").split(",")]
                if selected_cards[0] == 0:
                    draw_num = players[turn].draw_card(uno_cards, card_pile, draw_num, turn)
                    card_effect = True
                else:
                    if top_card[0].number == players[turn].cards[selected_cards[0] - 1].number:
                        card_effect = players[turn].use_card(selected_cards, top_card, card_pile, turn)
                        if card_effect[2] > 0:
                            draw_num += card_effect[2]
                        if card_effect[3] == True:
                            val_color = False
                            while val_color == False:
                                print("1: red")
                                print("2: yellow")
                                print("3: green")
                                print("4: purple")
                                next_color = int(input("Please select a color from the above: "))
                                if next_color == 1:
                                    top_card[0].color = "red"
                                    val_color = True
                                elif next_color == 2:
                                    top_card[0].color = "yellow"
                                    val_color = True
                                elif next_color == 3:
                                    top_card[0].color = "green"
                                    val_color = True
                                elif next_color == 4:
                                    top_card[0].color = "purple"
                                    val_color = True
                                else:
                                    print("Please select a valid color")
            else:
                selected_cards = [int(tok) for tok in input("Please select cards to use, or type 0 to draw a card: ").split(",")]
                # print(selected_cards)
                if selected_cards[0] == 0:
                    # print("check")
                    draw_num = players[turn].draw_card(uno_cards, card_pile, 1, turn)
                    card_effect = True
                else:
                    card_effect = players[turn].use_card(selected_cards, top_card, card_pile, turn)
                    if not card_effect == False:
                        add_turn = add_turn + card_effect[0]
                        for i in range(int(card_effect[1])):
                            if order == True:
                                order = False
                            else:
                                order = True
                        if card_effect[2] > 0:
                            draw_num += card_effect[2]
                        if card_effect[3] == True:
                            val_color = False
                            while val_color == False:
                                print("1: red")
                                print("2: yellow")
                                print("3: green")
                                print("4: purple")
                                next_color = int(input("Please select a color from the above: "))
                                if next_color == 1:
                                    top_card[0].color = "red"
                                    val_color = True
                                elif next_color == 2:
                                    top_card[0].color = "yellow"
                                    val_color = True
                                elif next_color == 3:
                                    top_card[0].color = "green"
                                    val_color = True
                                elif next_color == 4:
                                    top_card[0].color = "purple"
                                    val_color = True
                                else:
                                    print("Please select a valid color")
        print("You have " + str(len(players[turn].cards)) + " cards left")
        print()
        if len(players[turn].cards) == 0:
            card_cleared = True
            print("*******************")
            print("*You won the game!*")
            print("*******************")

        #Changing turn
        if order == True:
            turn = (turn + add_turn) % num_of_players
        else:
            turn = (turn - add_turn) % num_of_players
        if len(players[turn].cards) == 0:
            card_cleared = True
    else:
        add_turn = 1
        total_points = 0
        selected_cards = [0]
        show_top_card()
        if draw_num > 0:
            print(str(top_card[0].number + " was used."))
            for x, i in enumerate(players[turn].cards):
                cur_cards = []
                if i.number == top_card[0].number:
                    cur_cards.append(x + 1)
                    selected_cards = cur_cards
            if selected_cards[0] == 0:
                draw_num = players[turn].draw_card(uno_cards, card_pile, draw_num, turn)
            else:
                card_effect = players[turn].use_card(selected_cards, top_card, card_pile, turn)
                add_turn = add_turn + card_effect[0]
                if card_effect[2] > 0:
                    draw_num += card_effect[2]
                total_points = 0
                cur_total_points = 0
                for i in players[turn].cards:
                    cur_color = i.color
                    for j in players[turn].cards:
                        if j.color == cur_color:
                            cur_total_points += int(j.points)
                    if total_points <= cur_total_points:
                        total_points = cur_total_points
                        selected_color = cur_color
                top_card[0].color = selected_color
        else:
            for x, i in enumerate(players[turn].cards):
                cur_total_points = 0
                cur_cards = []
                if i.color == "-" or top_card[0].color == i.color or top_card[0].number == i.number:
                    cur_cards.append(x + 1)
                    cur_total_points += int(i.points)
                    for y, j in enumerate(players[turn].cards):
                        if x == y:
                            pass
                        elif i.number == j.number:
                            cur_cards.append(y + 1)
                            cur_total_points += int(j.points)
                    if total_points <= cur_total_points:
                        total_points = cur_total_points
                        selected_cards = cur_cards

            if selected_cards[0] == 0:
                draw_num = players[turn].draw_card(uno_cards, card_pile, 1, turn)
            else:
                card_effect = players[turn].use_card(selected_cards, top_card, card_pile, turn)
                add_turn = add_turn + card_effect[0]
                for i in range(int(card_effect[1])):
                    if order == True:
                        order = False
                    else:
                        order = True
                if card_effect[2] > 0:
                    draw_num += card_effect[2]
                if card_effect[3] == True:
                    total_points = 0
                    cur_total_points = 0
                    for i in players[turn].cards:
                        cur_color = i.color
                        for j in players[turn].cards:
                            if j.color == cur_color:
                                cur_total_points += int(j.points)
                        if total_points <= cur_total_points:
                            total_points = cur_total_points
                            selected_color = cur_color
                    top_card[0].color = selected_color
        print("Player" + str(turn + 1) + " has " + str(len(players[turn].cards)) + " cards left")
        print()
        if len(players[turn].cards) == 0:
            card_cleared = True
            print("***********************")
            print("*Player" + str(turn + 1) + " won the game!*")
            print("***********************")
        else:
            input("Press enter to continue")
        #Changing turn
        if order == True:
            # print(str(turn) + " " + str(add_turn) + " " + str(num_of_players))
            turn = (turn + add_turn) % num_of_players
            # print(str(turn) + " " + str(add_turn) + " " + str(num_of_players))
        else:
            turn = (turn - add_turn) % num_of_players

print()
print("[RESULT]")
for i in range(num_of_players):
    total_points = 0
    for j in players[i].cards:
        total_points += int(j.points)
    print("Player" + str(i + 1) + ": " + str(total_points) + " points")