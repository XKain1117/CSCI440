#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>

#define TOTAL_THREADS 10

struct SharedInfo {
    long long interval;
    long long split_amount;
    long long circle_points;
    long long square_points;
    pthread_mutex_t mutex;
};


//this whole idea is really cool. I had never known about this before.
// Note to self, go lookup more about monte pi stuff 
void* calc_points(void* shared) {
    srand(time(NULL));

    struct SharedInfo* si = (struct SharedInfo*)shared;
    double rand_x, rand_y, origin_dist;
    long long c_points = 0;
    long long s_points = 0;

    pthread_mutex_lock(&si->mutex);
    long long interval = si->interval;
    long long split_amount = si->split_amount;
    pthread_mutex_unlock(&si->mutex);
    
    for (long long i = 0; i < split_amount; i++) {
        rand_x = (double)(rand() % (interval + 1)) / interval;
        rand_y = (double)(rand() % (interval + 1)) / interval;

        origin_dist = rand_x * rand_x + rand_y * rand_y;

        if (origin_dist <= 1) {
            c_points++;
        }
        s_points++;
    }
    pthread_mutex_lock(&si->mutex);
    si->circle_points = c_points;
    si->square_points = s_points;
    pthread_mutex_unlock(&si->mutex);

    return NULL; 
}

int main(int argc, char* argv[]) {

    double pi, cpu_time_used;
    int rc;
    struct SharedInfo* ti = malloc(sizeof(struct SharedInfo));
    ti->circle_points = 0;
    ti->square_points = 0;
    ti->interval = atoi(argv[2]);
    ti->split_amount = ((ti->interval * ti->interval) / TOTAL_THREADS);

    pthread_t threads[TOTAL_THREADS];

    if (pthread_mutex_init(&ti->mutex, NULL) != 0) {
        perror("Error initializing circle mutex");
        exit(EXIT_FAILURE);
    }

    clock_t start, end;
    start = clock();

    for (int t = 0; t < TOTAL_THREADS; t++) {
        rc = pthread_create(&(threads[t]), NULL, calc_points, ti);
        if (rc) {
            printf("ERROR; return code from pthread_create() is %d\n", rc);
            exit(EXIT_FAILURE);
        }
    }

    for (int t = 0; t < TOTAL_THREADS; t++) {
        pthread_join(threads[t], NULL);
    }

    if (ti->square_points > 0) {
        pi = (double)(4 * ti->circle_points) / ti->square_points;
    } else {
        pi = 0.0; 
    }

    end = clock();
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("%f\n", cpu_time_used);
    FILE* outputfile = fopen(argv[argc-2], "w");

    fprintf(outputfile, "Circle: %lld, Square: %lld\n", ti->circle_points, ti->square_points);
    fprintf(outputfile, "\nFinal Estimation of Pi = %lf\n", pi);

    pthread_mutex_destroy(&ti->mutex);
    free(ti);

    fclose(outputfile);

    return 0;
}
