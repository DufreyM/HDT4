import simpy
import random
import statistics
import matplotlib.pyplot as plt

RANDOM_SEED = 42
NUM_PROCESSES = [25, 50, 100, 150, 200]
INTERVALS = [10, 5, 1]
CPU_SPEED = 3  # instrucciones por unidad de tiempo
MEMORY_SIZE = 100
CPU_COUNT = 1

class Process:
    def __init__(self, env, name, cpu, ram, memory, instructions):
        self.env = env
        self.name = name
        self.cpu = cpu
        self.ram = ram
        self.memory = memory
        self.instructions = instructions
        self.cpu_time = 0
        self.wait_time = 0
        self.io_wait = False

    def run(self):
        global CPU_SPEED
        with self.ram.get(self.memory) as req:
            yield req

            while self.instructions > 0:
                with self.cpu.request() as req:
                    yield req

                    for _ in range(CPU_SPEED):
                        if self.instructions > 0:
                            self.instructions -= 1
                            self.cpu_time += 1
                            if self.instructions == 0:
                                break
                        else:
                            break

                if self.instructions > 0:
                    if random.randint(1, 21) == 1:
                        self.io_wait = True
                        yield self.env.timeout(1)
                        self.io_wait = False
                        self.wait_time += 1

def generate_processes(env, cpu, ram, num_processes, interval):
    processes = []
    for i in range(num_processes):
        instructions = random.randint(1, 10)
        memory = random.randint(1, 10)
        p = Process(env, f'Process_{i}', cpu, ram, memory, instructions)
        processes.append(p)
        env.process(p.run())
        yield env.timeout(random.expovariate(1.0 / interval))
    return processes

def simulate(num_processes_list, intervals_list):
    results = {}
    for num_processes in num_processes_list:
        for interval in intervals_list:
            env = simpy.Environment()
            cpu = simpy.Resource(env, capacity=CPU_COUNT)
            ram = simpy.Container(env, init=MEMORY_SIZE, capacity=MEMORY_SIZE)
            processes = list(generate_processes(env, cpu, ram, num_processes, interval))
            env.run()

            times = []
            for p in processes:
                times.append(p.cpu_time + p.wait_time)
            
            avg_time = statistics.mean(times)
            std_dev = statistics.stdev(times)
            results[(num_processes, interval)] = (avg_time, std_dev)
    return results

def plot_results(results):
    for interval in INTERVALS:
        avg_times = [results[(num_processes, interval)][0] for num_processes in NUM_PROCESSES]
        plt.plot(NUM_PROCESSES, avg_times, label=f'Interval={interval}')
    plt.xlabel('Number of Processes')
    plt.ylabel('Average Time')
    plt.title('Average Time vs Number of Processes')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    random.seed(RANDOM_SEED)
    simulation_results = simulate(NUM_PROCESSES, INTERVALS)
    plot_results(simulation_results)
