import tkinter as tk
from tkinter import messagebox
import random

ROWS = 3
COLS = 3
symbol_count = {"A": 1, "B": 3, "C": 6, "D": 10}
symbol_values = {"A": 15, "B": 6, "C": 4, "D": 2}
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

BALANCE_FILE = "balance.txt"

def save_balance(balance):
    with open(BALANCE_FILE, "w") as file:
        file.write(str(balance))

def load_balance():
    try:
        with open(BALANCE_FILE, "r") as file:
            return int(file.read())
    except:
        return None 
    
all_symbols = []
for symbol, count in symbol_count.items():
    all_symbols.extend([symbol] * count)

def get_slot_machine_spin(rows, cols):
    columns = []
    for _ in range(cols):
        column = []
        # Bias symbol frequency: 'A' is rarest
        value = random.choices(
            population=list(symbol_count.keys()),
            weights=[0.05, 0.2, 0.35, 0.4],  # A (rarest) → D (common)
            k=rows
        )
        column.extend(value)
        columns.append(column)


    for row in range(rows):
        rng = random.random()
        if rng < 0.70:
            forced_mismatch = random.sample(list(symbol_count.keys()), 3)
            for col in range(cols):
                columns[col][row] = forced_mismatch[col]
        elif rng < 0.90:
            match_symbol = random.choices(list(symbol_count.keys()), weights=[0.05, 0.2, 0.35, 0.4])[0]
            match_positions = random.sample([0, 1, 2], 2)
            for i, col in enumerate(columns):
                if i in match_positions:
                    col[row] = match_symbol
                else:
                    col[row] = random.choice([s for s in symbol_count if s != match_symbol])
        else:
            match_symbol = random.choices(list(symbol_count.keys()), weights=[0.1, 0.2, 0.3, 0.4])[0]
            for col in columns:
                col[row] = match_symbol

    return columns


def check_winnings(columns, lines, bet):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        row = [column[line] for column in columns]
        if row[0] == row[1] == row[2]:
            win_amount = symbol_values[row[0]] * bet
            winnings += win_amount
            winning_lines.append((line + 1, f"3x {row[0]}", win_amount))
        elif row[0] == row[1] or row[1] == row[2] or row[0] == row[2]:
            match = row[0] if row[0] == row[1] or row[0] == row[2] else row[1]
            win_amount = int(symbol_values[match] * 0.3 * bet)
            winnings += win_amount
            winning_lines.append((line + 1, f"2x {match}", win_amount))
    return winnings, winning_lines

class SlotMachineApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Slot Machine Game")
        self.bet = 10
        self.lines = 3
        self.setup_investment_ui()

    def setup_investment_ui(self):
      self.investment_frame = tk.Frame(self.root)
      self.investment_frame.pack(pady=20)

      tk.Label(self.investment_frame, text="Enter your investment (₹):", font=("Arial", 14)).pack(pady=5)
      self.investment_entry = tk.Entry(self.investment_frame, font=("Arial", 14))
      self.investment_entry.pack(pady=5)
      tk.Button(self.investment_frame, text="Start Game", font=("Arial", 14), bg="green", fg="white",
                command=self.start_game).pack(pady=10)


    def setup_ui(self):
        self.balance_label = tk.Label(self.root, text=f"Balance: ₹{self.balance}", font=("Arial", 16), fg="green")
        self.balance_label.pack(pady=10)

        self.slots_frame = tk.Frame(self.root)
        self.slots_frame.pack()

        self.slot_labels = [[tk.Label(self.slots_frame, text="", width=4, height=2, font=("Arial", 24), borderwidth=2, relief="ridge")
                            for _ in range(COLS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                self.slot_labels[r][c].grid(row=r, column=c, padx=5, pady=5)

        settings_frame = tk.Frame(self.root)
        settings_frame.pack(pady=10)

        tk.Label(settings_frame, text="Bet/Line ₹:").grid(row=0, column=0)
        self.bet_entry = tk.Entry(settings_frame, width=5)
        self.bet_entry.insert(0, str(self.bet))
        self.bet_entry.grid(row=0, column=1)

        tk.Label(settings_frame, text="Lines:").grid(row=0, column=2)
        self.lines_entry = tk.Entry(settings_frame, width=5)
        self.lines_entry.insert(0, str(self.lines))
        self.lines_entry.grid(row=0, column=3)

        self.spin_button = tk.Button(self.root, text="🎲 Spin", font=("Arial", 14), bg="orange", command=self.spin)
        self.spin_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack()

    def spin(self):
        try:
            self.bet = int(self.bet_entry.get())
            self.lines = int(self.lines_entry.get())
            total_bet = self.bet * self.lines

            if not (MIN_BET <= self.bet <= MAX_BET):
                raise ValueError(f"Bet must be ₹{MIN_BET}-{MAX_BET}")
            if not (1 <= self.lines <= MAX_LINES):
                raise ValueError(f"Lines must be 1-{MAX_LINES}")
            if total_bet > self.balance:
                raise ValueError("Insufficient balance")

        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))
            return

        columns = get_slot_machine_spin(ROWS, COLS)
        for r in range(ROWS):
            for c in range(COLS):
                self.slot_labels[r][c].config(text=columns[c][r])

        winnings, winning_lines = check_winnings(columns, self.lines, self.bet)
        self.balance += (winnings - total_bet)
        self.balance_label.config(text=f"Balance: ₹{self.balance}")

        if winning_lines:
            lines_text = "\n".join([f"Line {line}: {match} → ₹{amount}" for line, match, amount in winning_lines])
            self.result_label.config(text=f"You won:\n{lines_text}\nTotal: ₹{winnings}", fg="blue")
        else:
            self.result_label.config(text="No winning lines this time.", fg="red")
        save_balance(self.balance)

    def start_game(self):
        try:
            balance_input = self.investment_entry.get()
            if balance_input == "":
                stored_balance = load_balance()
                if stored_balance is not None:
                    self.balance = stored_balance
                else:
                    raise ValueError("No previous balance found.")
            else:
                self.balance = int(balance_input)
                if self.balance <= 0:
                    raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Enter a positive number or leave blank to resume saved balance.")
            return

        save_balance(self.balance)
        self.investment_frame.destroy()
        self.setup_ui()

root = tk.Tk()
app = SlotMachineApp(root)
root.mainloop()
