import random
import time
import multiprocessing
import os

def get_raspberry_pi_temperature():
    # Reads the temperature from the Raspberry Pi's system file
    temp = os.popen("vcgencmd measure_temp").readline()
    # Cleans up the result and returns it
    return temp.replace("temp=", "").replace("'C\n", "°C")

def estimate_pi_for_chunk(num_samples):
    inside_circle = 0
    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1:
            inside_circle += 1
    return inside_circle

def estimate_pi(num_samples, num_processes):
    pool = multiprocessing.Pool(processes=num_processes)
    chunk_size = num_samples // num_processes
    
    # Create a list with sample size for each process
    tasks = [chunk_size] * num_processes
    
    # Execute parallel computation
    results = pool.map(estimate_pi_for_chunk, tasks)
    
    pool.close()
    pool.join()
    
    # Aggregate results
    total_inside_circle = sum(results)
    
    return (total_inside_circle / num_samples) * 4

def main():
    num_samples = 100000000  # Number of samples for the pi calculation
    num_processes = multiprocessing.cpu_count()  # Use all available cores
    temperature = get_raspberry_pi_temperature()
    print(f"The temperature of the Raspberry Pi is: {temperature}")
    start_time = time.time()
    pi_estimate = estimate_pi(num_samples, num_processes)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Estimated pi: {pi_estimate}")
    print(f"Execution time: {execution_time} seconds")

    # Save the data to a file for later analysis, including temperature
    with open("execution_times.txt", "a") as file:
        file.write(f"Num Samples: {num_samples}, Execution Time: {execution_time}, Temperature: {temperature}\n")
    
    # Get the temperature again after execution
    temperature = get_raspberry_pi_temperature()
    print(f"The temperature of the Raspberry Pi is: {temperature}")

if __name__ == "__main__":
    main()
