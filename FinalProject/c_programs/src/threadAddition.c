#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define MAX_SIZE 1000
#define NUM_THREADS 4

typedef struct {
    int *arr;
    int size;
    int result;
    pthread_mutex_t *mutex;
} ThreadInfo;

void *partialSum(void *info) {
    ThreadInfo *data = (ThreadInfo *)info;
    
    int thisSum = 0;

    for (int i = 0; i < data->size; i++) {
        thisSum += data->arr[i];
    }

    pthread_mutex_lock(data->mutex);
    data->result += thisSum;
    pthread_mutex_unlock(data->mutex);

    pthread_exit(NULL);
}

int main(int argc, char* argv[]) {
    int size = atoi(argv[1]);
    int array[size];
    pthread_t threads[NUM_THREADS];
    ThreadInfo threadInfo[NUM_THREADS];
    pthread_mutex_t mutex;
    FILE* outputFile = fopen(argv[2], "w");

    for (int i = 0; i < size; ++i) {
        array[i] = rand() % 100;
    }

    

    int elementsPerThread = size / NUM_THREADS;
    int elementsLeft = size % NUM_THREADS;

    pthread_mutex_init(&mutex, NULL);

    clock_t start = clock();

    for (int i = 0; i < NUM_THREADS; ++i) {
        threadInfo[i].arr = array + i * elementsPerThread;

        //This is for if the number is not evenly divsible by the number of threads, the last one will be given the rest
        // Got this from chat gpt, cause i couldnt figure out how to do its
        threadInfo[i].size = (i == NUM_THREADS - 1) ? elementsPerThread + elementsLeft : elementsPerThread;
        threadInfo[i].result = 0;
        threadInfo[i].mutex = &mutex;

        pthread_create(&threads[i], NULL, partialSum, &threadInfo[i]);
    }

    for (int i = 0; i < NUM_THREADS; ++i) {
        pthread_join(threads[i], NULL);
    }

    int sum = 0;
    for (int i = 0; i < NUM_THREADS; ++i) {
        sum += threadInfo[i].result;
    }

    clock_t end = clock();
    double cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("%f\n", cpu_time_used);

    fprintf(outputFile, "sum: %d\n", sum);

    pthread_mutex_destroy(&mutex);

    return 0;
}
