#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>

struct Matrix {
    int rows;
    int cols;
    double** data;
};

struct ThreadData {
    struct Matrix* result;
    struct Matrix* matrix1;
    struct Matrix* matrix2;
    int start_block;
    int end_block;
    pthread_mutex_t* mutex;
};

void initializeMatrix(struct Matrix* matrix) {
    matrix->data = (double**)malloc(matrix->rows * sizeof(double*));
    for (int i = 0; i < matrix->rows; ++i) {
        matrix->data[i] = (double*)malloc(matrix->cols * sizeof(double));
        for (int j = 0; j < matrix->cols; ++j) {
            matrix->data[i][j] = (double)rand() / RAND_MAX;
        }
    }
}

void* multiplyBlocks(void* arg) {
    struct ThreadData* data = (struct ThreadData*)arg;

    for (int block_i = data->start_block; block_i < data->end_block; ++block_i) {
        for (int block_j = 0; block_j < data->matrix2->cols; ++block_j) {
            double local_accumulator = 0.0;

            for (int k = 0; k < data->matrix1->cols; ++k) {
                local_accumulator += data->matrix1->data[block_i][k] * data->matrix2->data[k][block_j];
            }

            pthread_mutex_lock(data->mutex);
            data->result->data[block_i][block_j] = local_accumulator;
            pthread_mutex_unlock(data->mutex);

        }
    }

    return NULL;
}

void multiplyMatrices(struct Matrix* result, struct Matrix* matrix1, struct Matrix* matrix2, int num_threads, char* argv[]) {
    pthread_t threads[num_threads];
    struct ThreadData threadData[num_threads];
    pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

    int blocks_per_thread = result->rows / num_threads;

    for (int i = 0; i < num_threads; ++i) {
        threadData[i].result = result;
        threadData[i].matrix1 = matrix1;
        threadData[i].matrix2 = matrix2;
        threadData[i].start_block = i * blocks_per_thread;
        threadData[i].end_block = (i == num_threads - 1) ? result->rows : (i + 1) * blocks_per_thread;
        threadData[i].mutex = &mutex;

        pthread_create(&threads[i], NULL, multiplyBlocks, (void*)&threadData[i]);
    }

    clock_t start = clock();

    for (int i = 0; i < num_threads; ++i) {
        pthread_join(threads[i], NULL);
    }

    clock_t end = clock();
    double cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;

    FILE* output_file = fopen(argv[2], "w");
    if (output_file == NULL) {
        perror("Error opening output file");
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < result->rows; ++i) {
        for (int j = 0; j < result->cols; ++j) {
            fprintf(output_file, "%lf ", result->data[i][j]);
        }
        fprintf(output_file, "\n");
    }

    fclose(output_file);

    printf("%f\n", cpu_time_used);
}

int main(int argc, char* argv[]) {
    srand(time(NULL));

    struct Matrix matrix1, matrix2, result;

    matrix1.rows = atoi(argv[1]);
    matrix1.cols = atoi(argv[1]);
    initializeMatrix(&matrix1);

    matrix2.rows = atoi(argv[1]);
    matrix2.cols = atoi(argv[1]);
    initializeMatrix(&matrix2);

    result.rows = matrix1.rows;
    result.cols = matrix2.cols;
    result.data = (double**)malloc(result.rows * sizeof(double*));
    for (int i = 0; i < result.rows; ++i) {
        result.data[i] = (double*)malloc(result.cols * sizeof(double));
    }

    multiplyMatrices(&result, &matrix1, &matrix2, 20, argv);

    for (int i = 0; i < matrix1.rows; ++i) {
        free(matrix1.data[i]);
    }
    free(matrix1.data);

    for (int i = 0; i < matrix2.rows; ++i) {
        free(matrix2.data[i]);
    }
    free(matrix2.data);

    for (int i = 0; i < result.rows; ++i) {
        free(result.data[i]);
    }
    free(result.data);

    return 0;
}
