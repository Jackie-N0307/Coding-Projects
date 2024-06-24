import random 
#from os import system, name

def clear():
   # for windows
   if name == 'nt':
      _ = system('cls')


      
def create_board():

    global board
    global num_rows
    global num_cols
    global win_con
    
    board = []

    num_rows = int(input("how many rows: "))
    num_cols = int(input("how many col: "))
    win_con = int(input("how many in row to win do u want: "))
    

    for c in range(num_cols):

        row = []

        #adding zeros to a list a to add to the board list
        for r in range(num_rows):
            row.append("0")


        board.append(row)


    #print(board)
    print_board(board)


def print_board(board):
    #clear
    #print(f"Number of rows is {num_rows}")
    #print(f"Number of cols is {num_cols}")
    print("||", end =" ")

    #prints the numbers ontop
    for c in range(num_cols):
        print(f"{c+1} ||",end =" ")



    #printing the array as a board        
    for row in range(num_rows):
         #to make a new line
        print()

        #printing the line depending on length 
        for c in range(num_cols):
            print("====", end =" ")

        print()
        for col in range(num_cols):
            print("|", end =" ")
            '''
            print(f"col = {col} ",end =" ")
            print(f"and row = {num_rows - (row+1) }",end=" ")
            print(board[col],end =" ")
            '''
            print(f"{board[col][num_rows - (row+1)]} |",end ="")

    
    print()
        
def drop_piece(board,column,player):

    global row_dropped
    
    #starts from the bottom and goes up
    for row_array in range(num_rows):
        #print(row_array)
        if board[column-1][row_array] == "0":
            
            valid_row = row_array
            break
        

    #when an open spot is shown then it takes that and drops the piece
    #print(valid_row)
            
    if player == True:
        board[column-1][valid_row] = "x"

    else:
        board[column-1][valid_row] = "p"

    row_dropped = valid_row
    print(row_dropped)


    #print(board)
    print_board(board)



def check_win(board,elem,column,row):
    row += 1
    print(f"You need {win_con} to win")
    #print(f"col is {column}, row is {row}")
    if vertical_check(board,elem,column,row) == True:
        return True

    if horizontal_check(board,elem,column,row) == True:
        return True

    if diagonal_check(board,elem,column,row) == True:
        return True

    else:
        return False
    
        

def vertical_check(board,elem,column,row):
    vert_bag = []

    #it cycles down  a column and checks if they are all matching
    for r in range(row):
        if board[column-1][r] == elem:
            vert_bag.append(r)

        else:
            break

    #it adds to the bag and when the bag is bigger or same size as win con it returns True
    #print(f"vert bag is {vert_bag}")
    if len(vert_bag) >= win_con:
        return True

    else:
        return False
    

def horizontal_check(board,elem,column,row):
    hor_bag = []

    #it goes to the left then restarts and checks the right side
    c = column
    while c < num_cols -1 :
        if board[c-1][row-1] == elem:
            if c not in hor_bag:
                hor_bag.append(c)

            c += 1

        else:
            break


    c = column
    while 0 <= c:
        if board[c-1][row-1] == elem:
            if c not in hor_bag:
                
                hor_bag.append(c)
            c -= 1

        else:
            break

    #print(f"hor bag is {hor_bag}")
    if len(hor_bag) >= win_con:
        return True

    else:
        return False
            
def diagonal_check(board,elem,column,row):
    diag_up_bag = []

    c = column
    r = row

    #up to down
    while c < num_cols:
        #print(c)
        if board[c-1][r-1] == elem:
            if c not in diag_up_bag:
                diag_up_bag.append(c)

            r += 1
            c += 1

        else:
            break
        
    c = column
    r = row
    while 0 <= c:
        #print(c)
        #print(board[c-1][r-1])
        if board[c-1][r-1] == elem:
            if c not in diag_up_bag:
                diag_up_bag.append(c)

            r -= 1
            c -= 1

        else:
            break


    #down to up
    c = column
    r = row
    diag_down_bag = []

    while c < num_cols:        
        if board[c-1][r-1] == elem:
            if c not in diag_down_bag:
                diag_down_bag.append(c)

            c += 1
            r -= 1

        else:
            break

    c = column
    r = row
    while 0 <= c:
        if board[c-1][r-1] == elem:
            if c not in diag_down_bag:
                diag_down_bag.append(c)

            c -= 1
            r += 1

        else:
            break
                        
    #print(f"diag_up = {diag_up_bag} and diag_down = {diag_down_bag}")
    if len(diag_up_bag) >= win_con:
        return True

    elif len(diag_down_bag) >= win_con:
        return True
        
    else:
        return False

def run_game(board):
    player_start = input("Is the player starting (Y/N): ")
    win = False
    while win == False:

        #if the player starts they go first and it just loops 
        if player_start == "Y":
            col_drop = int(input("what coloumn would u like to drop: "))
            drop_piece(board,col_drop,True)
            winner = check_win(board,"x",col_drop,row_dropped)
            if winner == True:
                print("You win")
                break

            op_drop = int(input("where would person 2 like to drop: "))
            drop_piece(board,op_drop,False)
            op_winner = check_win(board,"p",op_drop,row_dropped)
            if op_winner == True:
                print("You Lose")
                break

        #second person going first
        else:
            op_drop = int(input("where would person 2 like to drop: "))
            drop_piece(board,op_drop,False)
            op_winner = check_win(board,"p",op_drop,row_dropped)
            if op_winner == True:
                print("You Lose")
                break

            col_drop = int(input("what coloumn would u like to drop: "))
            drop_piece(board,col_drop,True)
            winner = check_win(board,"x",col_drop,row_dropped)
            if winner == True:
                print("You win")
                break
                
def valid_input(board):
    valid_col = []
    for c in range(num_cols):
        if board[c][num_rows-1] == "0":
            valid_col.append(c)               
            
    
    
    return random.choice(valid_col)


                               
def ai_game(board):
    win = False
    while win == False:
        player_start = "Y"
        #if the player starts they go first and it just loops 
        if player_start == "Y":
            col_drop = valid_input(board)
            drop_piece(board,col_drop,True)
            winner = check_win(board,"x",col_drop,row_dropped)
            if winner == True:
                print("You win")
                break

            op_drop = valid_input(board)
            drop_piece(board,op_drop,False)
            op_winner = check_win(board,"p",op_drop,row_dropped)
            if op_winner == True:
                print("You Lose")
                break

           
create_board()
run_game(board)

#ai_game(board)
