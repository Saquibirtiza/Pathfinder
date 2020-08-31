import numpy as np
import queue

m = [['S',0,0,'B',0,0,0],
    [0,'B',0,0,0,'B',0],
    [0,'B',0,0,0,0,0],
    [0,0,'B','B',0,0,0],
    ['B',0,'B','E',0,'B',0]]

R = 5 #Number of Rows 
C = 7 #Number of Columns

sr = 0 #starting row number
sc = 0 #strating column number
er = 4 #ending row number
ec = 3 #ending column number
rq = queue.Queue(0) #empty row queue
cq = queue.Queue(0) #empty column queue


reached_end = False
visited = np.zeros((5,7), dtype=int)
parent = np.zeros((5,7), dtype=int)

#hard coded for now
parent[0][0] = 10000

#north, south, east, west direction vectors
dr = [-1, +1, 0, 0] 
dc = [0, 0, +1, -1]

#variables to track number of steps
move_count = 0
nodes_current_layer = 1
nodes_next_layer = 0
column = 0
row = 0


def explore_neighbours2(r,c):
    fcost = 0
    minfcost = 10000
    next_cord = []
    global nodes_next_layer
    for i in range(0,4):
        rr = r + dr[i]
        cc = c + dc[i]

        if rr<0 or cc < 0: continue
        if rr >=R or cc >= C: continue
        if visited[rr][cc]: continue
        if m[rr][cc] == 'B': continue

        parent[rr][cc] = (r)*C + c
        visited[rr][cc] = 1

        hcost = abs(er - rr) + abs(ec - cc)
        gcost = abs(rr - sr) + abs(cc - sc)

        fcost = gcost + hcost
        # print(fcost, [rr, cc])
        if fcost <= minfcost:
            minfcost = fcost
            next_cord = [rr, cc]
    # print("-------------")
    return next_cord


    




def solver2():
    global row
    global column
    visited[sr][sc] = 1

    r = sr
    c = sc   

    while True:
        next_point = explore_neighbours2(r,c)
        # print(next_point)
        if m[next_point[0]][next_point[1]] == 'E':
            row = next_point[0]
            column = next_point[1]
            reached_end = True
            break
        r = next_point[0]
        c = next_point[1]

    if reached_end == True:
        return 1
    else:
        return -1
        


output = solver()

if (output != -1):
    val = parent[row][column]
    print("Parent Matrix: ")
    print(parent)
    print("Path:")
    while val != 10000:
        print("(",row,",", column,")")
        column = val%C
        row = int((val-column)/C)
        val = parent[row][column]
print ("( 0 , 0 )")