import subprocess
import os
import numpy as np
from prettytable import PrettyTable


time_output = "time.txt"

threadAdditiontimes = {
    "small" : [],
    "medium" : [],
    "large" : []
}
threadMontetimes = {
    "small" : [],
    "medium" : [],
    "large" : []
}
threadMatrixtimes = {
    "small" : [],
    "medium" : [],
    "large" : []
}

pythonAdditiontimes = {
    "small" : [],
    "medium" : [],
    "large" : []
}
pythonMontetimes = {
    "small" : [],
    "medium" : [],
    "large" : []
}
pythonMatrixtimes = {
    "small" : [],
    "medium" : [],
    "large" : []
}

sizes = ["small", "medium", "large"]

add_outputs = ["results/Addition/small.txt", "results/Addition/medium.txt", "results/Addition/large.txt"]
add_inputs = [10000, 50000, 1000000]

matrix_inputs = [50, 100, 250]
matrix_outputs = ["results/Matrix/small.txt", "results/Matrix/medium.txt", "results/Matrix/large.txt"]

monte_inputs = [500, 1000, 1500]
monte_outputs = ["results/Monte/small.txt","results/Monte/medium.txt", "results/Monte/large.txt"]


finalDataPython = {
    "Addition" : {
        "small" : {
            "SEM" : 0,
            "MOE" : 0
        },
        "medium" : {
            "SEM" : 0,
            "MOE" : 0
        },
        "large" : {
            "SEM" : 0,
            "MOE" : 0
        }
    },
    "Matrix" : {
        "small" : {
            "SEM" : 0,
            "MOE" : 0
        },
        "medium" : {
            "SEM" : 0,
            "MOE" : 0
        },
        "large" : {
            "SEM" : 0,
            "MOE" : 0
        }
    },
    "Monte" : {
        "small" : {
            "SEM" : 0,
            "MOE" : 0
        },
        "medium" : {
            "SEM" : 0,
            "MOE" : 0
        },
        "large" : {
            "SEM" : 0,
            "MOE" : 0
        }
    }
}
finalDataC = {
    "Addition" : {
        "small" : {
            "SEM" : 0,
            "MOE" : 0
        },
        "medium" : {
            "SEM" : 0,
            "MOE" : 0
        },
        "large" : {
            "SEM" : 0,
            "MOE" : 0
        }
    },
    "Matrix" : {
        "small" : {
            "SEM" : 0,
            "MOE" : 0
        },
        "medium" : {
            "SEM" : 0,
            "MOE" : 0
        },
        "large" : {
            "SEM" : 0,
            "MOE" : 0
        }
    },
    "Monte" : {
        "small" : {
            "SEM" : 0,
            "MOE" : 0
        },
        "medium" : {
            "SEM" : 0,
            "MOE" : 0
        },
        "large" : {
            "SEM" : 0,
            "MOE" : 0
        }
    }
}
def calc_err_generic(times, finalData, name, sizes):
    table = PrettyTable()
    for size in sizes:
        if len(times[size]) <= 1:
            # Handle the case where there's not enough data for meaningful calculations
            finalData[name][size]["SEM"] = 0
            finalData[name][size]["MOE"] = 0
        else:
            sem = np.std(times[size]) / np.sqrt(len(times[size]))
            confidence_multiplier = 1.96
            margin_of_error = confidence_multiplier * sem

            sem *= 100
            margin_of_error *= 100

            finalData[name][size]["SEM"] = round(sem, 4)
            finalData[name][size]["MOE"] = round(margin_of_error, 4)

    table.title = f"{name} Performance Metrics"

    # Define the field names
    table.field_names = ["Run Size", "SEM", "MOE"]

    # Add rows to the table
    for size, metrics in zip(sizes, finalData[name].values()):
        table.add_row([size, metrics["SEM"], metrics["MOE"]])

    # Print the table
    print(table)


# Function to run 'make clean' and 'make' commands
def build_program(makefile_path):
    subprocess.run(["make", "clean"], cwd=makefile_path)
    subprocess.run(["make"], cwd=makefile_path)

# Specify the path to your Makefile


# Function to run a command from a specific directory
def run_command(command, directory):
    process = subprocess.Popen(command, cwd=directory, stdout=subprocess.PIPE, text=True)
    output = process.communicate()[0]
    return output

def run_c_programs():
    makefile_path = "c_programs/"
    # Run 'make clean' and 'make' at the beginning
    build_program(makefile_path)
    print("C Programs:")
    print("====================================================")

    print("Beginning Monte Runs")
    # Monte Carlo Pi program
    print("small.txt")
    for i in range(20):
        monte_command = ["./threadMonte", str(i), str(monte_inputs[0]), monte_outputs[0], time_output]
        output = run_command(monte_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        threadMontetimes["small"].append(elapsed_time)
        print(f"Done with run {i}")
    print("medium.txt")
    for i in range(20):
        monte_command = ["./threadMonte", str(i), str(monte_inputs[1]), monte_outputs[1], time_output]
        output = run_command(monte_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        threadMontetimes["medium"].append(elapsed_time)
        print(f"Done with run {i}")
    print("large.txt")
    for i in range(20):
        monte_command = ["./threadMonte", str(i), str(monte_inputs[2]), monte_outputs[2], time_output]
        output = run_command(monte_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        threadMontetimes["large"].append(elapsed_time)
        print(f"Done with run {i}")

    print("====================================================")

    print("Beginning Addition Runs")
    print("====================================================")
    print("small.txt")
    for i in range(20):
        add_command = ["./threadAddition", str(add_inputs[0]), add_outputs[0]]
        output = run_command(add_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        threadAdditiontimes["small"].append(elapsed_time)
        print(f"Done with run {i}")

    print("medium.txt")
    for i in range(20):
        add_command = ["./threadAddition", str(add_inputs[1]), add_outputs[1]]
        output = run_command(add_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        threadAdditiontimes["medium"].append(elapsed_time)
        print(f"Done with run {i}")

    print("large.txt")
    for i in range(20):
        add_command = ["./threadAddition", str(add_inputs[2]), add_outputs[2]]
        output = run_command(add_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        threadAdditiontimes["large"].append(elapsed_time)
        print(f"Done with run {i}")

    
    #Matrix Mult program
    print("Beginning Matrix Runs")
    print("====================================================")
    table = PrettyTable()
    #Matrix Multiplication code
    print("small.txt")
    for i in range(20):
        matrix_command = ["./threadMatrixMult", str(matrix_inputs[0]), matrix_outputs[0]]
        output = run_command(matrix_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        threadMatrixtimes["small"].append(elapsed_time)
        print(f"Done with run {i}")
    print("medium.txt")
    for i in range(20):
        matrix_command = ["./threadMatrixMult", str(i), str(matrix_inputs[1]), matrix_outputs[1]]
        output = run_command(matrix_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        threadMatrixtimes["medium"].append(elapsed_time)
        print(f"Done with run {i}")
    print("large.txt")
    for i in range(20):
        matrix_command = ["./threadMatrixMult", str(matrix_inputs[2]), matrix_outputs[2]]
        output = run_command(matrix_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        threadMatrixtimes["large"].append(elapsed_time)
        print(f"Done with run {i}")



def run_python_programs():
    makefile_path = "python_programs/"
    print("Python Programs:")
    print("====================================================")

    # Monte Carlo Pi program
    print("Beginning Monte Runs")
    print("small.txt")
    for i in range(20):
        monte_command = ["python3", "multiProcMonte.py", str(monte_inputs[0]), monte_outputs[0]]
        output = run_command(monte_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        pythonMontetimes["small"].append(elapsed_time)
        print(f"Done with run {i}")

    print("medium.txt")
    for i in range(20):
        monte_command = ["python3", "multiProcMonte.py", str(monte_inputs[1]), monte_outputs[1]]
        output = run_command(monte_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        pythonMontetimes["medium"].append(elapsed_time)
        print(f"Done with run {i}")

    print("large.txt")
    for i in range(40):
        monte_command = ["python3", "multiProcMonte.py", str(monte_inputs[2]), monte_outputs[2]]
        output = run_command(monte_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        pythonMontetimes["large"].append(elapsed_time)
        print(f"Done with run {i}")
    print("====================================================")

    #Matrix Multiplication program
    print("Beginning Matrix Runs")
    print("small.txt")
    for i in range(20):
        matrix_command = ["python3", "multiProcMatrixMult.py", str(matrix_inputs[0]), matrix_outputs[0]]
        output = run_command(matrix_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        pythonMatrixtimes["small"].append(elapsed_time)
        print(f"Done with run {i}")

    print("medium.txt")
    for i in range(20):
        matrix_command = ["python3", "multiProcMatrixMult.py", str(matrix_inputs[1]), matrix_outputs[1]]
        output = run_command(matrix_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        pythonMatrixtimes["medium"].append(elapsed_time)
        print(f"Done with run {i}")

    print("large.txt")
    for i in range(20):
        matrix_command = ["python3", "multiProcMatrixMult.py", str(matrix_inputs[2]), matrix_outputs[2]]
        output = run_command(matrix_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        pythonMatrixtimes["large"].append(elapsed_time)
        print(f"Done with run {i}")
    print("====================================================")

    # Addition program
    print("Beginning Addition Runs")
    print("small.txt")
    for i in range(20):
        add_command = ["python3", "multiProcAddition.py", str(add_inputs[0]), add_outputs[0]]
        output = run_command(add_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        pythonAdditiontimes["small"].append(elapsed_time)
        print(f"Done with run {i}")

    print("medium.txt")
    for i in range(20):
        add_command = ["python3", "multiProcAddition.py", str(add_inputs[1]), add_outputs[1]]
        output = run_command(add_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        pythonAdditiontimes["medium"].append(elapsed_time)
        print(f"Done with run {i}")

    print("large.txt")
    for i in range(20):
        add_command = ["python3", "multiProcAddition.py", str(add_inputs[2]), add_outputs[2]]
        output = run_command(add_command, os.path.join(makefile_path))
        elapsed_time = float(output.strip())
        pythonAdditiontimes["large"].append(elapsed_time)
        print(f"Done with run {i}")
    print("====================================================")

run_c_programs()
run_python_programs()

calc_err_generic(threadMatrixtimes, finalDataC, "Matrix", sizes)
calc_err_generic(threadMontetimes, finalDataC, "Monte", sizes)
calc_err_generic(threadAdditiontimes, finalDataC, "Addition", sizes)
calc_err_generic(pythonMatrixtimes, finalDataPython, "Matrix", sizes)
calc_err_generic(pythonMontetimes, finalDataPython, "Monte", sizes)
calc_err_generic(pythonAdditiontimes, finalDataPython, "Addition", sizes)

