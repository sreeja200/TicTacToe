import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import itertools

class TicTacToe:
    def __init__(self):
        self.current_player, self.x_score, self.o_score = "X", 0, 0
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.config(bg="#f0f0f0")
        self.window.geometry("800x400")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        self.grid_frame = tk.Frame(self.window)
        self.grid_frame.grid(row=0, column=0, sticky="nsew")
        self.title_label = tk.Label(self.grid_frame, text="Tic-Tac-Toe", font=("Arial", 24), bg="#f0f0f0", fg="#333")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))

        self.score_label = tk.Label(self.grid_frame, text=f"Player X: {self.x_score} | Player O: {self.o_score}", font=("Arial", 16), bg="#f0f0f0", fg="#333")
        self.score_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))

        self.buttons = [[tk.Button(self.grid_frame, text="", width=5, height=2, font=("Comic Sans MS", 40, "bold"), bg="#f4f4f4", relief="raised", bd=5, command=lambda i=i, j=j: self.make_move(i, j)) 
                         for j in range(3)] for i in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].grid(row=i+2, column=j, padx=5, pady=5)

        self.clap_frame = tk.Frame(self.window)
        self.clap_frame.grid(row=0, column=1, sticky="nsew")
        self.label = tk.Label(self.clap_frame)
        self.label.pack()

        try:
            self.frames = [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(Image.open(r"C:\Users\G SREEJA\Downloads\clappinghands.gif"))]
        except Exception as e:
            print(f"Error loading GIF: {e}")
            self.frames = []

        self.clap_frame.grid_forget()
        self.frame_cycle = itertools.cycle(self.frames)

    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, fg="#FF5733" if self.current_player == "X" else "#4C8BF5", font=("Comic Sans MS", 40, "bold"), bg="lightblue" if self.current_player == "X" else "#D8B3D6")
            if self.check_winner(self.current_player):
                self.update_score()
                self.show_winner_message()
                self.show_clapping_animation()
                self.enable_click_to_restart()
            elif all("" not in row for row in self.board):
                messagebox.showinfo("Game Over", "It's a draw!")
                self.enable_click_to_restart()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, player):
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == player:
                self.highlight_winning_combination([(i, 0), (i, 1), (i, 2)])
                return True
        # Check columns
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == player:
                self.highlight_winning_combination([(0, i), (1, i), (2, i)])
                return True
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            self.highlight_winning_combination([(0, 0), (1, 1), (2, 2)])
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            self.highlight_winning_combination([(0, 2), (1, 1), (2, 0)])
            return True
        return False

    def highlight_winning_combination(self, combination):
        for row, col in combination:
            self.buttons[row][col].config(bg="green")

    def reset_game(self, event=None):
        self.current_player, self.board = "X", [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", fg="black", font=("Comic Sans MS", 40, "bold"), bg="#f4f4f4")
        self.stop_clapping_animation()
        self.window.unbind("<Button-1>")

    def enable_click_to_restart(self):
        self.window.bind("<Button-1>", self.reset_game)

    def update_score(self):
        if self.current_player == "X":
            self.x_score += 1
        else:
            self.o_score += 1
        self.score_label.config(text=f"Player X: {self.x_score} | Player O: {self.o_score}")

    def show_winner_message(self):
        self.window.after(0, messagebox.showinfo, "Game Over", f"Player {self.current_player} wins!")

    def show_clapping_animation(self):
        self.clap_frame.grid(row=0, column=1, rowspan=3, padx=20)
        self.animate_clapping()

    def animate_clapping(self):
        try:
            self.label.config(image=next(self.frame_cycle))
            self.window.after(100, self.animate_clapping)
        except Exception as e:
            print(f"Error during frame update: {e}")

    def stop_clapping_animation(self):
        self.clap_frame.grid_forget()

    def run(self):
        self.window.mainloop()

TicTacToe().run()
