from copy import deepcopy
from random import randint

alphabet = [chr(i) for i in range(97, 123)]
letter_to_number = letter_to_number = {letter: index + 1 for index, letter in enumerate(alphabet)}

def create_grid():
    hidden_grid = [[ "⬛" for i in range(16)] for j in range(16)]
    new_row = ["  "]
    new_row_2 = ["  "]
    for i in range(len(hidden_grid)):
        if i < 9:
            new_row_2.append("_ ")
            new_row.append(str(f'{i + 1} '))
        else:
            new_row_2.append(f'{str(i + 1)[0]} ')
            new_row.append(f'{str(i + 1)[1]} ')
    hidden_grid.insert(0, new_row)
    hidden_grid.insert(0, new_row_2)
    for idx, row in enumerate(hidden_grid):
        if idx == 0 or idx == 1:
            continue
        row.insert(0, alphabet[idx - 2])
    shown_grid = deepcopy(hidden_grid)
    return shown_grid, hidden_grid

def display_grid(grid):
    for i in grid:
        print("".join(i))

def place_bombs(hidden_grid):
    i = 0
    while i < 40:
        row = randint(2, 17)
        col = randint(1, 16)
        if hidden_grid[row][col] != "💣":
            hidden_grid[row][col] = "💣"
        else:
            continue
        i += 1

def check_surrounding(grid, check_row, check_col):
    bombs = 0

    for i in range(-1, 2): 
        for j in range(-1, 2):
            if i == 0 and j == 0: 
                continue
            
            neighbor_row = check_row + i 
            neighbor_col = check_col + j
            try:                    
                if grid[neighbor_row][neighbor_col] == "💣": 
                    bombs += 1 
            except IndexError: 
                pass
    return bombs

def flood_fill():
    pass # ill code later

def gameloop():
    shown_grid, hidden_grid = create_grid()
    display_grid(grid=shown_grid)
    while True:
        first_choice = input("where: ").lower().strip()
        try:
            coord_char = first_choice[0]
            coord_num = int(first_choice[1:])   
            if (len(first_choice) < 2 or len(first_choice) > 3 or coord_char not in alphabet or coord_num > 26 or coord_num < 1):
                raise(ValueError) # i definitely shouldn't do this but i'm going to anyway
        except (IndexError, ValueError):
            print("please enter a valid grid coordinate")
            continue
        break

    row = letter_to_number[coord_char] + 1
    col = coord_num

    hidden_grid[row][col] = "⬜"
    shown_grid[row][col] = "⬜"

    place_bombs(hidden_grid)
    surrounding_bombs = check_surrounding(hidden_grid, row, col)
    if surrounding_bombs > 0:
        hidden_grid[row][col] = surrounding_bombs
        shown_grid[row][col] = surrounding_bombs
    display_grid(hidden_grid)
    display_grid(shown_grid)

gameloop()
