import sys
import multiprocessing
import random
import time

NUM_PROCESSES = 4

def partial_sum(arr, result, mutex):
    local_sum = sum(arr)

    with mutex:
        result.value += local_sum

def main():
    size = int(sys.argv[1])
    array = [random.randint(0, 99) for _ in range(size)]

    processes = []
    result = multiprocessing.Value('i', 0)
    mutex = multiprocessing.Lock()

    elements_per_process = size // NUM_PROCESSES
    remaining_elements = size % NUM_PROCESSES

    start_time = time.time()

    for i in range(NUM_PROCESSES):
        arr_slice = array[i * elements_per_process: (i + 1) * elements_per_process + (remaining_elements if i == NUM_PROCESSES - 1 else 0)]

        process = multiprocessing.Process(target=partial_sum, args=(arr_slice, result, mutex))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total_sum = result.value

    end_time = time.time()
    cpu_time_used = end_time - start_time

    print(cpu_time_used)


    with open(sys.argv[2], "w") as output_file:
        output_file.write(f"The sum of the array elements is: {total_sum}\n")

if __name__ == "__main__":
    main()
