import tkinter as tk
import sys

startingX = 0
startingY = 0

class KnightsTour:
    def __init__(self, width, height):
        self.w = width
        self.h = height

        self.board = []
        self.generate_board()

    def generate_board(self):
        #Creates a nested list to represent the game board
        
        for i in range(self.h):
            self.board.append([0]*self.w)

    def print_board(self, path):
        #Trace path with line
        for i in range(len(path)-1):
            board.canvas.create_line(path[i][0] * 30 +16, path[i][1] * 30 +16, path[i+1][0] * 30 +16, path[i+1][1] * 30 +16, fill ='red', width = 2.0)

    def generate_legal_moves(self, cur_pos):
        #Define legal moves for the knight to take next
 
        possible_pos = []
        move_offsets = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                        (2, 1), (2, -1), (-2, 1), (-2, -1)]

        for move in move_offsets:
            new_x = cur_pos[0] + move[0]
            new_y = cur_pos[1] + move[1]

            #Check that new possibility is within the grid
            if (new_x >= self.h):
                continue
            elif (new_x < 0):
                continue
            elif (new_y >= self.w):
                continue
            elif (new_y < 0):
                continue
            else:
                possible_pos.append((new_x, new_y))

        return possible_pos

    def sort_neighbors(self, to_visit):
        #Sort possible choices by least amount of moves to spot
        neighbor_list = self.generate_legal_moves(to_visit)
        empty_neighbors = []

        for neighbor in neighbor_list:
            np_value = self.board[neighbor[0]][neighbor[1]]
            #if position is not taken append
            if np_value == 0:
                empty_neighbors.append(neighbor)

        scores = []
        for empty in empty_neighbors:
            score = [empty, 0]
            moves = self.generate_legal_moves(empty)
            for m in moves:
                if self.board[m[0]][m[1]] == 0:
                    score[1] += 1
            scores.append(score)
        #sort by neighbor_scores
        scores_sort = sorted(scores, key = lambda s: s[1])
        sorted_neighbors = [s[0] for s in scores_sort]
        return sorted_neighbors

    def tour(self, n, path, to_visit):
        """
        Recursive definition of knights tour. Inputs are as follows:
        n = current depth of tree
        path = current path taken
        to_visit = node to visit
        """
        self.board[to_visit[0]][to_visit[1]] = n
        path.append(to_visit) #append the newest vertex to the current point
        
        #if every grid is filled
        if n == self.w * self.h: 
            self.print_board(path)
            print( "Complete")
            sys.exit(1)

        else:
            sorted_neighbors = self.sort_neighbors(to_visit)
            for neighbor in sorted_neighbors:
                self.tour(n+1, path, neighbor)
                
            #If we exit this loop, all neighbors failed so we reset
            self.board[to_visit[0]][to_visit[1]] = 0
            try:
                path.pop()
                print( "Going back to: ", path[-1])
            except IndexError:
                print( "No path found")
                sys.exit(1)


class GameBoard(tk.Frame):

    def __init__(self, parent, rows=8, columns=8, size=32, color1="white"):
        self.rows = rows
        self.columns = columns
        #SIZE IN PIXELS ugh why
        self.size = size
        self.color1 = color1
        self.color1 = color1
        self.pieces = {}

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height)

        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        #CREATES BOARD
        self.canvas.bind("<Configure>", self.refresh)

        solveButton = tk.Button(self, text = "Solve", command =lambda: self.solveKnightTour(startingX,startingY), anchor = 's')
        solveButton.configure(width = 10, activebackground = "#33B5E5", relief = 'raised')
        solveButton_window = self.canvas.create_window(10, 10, anchor='s', window=solveButton)
        solveButton.pack(side='bottom')

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color1
        for row in range(self.rows):
            color = self.color1 if color == self.color1 else self.color1
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size 
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color1 else self.color1
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def solveKnightTour(self, x =1 , y=1):
        print(x, y)
        kt = KnightsTour(8, 8)
        kt.tour(1, [], (x,y))
        kt.print_board()
    
imagedata = '''
    R0lGODlhGQAcAHAAACH5BAEAAPwALAAAAAAZABwAhwAAAAAAMwAAZgAAmQAAzAA
    A/wArAAArMwArZgArmQArzAAr/wBVAABVMwBVZgBVmQBVzABV/wCAAACAMwCAZg
    CAmQCAzACA/wCqAACqMwCqZgCqmQCqzACq/wDVAADVMwDVZgDVmQDVzADV/wD/A
    AD/MwD/ZgD/mQD/zAD//zMAADMAMzMAZjMAmTMAzDMA/zMrADMrMzMrZjMrmTMrz
    DMr/zNVADNVMzNVZjNVmTNVzDNV/zOAADOAMzOAZjOAmTOAzDOA/zOqADOqMzOqZ
    jOqmTOqzDOq/zPVADPVMzPVZjPVmTPVzDPV/zP/ADP/MzP/ZjP/mTP/zDP//2YAA
    GYAM2YAZmYAmWYAzGYA/2YrAGYrM2YrZmYrmWYrzGYr/2ZVAGZVM2ZVZmZVmWZVz
    GZV/2aAAGaAM2aAZmaAmWaAzGaA/2aqAGaqM2aqZmaqmWaqzGaq/2bVAGbVM2bVZ
    mbVmWbVzGbV/2b/AGb/M2b/Zmb/mWb/zGb//5kAAJkAM5kAZpkAmZkAzJkA/5krA
    JkrM5krZpkrmZkrzJkr/5lVAJlVM5lVZplVmZlVzJlV/5mAAJmAM5mAZpmAmZmAz
    JmA/5mqAJmqM5mqZpmqmZmqzJmq/5nVAJnVM5nVZpnVmZnVzJnV/5n/AJn/M5n/Zpn
    /mZn/zJn//8wAAMwAM8wAZswAmcwAzMwA/8wrAMwrM8wrZswrmcwrzMwr/8xVAMxV
    M8xVZsxVmcxVzMxV/8yAAMyAM8yAZsyAmcyAzMyA/8yqAMyqM8yqZsyqmcyqzMyq
    /8zVAMzVM8zVZszVmczVzMzV/8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Am
    f8AzP8A//8rAP8rM/8rZv8rmf8rzP8r//9VAP9VM/9VZv9Vmf9VzP9V//+AAP+AM/
    +AZv+Amf+AzP+A//+qAP+qM/+qZv+qmf+qzP+q///VAP/VM//VZv/Vmf/VzP/V///
    /AP//M///Zv//mf//zP///wAAAAAAAAAAAAAAAAjfAPcJFDhpoMGDCA+KuQGAWCY0
    C2PEyJQw4SQAGIkpUzaJIUaKFQeiwUgSwMR9xEgWDBmjpMsY+zKZvFFRpsubBU2CP
    HizJwAx+wCsUHbQpk+XaILCNHjUZz2GQAUqa+ozKFGBYnwaOKqs5dWeQZtOBCDQY
    8mBJLfeJCaGqEuaaIX6zASyJUaEdn2yjUsM4U21H3eGvLmiJLS+IfddbJo47tGVibO
    mfZk4UwyzPi9HRbjYZeGbcBEa7Qn450FlGiVTxRhj49XSf6kKzFsS9tHZRz/LBbsv
    r4HPn9VupY0xIAA7
    '''                   

if __name__ == "__main__":
    root = tk.Tk()
    root.title("The Knight's Tour")
    board = GameBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    player1 = tk.PhotoImage(data=imagedata)

    def callback(event):

        global startingX
        global startingY
        #FOR X'S
        if event.x >= 0 and event.x <=32:
            event.x = 0
        elif event.x > 32 and event.x <= 64:
            event.x = 1
        elif event.x > 64 and event.x <=96:
            event.x = 2
        elif event.x > 96 and event.x <= 128:
            event.x = 3
        elif event.x > 128 and event.x <=160:
            event.x = 4
        elif event.x > 160 and event.x <= 192:
            event.x = 5
        elif event.x > 192 and event.x <= 224:
            event.x = 6
        elif event.x > 224 and event.x <= 256:
            event.x = 7

        #FOR Y'S
        if event.y >= 0 and event.y <=32:
            event.y = 0
        elif event.y > 32 and event.y <= 64:
            event.y = 1
        elif event.y > 64 and event.y <=96:
            event.y = 2
        elif event.y > 96 and event.y <= 128:
            event.y = 3
        elif event.y > 128 and event.y <=160:
            event.y = 4
        elif event.y > 160 and event.y <= 192:
            event.y = 5
        elif event.y > 192 and event.y <= 224:
            event.y = 6
        elif event.y > 224 and event.y <= 256:
            event.y = 7
            
        startingX = event.x
        startingY = event.y
        
        #DRAWING LINES
        board.addpiece("player1", player1, event.y, event.x)
        
    board.canvas.bind("<Button-1>", callback)

    root.mainloop()
