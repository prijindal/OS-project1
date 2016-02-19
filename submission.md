#### Name - Priyanshu Jindal
#### Reg. No. - 14BCE0607
#### Project Code - CSE222P163

#### Question 1
Exercise 4.23 asked you to design a program using OpenMP that
estimated  using the Monte Carlo technique. Examine your solution to
that program looking for any possible race conditions. If you identify a
race condition, protect against it using the strategy outlined in Section
5.10.2.

- Estimating Pi using Monte Carlo Technique by parallel execution with use of OpenMP Framework
- Identifying and protecting against any race conditions

**Solution `in C code`**
```
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
  long incircle = 0;
  long points_per_thread = 1000;
  int thread_count = 16;
  double total_points = (double)points_per_thread*thread_count;

  #pragma omp parallel shared(incircle) num_threads(thread_count)
  {
    long incircle_thread = 0;
    unsigned int myseed = omp_get_thread_num();
    long i;
    for(i = 0;i < points_per_thread;++i) {
      double x = rand_r(&myseed)/((double)RAND_MAX + 1) * 2.0 - 1.0;
      double y = rand_r(&myseed)/((double)RAND_MAX + 1) * 2.0 - 1.0;

      if(x * x + y* y < 1) {
        incircle_thread++;
      }
    }
    #pragma omp critical
    {
      incircle+=incircle_thread;
    }
  }

  printf("Pi: %f\n", (4. * (double)incircle) / (total_points));
};
```

**Output 1**
![Output 1](pi1.png)

**Output 2**
![Output 2](pi2.png)


#### Question 2
- Make a Sudoku solution validator using multithreading
- Make 9 threads for each Box
- Make 1 thread to verify rows and 1 for column

**Solution `in Python code`**
```
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

```

**Sample Output 1**
- When Sudoku solution is correct

![Output 1](/sudoku1.png)

**Sample Output 2**
- When Sudoku solution is incorrect

![Output 2](/sudoku2.png)
