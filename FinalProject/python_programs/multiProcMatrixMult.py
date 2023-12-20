import sys
import multiprocessing
import random
import time

class Matrix:
    def __init__(self, rows, cols, lower_limit=0, upper_limit=1):
        self.rows = rows
        self.cols = cols
        self.data = [
            [random.uniform(lower_limit, upper_limit) for _ in range(cols)]
            for _ in range(rows)
        ]

class ThreadData:
    def __init__(self, result, matrix1, matrix2, start_block, end_block, mutex):
        self.result = result
        self.matrix1 = matrix1
        self.matrix2 = matrix2
        self.start_block = start_block
        self.end_block = end_block
        self.mutex = mutex

def multiply_blocks(data):
    for block_i in range(data.start_block, data.end_block):
        for block_j in range(data.matrix2.cols):
            local_accumulator = 0.0

            for k in range(data.matrix1.cols):
                local_accumulator += data.matrix1.data[block_i][k] * data.matrix2.data[k][block_j]

            with data.mutex:
                data.result.data[block_i][block_j] = local_accumulator

def multiply_matrices(result, matrix1, matrix2, num_processes, argv):
    processes = []
    mutex = multiprocessing.Lock()

    blocks_per_process = result.rows // num_processes

    for i in range(num_processes):
        data = ThreadData(result, matrix1, matrix2, i * blocks_per_process, (i + 1) * blocks_per_process, mutex)
        process = multiprocessing.Process(target=multiply_blocks, args=(data,))
        processes.append(process)
        process.start()

    start_time = time.time()

    for process in processes:
        process.join()

    end_time = time.time()
    cpu_time_used = end_time - start_time

    with open(argv[2], "w") as output_file:
        for i in range(result.rows):
            output_file.write(" ".join(map(str, result.data[i])) + "\n")

    print(cpu_time_used)

def main():
    random.seed()

    matrix_size = int(sys.argv[1])
    matrix1 = Matrix(matrix_size, matrix_size, 0, 100)
    matrix2 = Matrix(matrix_size, matrix_size, 0, 100)
    result = Matrix(matrix_size, matrix_size)

    multiply_matrices(result, matrix1, matrix2, 20, sys.argv)

if __name__ == "__main__":
    main()
