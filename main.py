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
        if hidden_grid[row][col] == "⬛":
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

def flood_fill(hidden, shown, check_row, check_col): 
    flooding = True
    checked = []
    to_check = []
    count = 0
    while flooding:
        try:
            to_check = [item for item in to_check if item not in checked]
            check_row = to_check[0][0]
            check_col = to_check[0][1]
            to_check.pop(0)
        except:
            if count == 0:
                pass
            else:
                break
        for i in range(-1, 2): 
            for j in range(-1, 2):
                if (i == 0 and j == 0) or ((check_row + i) < 2) or ((check_col + j) < 1): 
                    continue
                try:
                    if hidden[check_row + i][check_col + j] != "💣":
                        surrounding_bombs = check_surrounding(hidden, check_row + i, check_col + j)
                        if surrounding_bombs > 0:
                            hidden[check_row + i][check_col + j] = str(f' {surrounding_bombs}')
                            shown[check_row + i][check_col + j] = str(f' {surrounding_bombs}')
                        else:
                            hidden[check_row + i][check_col + j] = "⬜"
                            shown[check_row + i][check_col + j] = "⬜"
                            to_check.append([check_row + i, check_col + j])
                except: continue
        checked.append([check_row, check_col])
        count += 1

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
        hidden_grid[row][col] = str(f' {surrounding_bombs}')
        shown_grid[row][col] = str(f' {surrounding_bombs}')
    
    flood_fill(hidden_grid, shown_grid, row, col)

    display_grid(shown_grid)

    while True:
        flag = False
        choice = input("grid co-ordinate (write F in front of grid co-ord to flag): ").lower().strip()
        if len(choice) == 4:
            try:
                coord_char = choice[1]
                coord_num = int(choice[1:])
                if coord_char not in alphabet or coord_num > 26 or coord_num < 1:
                    raise ValueError
                flag = True
            except (IndexError, ValueError):
                print("please enter a valid grid coordinate")
        elif len(choice) == 3:
            try:
                if choice[0] == "f" and choice[1] in alphabet:
                    flag = True
                    coord_num = int(choice[2])
                else:
                    coord_num = int(choice[1])
                coord_char = choice[1]
                if coord_char not in alphabet or coord_num > 26 or coord_num < 1:
                    raise ValueError
            except (IndexError, ValueError):
                print("please enter a valid grid coordinate")
        else:
            try:
                coord_char = first_choice[0]
                coord_num = int(first_choice[1:])   
                if (len(first_choice) < 2 or len(first_choice) > 3 or coord_char not in alphabet or coord_num > 26 or coord_num < 1):
                    raise(ValueError) # i definitely shouldn't do this but i'm going to anyway
            except (IndexError, ValueError):
                print("please enter a valid grid coordinate")
        row = letter_to_number[coord_char] + 1
        col = coord_num
        if flag is True:
            if shown_grid[row][col] == "🚩":
                shown_grid[row][col] = "⬛"
            elif shown_grid[row][col] != "⬛":
                print("you can't place a flag on that square!")
            else:
                shown_grid[row][col] = "🚩"
        else:
            if hidden_grid[row][col] == "💣":
                display_grid(hidden_grid)
                print("game over!!!")
                break
            
            surrounding_bombs = check_surrounding(hidden_grid, row, col)

            if surrounding_bombs > 0:
                hidden_grid[row][col] = str(f' {surrounding_bombs}')
                shown_grid[row][col] = str(f' {surrounding_bombs}')
            
            flood_fill(hidden_grid, shown_grid, row, col)

        display_grid(hidden_grid)
        display_grid(shown_grid)

gameloop()
