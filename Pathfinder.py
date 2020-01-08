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
rq = queue.Queue(0) #empty row queue
cq = queue.Queue(0) #empty column queue

reached_end = False
visited = np.zeros((5,7), dtype=int)

#north, south, east, west direction vectors
dr = [-1, +1, 0, 0] 
dc = [0, 0, +1, -1]

#variables to track number of steps
move_count = 0
nodes_current_layer = 1
nodes_next_layer = 0


def explore_neighbours(r,c):
    global nodes_next_layer
    for i in range(0,4):
        rr = r + dr[i]
        cc = c + dc[i]

        if rr<0 or cc < 0: continue
        if rr >=R or cc >= C: continue

        if visited[rr][cc]: continue
        if m[rr][cc] == 'B': continue

        rq.put(rr)
        cq.put(cc)
        visited[rr][cc] = 1
        nodes_next_layer += 1




def solver():
    rq.put(sr)
    cq.put(sc)
    visited[sr][sc] = 1
    global nodes_current_layer
    global move_count
    global nodes_next_layer

    while rq.qsize() > 0:
        r = rq.get()
        c = cq.get()
        if m[r][c] == 'E':
            reached_end = True
            break
        explore_neighbours(r,c)
        nodes_current_layer -= 1
        if nodes_current_layer == 0:
            nodes_current_layer = nodes_next_layer
            nodes_next_layer = 0
            move_count += 1
    if reached_end:
        return move_count
    return -1
          

output = solver()
print(output)


