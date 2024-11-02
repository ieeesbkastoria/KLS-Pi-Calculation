from mpi4py import MPI
import random
import time
import os

def get_raspberry_pi_temperature():
    """Retrieves the temperature of the Raspberry Pi by executing a system command."""
    temp = os.popen("vcgencmd measure_temp").readline()
    return temp.replace("temp=", "").replace("'C\n", "°C")

def estimate_pi_worker(num_samples):
    """Count how many points fall inside the unit circle."""
    count_inside_circle = 0
    for _ in range(num_samples):
        x, y = random.random(), random.random()
        if x**2 + y**2 <= 1:
            count_inside_circle += 1
    return count_inside_circle

def main():
    # Initialize the MPI environment
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()  # Get the rank (ID) of the process
    size = comm.Get_size()  # Get the total number of processes

    # Configuration
    total_samples = 100000000  # Total number of samples (e.g., 100 million)
    samples_per_process = total_samples // size  # Divide samples evenly across processes

    # Start timing
    start_time = time.time()

    # Each process estimates pi for its chunk of the total samples
    inside_circle = estimate_pi_worker(samples_per_process)

    # Gather the results from all processes and sum them at rank 0 (master process)
    total_inside_circle = comm.reduce(inside_circle, op=MPI.SUM, root=0)

    # Rank 0 process computes the final estimate of Pi
    if rank == 0:
        pi_estimate = (4.0 * total_inside_circle) / total_samples
        end_time = time.time()
        execution_time = end_time - start_time

        # Display results
        temperature = get_raspberry_pi_temperature()
        print(f"The temperature of the Raspberry Pi is: {temperature}")
        print(f"Estimated Pi: {pi_estimate}")
        print(f"Execution time: {execution_time} seconds")

        # Save results to a file
        with open("execution_times.txt", "a") as file:
            file.write(f"Num Samples: {total_samples}, Execution Time: {execution_time}, Temperature: {temperature}, Pi Estimate: {pi_estimate}\n")

if __name__ == "__main__":
    main()

