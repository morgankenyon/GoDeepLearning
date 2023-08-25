# Import Module
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Button
from dlgo import agent
from dlgo import goboard_slow
from dlgo import gotypes
import time
from functools import partial
import math

class GoBoard():
    def __init__(self):
        self.root = Tk()
        self.offset = 28
        self.space = 43
        
        self.board_height = 400
        self.board_width = 400
        self.ui_board = Canvas(self.root, height=self.board_height, width=self.board_width, bg='#e4bf81')

    def get_board_size(self, board_selection):
        if board_selection == "9x9":
            return 9
        elif board_selection == "13x13":
            return 13
        return 19

    def get_bot(self, bot_selection):
        if bot_selection == 'Random':
            return agent.naive.RandomBot()
        return agent.naive.RandomBot()

    def create_dot(self, board, middle_x, middle_y, color):
        dot_offset = 4
        board.create_oval(middle_x - dot_offset, middle_y - dot_offset, middle_x + dot_offset, middle_y + dot_offset, fill=color, width=1)

    def draw_stone(self, board, middle_x, middle_y, color):
        stone_offset = 18
        board.create_oval(middle_x - stone_offset, middle_y - stone_offset, middle_x + stone_offset, middle_y + stone_offset, fill=color, width=1, outline="")

    def draw_recent_stone(self, board, middle_x, middle_y, player):
        highlight_offset = 8
        stone_color = "white"
        stone_highlight = "black"
        if player == gotypes.Player.black:
            stone_color = "black"
            stone_highlight = "white"
        
        self.draw_stone(board, middle_x, middle_y, stone_color)
        board.create_oval(middle_x - highlight_offset, middle_y - highlight_offset, middle_x + highlight_offset, middle_y + highlight_offset, outline=stone_highlight, width=1)
    
    def write_board(self, board):
        #write columns
        for i in range(0, 9):
            number = i * self.space
            board.create_line(self.offset + number, self.offset + 0, self.offset + number, self.board_height - self.offset, fill="black", width=1)

        #write rows
        for i in range(0, 9):
            number = i * self.space
            board.create_line(self.offset + 0, self.offset + number, self.board_height - self.offset, self.offset + number, fill="black")
        
        #create dots
        middle = 4 * self.space + self.offset
        self.create_dot(board, middle, middle, "black")
 
        left_coordinate = 2 * self.space + self.offset
        self.create_dot(board, left_coordinate, left_coordinate, "black")

        right_coordinate = 6 * self.space + self.offset
        self.create_dot(board, right_coordinate, right_coordinate, "black")

        self.create_dot(board, left_coordinate, right_coordinate, "black")
        self.create_dot(board, right_coordinate, left_coordinate, "black")
    
    def calc_pos(self, num):
        return (num - 1) * self.space + self.offset
    
    def write_pieces(self, game_board, bot_move):
        self.ui_board.delete("all")

        self.write_board(self.ui_board)
        for row in range(game_board.num_rows, 0, -1):
            for col in range(1, game_board.num_cols + 1):
                stone = game_board.get(gotypes.Point(row=row, col=col))
                # if stone != None:
                #     print (f"row: {row}, col: {col}, stone: {stone}")
                stone_x = self.calc_pos(row)
                stone_y = self.calc_pos(col)
                if stone == gotypes.Player.black:
                    self.draw_stone(self.ui_board, stone_x, stone_y, "black")
                elif stone == gotypes.Player.white:
                    self.draw_stone(self.ui_board, stone_x, stone_y, "white") 
        
        new_stone_x = self.calc_pos(bot_move.row)
        new_stone_y = self.calc_pos(bot_move.col)
        new_stone_color = game_board.get(gotypes.Point(row=bot_move.row, col=bot_move.col))
        self.draw_recent_stone(self.ui_board, new_stone_x, new_stone_y, new_stone_color)

    def make_move(self, game, bots, count):
        if game.is_over():
            print("Game is over")
            Label(self.root,
                text='Game is over',
                font=('Arial', 20)).place(x=100, y=400)

        else:
            bot_move = bots[game.next_player].select_move(game)

            game = game.apply_move(bot_move)
            if (not bot_move.is_pass) and (not bot_move.is_resign):
                self.write_pieces(game.board, bot_move.point)
                
            
            self.root.after(150, partial(self.make_move, game, bots, count - 1))

    def start_game(self, board_size_selector, player_one_selector, player_two_selector):
        #getting selections for game
        board_size = self.get_board_size(board_size_selector.get())
        player_one_selection = player_one_selector.get()
        player_one_bot = self.get_bot(player_one_selection)
        player_two_selection = player_two_selector.get()
        player_two_bot = self.get_bot(player_two_selection)

        game = goboard_slow.GameState.new_game(board_size)
        bots = {
            gotypes.Player.black: player_one_bot,
            gotypes.Player.white: player_two_bot,
        }

        self.make_move(game, bots, 3)

    def launch(self):
        window_width = 1200
        window_height = 800
        # root window title and dimension
        self.root.title("Go")
        # Set geometry(widthxheight)
        self.root.geometry(f'{window_width}x{window_height}')
        
        #adding game board selector
        board_size_selector = Combobox(
            state="readonly",
            values=["9x9", "13x13", "19x19"]
        )
        board_size_selector.place(x=50, y=50)
        board_size_selector.current(0)

        #adding black bot
        player_one_selector = Combobox(
            state="readonly",
            values=["Random"]
        )
        player_one_selector.place(x=250, y=50)
        player_one_selector.current(0)

        #adding white bot
        player_two_selector = Combobox(
            state="readonly",
            values=["Random"]
        )
        player_two_selector.place(x=450, y=50)
        player_two_selector.current(0)

        #adding button to start game
        button = Button(text="Display selection", command=partial(
            self.start_game, 
            board_size_selector,
            player_one_selector,
            player_two_selector
        ))
        button.place(x=750, y=50)

        columns = 'ABCDEFGHJKLMNOPQRST'
        user_name = Label(self.root,
            text =  '   '.join(columns[:9]),          # need to update
            font=("Arial", 20)).place(x = 415,
                                    y = 600) 
        
        for i in range(1, 10):
            Label(self.root,
                  text = f'{i}',
                  font=('Arial', 20)).place(x = 367,
                                            y = 595 - (i * 43))

        self.ui_board.pack(pady=200)
        self.write_board(self.ui_board)

        # Execute Tkinter
        self.root.mainloop()

if __name__ == '__main__':
    goBoard = GoBoard()
    goBoard.launch()