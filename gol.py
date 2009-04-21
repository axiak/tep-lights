# Conway's Game of life

import dmx
import random

panel1 = dmx.LightPanel("18.224.3.100", 6038, 0, 0)
panel2 = dmx.LightPanel("18.224.3.102", 6038, 0, -3)
panel = dmx.PanelComposite()
panel.addPanel(panel1, 0, 12)
panel.addPanel(panel2, 0, 0)


board1 = [[0 for col in range(0, panel.width)] for row in range(0, panel.height)]
board2 = [[0 for col in range(0, panel.width)] for row in range(0, panel.height)]
board3 = [[0 for col in range(0, panel.width)] for row in range(0, panel.height)]

def initialize_board(board) :
    for r in range(0,len(board)) :
        for c in range(0,len(board[r])) :
            board[r][c] = random.randrange(2)

def generalized_gol(board, count_neighbors, next_state) :
    temp_board = [[v for v in row] for row in board]
    for r in range(0, len(board)) :
        for c in range(0, len(board[r])) :
            count = count_neighbors(board, r, c)
            temp_board[r][c] = next_state(board,count,r,c)
    return temp_board

def loose_gol_count(board, row, col) :
    global board1, board2, board3
    board_2 = None
    board_3 = None
    if board is board1 :
        board_2=board2
        board_3=board3
    elif board is board2 :
        board_2=board1
        board_3=board3
    else :
        board_2=board1
        board_3=board2
    count=0;
    count2=0;
    for r in range(-1,2) :
        for c in range(-1,2) :
            count2+=board_2[(row+r)%len(board)][(col+c)%len(board[row])]
            count2+=board_3[(row+r)%len(board)][(col+c)%len(board[row])]
            if(not (r==0 and c==0)) :
                count += board[(row+r)%len(board)][(col+c)%len(board[row])]
    return count + count2/8

def next_state_loose_gol(board, count, row, col) :
    if board[row][col] == 1 :
        if count==2 or count==3 :
            return 1
        else :
            return 0
    else:
        if count==3 :
            return 1
        else :
            return 0

def update_loose_gol() :
    global board1, board2, board3
    if random.random()<=1.0/40 :
        r = random.random()
        if r <= 1.0/3 :
            board=board1
        elif r <= 2.0/3 :
            board=board2
        else :
            board=board3
        initialize_board(board)
    board1 = generalized_gol(board1, loose_gol_count, next_state_loose_gol)
    board2 = generalized_gol(board2, loose_gol_count, next_state_loose_gol)
    board3 = generalized_gol(board3, loose_gol_count, next_state_loose_gol)

def execute_loose_game_of_life() :
    global panel, board1, board2, board3
    initialize_board(board1)
    initialize_board(board2)
    initialize_board(board3)

    while True :
        for r in range(0, panel.height) :
            for c in range(0, panel.width) :
                panel.lights[r][c].r = board1[r][c]
                panel.lights[r][c].g = board2[r][c]
                panel.lights[r][c].b = board3[r][c]
        update_loose_gol()
        panel.outputAndWait(10)

execute_loose_game_of_life()
