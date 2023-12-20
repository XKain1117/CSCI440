import multiprocessing
import random
import time
import sys
import logging

TOTAL_THREADS = 10

logging.basicConfig(level=logging.DEBUG, filename='logfile.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

class SharedInfo:
    def __init__(self, interval, split_amount):
        self.interval = multiprocessing.Value('i', interval)
        self.split_amount = multiprocessing.Value('i', split_amount)
        self.circle_points = multiprocessing.Value('i', 0)
        self.square_points = multiprocessing.Value('i', 0)
        self.lock = multiprocessing.Lock()

def calc_points(shared):
    seed = multiprocessing.current_process().pid
    random.seed(seed)
    c_points = 0
    s_points = 0

    with shared.lock:
        interval = shared.interval.value
        split_amount = shared.split_amount.value

    for _ in range(split_amount):
        rand_x = random.uniform(0, interval) / interval
        rand_y = random.uniform(0, interval) / interval

        origin_dist = rand_x**2 + rand_y**2

        if origin_dist <= 1:
            c_points += 1
        s_points += 1

    with shared.lock:
        shared.circle_points.value += c_points
        shared.square_points.value += s_points
        logging.debug(f'{shared.square_points.value}')

def main():
    pi = 0.0
    interval = int(sys.argv[1])
    split_amount = (interval * interval) // TOTAL_THREADS

    shared_info = SharedInfo(interval, split_amount)

    processes = []

    start_time = time.time()

    for _ in range(TOTAL_THREADS):
        process = multiprocessing.Process(target=calc_points, args=(shared_info,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    if shared_info.square_points.value > 0:
        pi = (4 * shared_info.circle_points.value) / shared_info.square_points.value

    end_time = time.time()
    cpu_time_used = end_time - start_time
    print(cpu_time_used)

    with open(sys.argv[2], "w") as outputfile:
        outputfile.write(f"Circle: {shared_info.circle_points.value}, Square: {shared_info.square_points.value}\n")
        outputfile.write(f"\nFinal Estimation of Pi = {pi}\n")

if __name__ == "__main__":
    main()
