from threading import Thread, Lock
from Queue import Queue

mutex = Lock()
answers = [0] * 11
sudoku = [
            [1,2,3,9,5,6,7,8,9],
            [4,5,6,7,8,9,1,2,3],
            [7,8,9,1,2,3,4,5,6],
            [2,3,4,5,1,7,8,9,1],
            [5,6,7,8,9,1,2,3,4],
            [8,6,1,2,3,4,5,6,7],
            [3,4,5,6,7,8,9,1,2],
            [6,7,8,9,1,2,3,4,5],
            [9,1,2,3,4,5,6,7,8]
        ]

def check_square(index):
    start_column = (index%3)*3
    end_column = start_column + 3
    start_row = (index/3)*3
    end_row = start_row + 3
    values = [0] * 10

    i = start_column
    j = start_row
    while(i < end_column):
        while(j < end_row):
            values[sudoku[i][j]]+=1
            j+=1
        j = start_row
        i+=1
    # print(values)
    k = True
    for i in range(1,10):
        if values[i] != 1:
            k = False
    mutex.acquire()
    if(k == True):
        answers[index] = 1
    mutex.release()

def check_row(index):
    k = True
    for i in range(9):
        # Check if ith row has all elements
        values = [0] * 10
        for j in range(9):
            values[sudoku[i][j]]+=1
        for i in range(1,10):
            if values[i] != 1:
                k = False
    if(k == True):
        answers[index] = 1
    # print(values)
def check_column(index):
    k = True
    for i in range(9):
        # Check if ith row has all elements
        values = [0] * 10
        for j in range(9):
            values[sudoku[j][i]]+=1
        for i in range(1,10):
            if values[i] != 1:
                k = False
    if(k == True):
        answers[index] = 1
    # print(values)

if __name__ == "__main__":

    print("Sample Sudoku to be checked: ")
    for i in sudoku:
        print i

    jobs = []
    for i in range(9):
        thread = Thread(target = check_square, args=(i,))
        jobs.append(thread)
    thread = Thread(target = check_row, args=(9,))
    jobs.append(thread)

    thread = Thread(target = check_column, args=(10,))
    jobs.append(thread)

    for j in jobs:
        j.start()
    for j in jobs:
        j.join()

    k = True
    for i in answers:
        if i != 1:
            k = False
    if(k==True):
        print("Correct Solution")
    else:
        print("Error in the Solution")
