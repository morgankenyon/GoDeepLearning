# Import Module
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Button
from dlgo import agent
from dlgo import goboard_slow
from dlgo import gotypes
import time

def get_board_size(board_selection):
    if board_selection == "9x9":
        return 9
    elif board_selection == "13x13":
        return 13
    return 19

def get_bot(bot_selection):
    if bot_selection == 'Random':
        return agent.naive.RandomBot()
    return agent.naive.RandomBot()

def create_dot(board, middle_x, middle_y, color):
    dot_offset = 4
    board.create_oval(middle_x - dot_offset, middle_y - dot_offset, middle_x + dot_offset, middle_y + dot_offset, fill=color, width=1)

def draw_stone(board, middle_x, middle_y, color):
    stone_offset = 18
    board.create_oval(middle_x - stone_offset, middle_y - stone_offset, middle_x + stone_offset, middle_y + stone_offset, fill=color, width=1, outline="")

 
def write_board(game_board):
    board_height = 400
    board_width = 400

    board = Canvas(root, height=board_height, width=board_width, bg='#e4bf81')
    board.pack(pady=200)

    #write columns
    offset = 28
    space = 43
    for i in range(0, 9):
        number = i * space
        board.create_line(offset + number, offset + 0, offset + number, board_height - offset, fill="black", width=1)

    #write rows
    for i in range(0, 9):
        number = i * space
        board.create_line(offset + 0, offset + number, board_height - offset, offset + number, fill="black")
    
    #create dots
    middle = 4 * space + offset
    create_dot(board, middle, middle, "black")
    #board.create_oval(middle - 5, middle - 5, middle + 5, middle + 5, fill="black", width=1)

    left_coordinate = 2 * space + offset
    create_dot(board, left_coordinate, left_coordinate, "black")

    right_coordinate = 6 * space + offset
    create_dot(board, right_coordinate, right_coordinate, "black")

    create_dot(board, left_coordinate, right_coordinate, "black")
    create_dot(board, right_coordinate, left_coordinate, "black")

    # white_x = 1 * space + offset
    # white_y = 7 * space + offset
    # draw_stone(board, white_x, white_y, "white")
    
    # white_x = 1 * space + offset
    # white_y = 6 * space + offset
    # draw_stone(board, white_x, white_y, "white")

    # black_x = 3 * space + offset
    # black_y = 4 * space + offset
    # draw_stone(board, black_x, black_y, "black")

    for row in range(game_board.num_rows, 0, -1):
        for col in range(1, game_board.num_cols + 1):
            stone = game_board.get(gotypes.Point(row=row, col=col))
            if stone != None:
                print (f"row: {row}, col: {col}, stone: {stone}")
            stone_x = (row - 1) * space + offset
            stone_y = (col - 1) * space + offset
            if stone == gotypes.Player.black:
                draw_stone(board, stone_x, stone_y, "black")
            elif stone == gotypes.Player.white:
                draw_stone(board, stone_x, stone_y, "white") 

def start_game():
    board_size = get_board_size(board_size_selector.get())
    player_one_selection = player_one_selector.get()
    player_one_bot = get_bot(player_one_selection)
    player_two_selection = player_two_selector.get()
    player_two_bot = get_bot(player_two_selection)

    # messagebox.showinfo(
    #     message=f"BoardSize: {board_size}, player_one_bot: {player_one_selection}, player_two_bot: {player_two_selection}",
    #     title="Selection"
    # )

    game = goboard_slow.GameState.new_game(board_size)
    bots = {
        gotypes.Player.black: agent.naive.RandomBot(),
        gotypes.Player.white: agent.naive.RandomBot(),
    }

    #while not game.is_over():
    #time.sleep(2)

    for i in range(0, 100):

        bot_move = bots[game.next_player].select_move(game)
        game = game.apply_move(bot_move)
        write_board(game.board)
        print("Writing board")
    
    # bot_move = bots[game.next_player].select_move(game)
    # game = game.apply_move(bot_move)
    
    # bot_move = bots[game.next_player].select_move(game)
    # game = game.apply_move(bot_move)


# create root window
root = Tk()
 
window_width = 1200
window_height = 800
# root window title and dimension
root.title("Go")
# Set geometry(widthxheight)
root.geometry(f'{window_width}x{window_height}')
 
#adding game board selector
board_size_selector = Combobox(
    state="readonly",
    values=["9x9", "13x13", "19x19"]
)
board_size_selector.place(x=50, y=50)

#adding black bot
player_one_selector = Combobox(
    state="readonly",
    values=["Random"]
)
player_one_selector.place(x=250, y=50)

#adding white bot
player_two_selector = Combobox(
    state="readonly",
    values=["Random"]
)
player_two_selector.place(x=450, y=50)

#adding button to start game
button = Button(text="Display selection", command=start_game)
button.place(x=750, y=50)

#write_board()
# Execute Tkinter
root.mainloop()