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
