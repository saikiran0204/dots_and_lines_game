from tkinter import *
from pygame import *
from sys import exit


class Players:
    def __init__(self, name, first):
        self.name = name
        self.points = 0
        self.first = first


def final():
    global players_list, number_of_players
    for i in range(number_of_players):
        for j in range(i + 1, number_of_players):
            if players_list[i].points < players_list[j].points:
                players_list[i], players_list[j] = players_list[j], players_list[i]
    window_3 = Tk()
    Label(window_3, text="Name").grid(row=0, column=0)
    Label(window_3, text="Points").grid(row=0, column=1)
    for i in range(number_of_players):
        Label(window_3, text=players_list[i].name).grid(row=i + 1, column=0)
        Label(window_3, text=players_list[i].points).grid(row=i + 1, column=1)
    z = Button(window_3, text='Close', command=lambda: window_3.destroy())
    z.grid(row=i + 2, column=1)
    window_3.mainloop()
    exit()


def round_of_pos(number):
    if number[-1] > 5:
        number[-2] += 1
    number[-1] = 0
    sum_1 = 0
    for i in number:
        sum_1 = sum_1 * 10 + i
    return sum_1


def left(x, y):
    if y in horizontal_visited[x - 1] and y in vertical_visited[x - 1] and y + 1 in horizontal_visited[x - 1]:
        textRect.center = (x * 30 - 15, y * 50 + 25)
        window.blit(text, textRect)
        return True


def right(x, y):
    if y in horizontal_visited[x] and y in vertical_visited[x + 1] and y + 1 in horizontal_visited[x]:
        textRect.center = (x * 30 + 15, y * 50 + 25)
        window.blit(text, textRect)
        return True


def check_vertical(x, y):
    global vertical_visited, horizontal_visited, turn
    if 1 < x < 19:
        if right(x, y) and left(x, y):
            return True, True, True
    if x > 1:
        if left(x, y):
            return True, True, False
    if x < 19:
        if right(x, y):
            return True, True, False
    return False, True


def down(x, y):
    if y + 1 in horizontal_visited[x] and y in vertical_visited[x] and y in vertical_visited[x + 1]:
        textRect.center = (x * 30 + 15, y * 50 + 25)
        window.blit(text, textRect)
        return True


def up(x, y):
    if y - 1 in vertical_visited[x] and y - 1 in horizontal_visited[x] and y - 1 in vertical_visited[x + 1]:
        textRect.center = (x * 30 + 15, y * 50 - 25)
        window.blit(text, textRect)
        return True


def check_horizontal(x, y):
    global vertical_visited, horizontal_visited, turn, textRect
    if 1 < y < 19:
        if down(x, y) and up(x, y):
            return True, True, True
    if y < 19:
        if down(x, y):
            return True, True, False
    if y > 1:
        if up(x, y):
            return True, True, False
    return False, True


def define_position(position):
    global vertical_visited, horizontal_visited
    if 574 > position[0] > 25 and 955 > position[1] > 45:
        x = round_of_pos([int(i) for i in str(position[0])])
        y = round_of_pos([int(i) for i in str(position[1])])
        temp_y = y // 50
        temp_x = x // 30
        print(temp_x, temp_y, x, y)
        print(horizontal_visited, '\n', vertical_visited)
        if x % 30 == 0:  # vertical
            if temp_y in vertical_visited[temp_x]:
                return False, False
            # print(temp_x, temp_y, "vertical")  # -------------------------print
            draw.line(window, (255, 0, 0), (temp_x * 30, temp_y * 50), (temp_x * 30, temp_y * 50 + 50), 5)
            vertical_visited[temp_x].append(temp_y)
            return check_vertical(temp_x, temp_y)
        elif y % 50 == 0:
            if temp_y in horizontal_visited[temp_x]:
                return False, False
            # print(temp_x, temp_y, "horizontal")  # ------------------------- print
            draw.line(window, (255, 0, 0), (temp_x * 30, temp_y * 50), (temp_x * 30 + 30, temp_y * 50), 5)
            horizontal_visited[temp_x].append(temp_y)
            return check_horizontal(temp_x, temp_y)
    return False, False


def pygame_initial():
    global horizontal_visited, vertical_visited, players_list, window, number_of_players, text, textRect
    init()
    window = display.set_mode((650, 960))
    display.set_caption("Game")
    window.fill((255, 255, 255))
    running = True
    for i in range(1, 20):
        horizontal_visited.append([])
        vertical_visited.append([])
        for j in range(1, 20):
            if i != 19 and j != 19:
                draw.rect(window, (0, 255, 255), (i * 30 + 2, j * 50 + 2, 26, 46))
            draw.circle(window, (255, 0, 0), (i * 30, j * 50), 3)
    font_1 = font.SysFont('freesansbold.ttf', 50)
    text_2 = font_1.render("Turn:", False, green, None)
    window.blit(text_2, (0, 0))
    turn = 0
    text_3 = font_1.render(str(players_list[turn].name), False, green, None)
    window.blit(text_3, (110, 0))
    text = font_1.render(str(players_list[turn].first), False, green, blue)
    textRect = text.get_rect()
    while running:
        for even in event.get():
            if even.type == QUIT:
                running = False
                quit()
                final()
            elif even.type == MOUSEBUTTONDOWN:
                temp = define_position(even.pos)
                if temp[1]:
                    if temp[0]:
                        if temp[2]:
                            players_list[turn].points += 2
                        else:
                            players_list[turn].points += 1
                    else:
                        turn += 1
                    if turn == number_of_players:
                        turn = 0
                    rectangle = text_3.get_rect()
                    draw.rect(window, white, (rectangle[0] + 110, rectangle[1], rectangle[2], rectangle[3]))
                    text_3 = font_1.render(str(players_list[turn].name), False, green, None)
                    window.blit(text_3, (110, 0))
                    text = font_1.render(str(players_list[turn].first), False, green, blue)
                    window.blit(text_3, (110, 0))
        display.update()


def third(number, players, window, letter_entry):
    global players_list, number_of_players
    number_of_players = number
    for i in range(number):
        players_list.append(Players(players[i].get(), letter_entry[i].get()))
    window.destroy()
    pygame_initial()


def second(number, window):
    number_of_players = int(number.get())
    window.destroy()
    window_1 = Tk()
    players_entry = []
    letter_entry = []
    for i in range(number_of_players):
        Label(window_1, text="Enter player name:").grid(row=i, column=0)
        number = Entry(window_1)
        number.grid(row=i, column=1)
        Label(window_1, text='and enter letter to display').grid(row=i, column=2)
        letter = Entry(window_1)
        letter.grid(row=i, column=3)
        letter_entry.append(letter)
        players_entry.append(number)
    z = Button(window_1, text='enter',
               command=lambda number=number_of_players, players=players_entry, window=window_1,
                              letter_entry=letter_entry: third(number, players,
                                                               window, letter_entry))
    z.grid(row=i + 1, column=1)
    window_1.mainloop()


def first():
    window = Tk()
    Label(window, text="Enter number of players:").grid(row=0, column=0)
    number = Entry(window)
    number.grid(row=0, column=1)
    z = Button(window, text='enter', command=lambda number=number, window=window: second(number, window))
    z.grid(row=1, column=1)
    window.mainloop()


white = (255, 255, 255)
green = (0, 0, 0)
blue = (0, 255, 255)
vertical_visited = [[]]
horizontal_visited = [[]]
players_list = []
number_of_players = 0
first()
