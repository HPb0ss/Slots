import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {"A": 1, "B": 3, "C": 6, "D": 10}
symbol_values = {"A" : 15, "B" : 6, "C" : 4, "D" : 2}

all_symbols = []

def check_winnings(columns, lines, bet, values) :
  winnings = 0
  winning_lines = []
  symbols_on_line = []
  for line in range(lines):
    symbols_on_line = [column[line] for column in columns]
    first = symbols_on_line[0]
    second = symbols_on_line[1]
    third = symbols_on_line[2]
    if first == second == third :
      win_amount = values[first] * bet
      winnings += win_amount
      winning_lines.append((line + 1, f"3x {first}", win_amount))
    elif first == second or second == third or first == third:
      if first == second or first == third :
        win_amount = int(values[first] * 0.3 * bet)
        winnings += win_amount
        winning_lines.append((line + 1, f"2x {first}", win_amount))
      else :
        win_amount = int(values[second] * 0.3 * bet)
        winnings += win_amount
        winning_lines.append((line + 1, f"2x {second}", win_amount))

  return winnings, winning_lines

def create_all_symbols(symbols) :
  for symbol, symbol_count in symbols.items() :
    for _ in range(symbol_count) :
      all_symbols.append(symbol)

def get_slot_machine_spin(rows, cols) :   
  columns = []
  for _ in range(cols) :
    column = []
    current_symbols = all_symbols[:]
    for _ in range(rows) :
      value = random.choice(current_symbols)
      current_symbols.remove(value)
      column.append(value)
    columns.append(column)

  return columns

def print_slot_machine(columns):
  for row in range(len(columns[0])) :
    for i, column in enumerate(columns) :
      if i != len(columns) - 1 :
        print(column[row], end=" | ")
      else :
        print(column[row])

def deposit() :
  while True :
    amount = input("What would you like to deposit? ₹")
    if amount.isdigit() :
      amount = int(amount)
      if amount > 0 :
        break
      else :
        print("Amount must be greater than 0.")
    else :
      print("Please enter a number.")

  return amount

def get_no_of_lines() :
  while True :
    lines = input("Enter the number of lines to bet on (1-" + str(MAX_LINES) + ")? ")
    if lines.isdigit() :
      lines = int(lines)
      if 1 <= lines <= MAX_LINES :
        break
      else :
        print("Enter a valid number of lines.")
    else :
      print("Please enter a number.")

  return lines

def get_bet() :
  while True :
    bet = input("What would you like to bet on each line? ₹")
    if bet.isdigit() :
      bet = int(bet)
      if MIN_BET <= bet <= MAX_BET :
        break
      else :
        print(f"Amount must be between ₹{MIN_BET} - ₹{MAX_BET}")
    else :
      print("Please enter a number.")

  return bet

def spin(balance) :
  lines = get_no_of_lines()
  while True :
    bet = get_bet()
    total_bet = bet * lines

    if total_bet > balance :
      print(f"You do not have enough to bet that amount, your current balance is ₹{balance}")    
    else :
      break

  print(f"You are betting {bet} on {lines} lines, Total bet is equal to: ₹{total_bet}")
  
  slots = get_slot_machine_spin(lines, COLS)
  print_slot_machine(slots)

  winnings, winning_lines = check_winnings(slots, lines, bet, symbol_values)
  if winning_lines :
    print(f"You won on lines:")
    for line, match, amount in winning_lines :
      print(f"Line {line}: {match} → ₹{amount}")
  else :
    print("No winning lines this time.")
  print(f"Total winnings this time: ₹{winnings}.")
  
  with open("balance.txt", 'a') as file :
    file.write(f"{winnings - total_bet}\n")

  return winnings - total_bet

def main() :
  balance = deposit()
  create_all_symbols(symbol_count)
  while True :
    print(f"Current balance is ₹{balance}")
    ans = input("Press enter to play (\'q\' to quit)")
    if ans == 'q' :
      break
    balance += spin(balance)
  print(f"You left with ₹{balance}")
  
  

main()