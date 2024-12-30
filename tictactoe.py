import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import itertools

class TicTacToe:
    def __init__(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.x_score = 0
        self.o_score = 0

        # Set up the main window
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.config(bg="#f0f0f0")
        self.window.geometry("800x400")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        # Left half: Tic-Tac-Toe grid and Score
        self.grid_frame = tk.Frame(self.window)
        self.grid_frame.grid(row=0, column=0, sticky="nsew")
        self.grid_frame.grid_propagate(False)

        # Title Label
        self.title_label = tk.Label(self.grid_frame, text="Tic-Tac-Toe", font=("Arial", 24), bg="#f0f0f0", fg="#333")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))

        # Score Labels
        self.score_label = tk.Label(self.grid_frame, text=f"Player X: {self.x_score} | Player O: {self.o_score}",
                                    font=("Arial", 16), bg="#f0f0f0", fg="#333")
        self.score_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))

        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.grid_frame, text="", width=5, height=2, font=("Comic Sans MS", 40, "bold"),
                                   bg="#f4f4f4", relief="raised", bd=5, command=lambda i=i, j=j: self.make_move(i, j))
                button.grid(row=i+2, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)

        # Right half: Clapping hands animation
        self.clap_frame = tk.Frame(self.window)
        self.clap_frame.grid(row=0, column=1, sticky="nsew")

        # Load the clapping hands GIF
        gif_path = r"C:\Users\G SREEJA\Downloads\clappinghands.gif"
        try:
            self.clap_image = Image.open(gif_path)
            self.frames = [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(self.clap_image)]
        except Exception as e:
            print(f"Error loading GIF: {e}")
            self.frames = []

        # Create a label to display the image
        self.label = tk.Label(self.clap_frame)
        self.label.pack()

        # Initially, hide the clapping animation
        self.clap_frame.grid_forget()

        # Initialize frame cycle for clapping animation
        self.frame_cycle = itertools.cycle(self.frames)

    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            if self.current_player == "X":
                self.buttons[row][col].config(text=self.current_player, fg="#FF5733", font=("Comic Sans MS", 40, "bold"), bg="lightblue")
            else:
                self.buttons[row][col].config(text=self.current_player, fg="#4C8BF5", font=("Comic Sans MS", 40, "bold"), bg="#D8B3D6")

            if self.check_winner(self.current_player):
                self.update_score()
                self.show_winner_message()
                self.show_clapping_animation()
                self.enable_click_to_restart()
            elif self.is_board_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.enable_click_to_restart()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self, player):
        # Check rows, columns, and diagonals
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == player:
                self.highlight_winning_combination([(i, 0), (i, 1), (i, 2)])
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == player:
                self.highlight_winning_combination([(0, i), (1, i), (2, i)])
                return True
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

    def is_board_full(self):
        for row in self.board:
            if "" in row:
                return False
        return True

    def reset_game(self, event=None):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", fg="black", font=("Comic Sans MS", 40, "bold"), bg="#f4f4f4")
        self.update_score()
        self.stop_clapping_animation()
        self.window.unbind("<Button-1>")  # Unbind the click event

    def enable_click_to_restart(self):
        self.window.bind("<Button-1>", self.reset_game)

    def update_score(self):
        if self.current_player == "X":
            self.x_score += 1
        elif self.current_player == "O":
            self.o_score += 1
        self.score_label.config(text=f"Player X: {self.x_score} | Player O: {self.o_score}")

    def show_winner_message(self):
        self.window.after(0, messagebox.showinfo, "Game Over", f"Player {self.current_player} wins!")

    def show_clapping_animation(self):
        self.clap_frame.grid(row=0, column=1, rowspan=3, padx=20)
        self.animate_clapping()

    def animate_clapping(self):
        try:
            next_frame = next(self.frame_cycle)
            self.label.config(image=next_frame)
            self.window.after(100, self.animate_clapping)
        except Exception as e:
            print(f"Error during frame update: {e}")

    def stop_clapping_animation(self):
        self.clap_frame.grid_forget()

    def run(self):
        self.window.mainloop()

# Run the game
game = TicTacToe()
game.run()
