import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None
        self.waiting_time = None
        self.turnaround_time = None

# Generating 67 processes
num_processes = 67
processes = []

for i in range(num_processes):
    arrival_time = random.randint(0, 100)
    burst_time = random.randint(1, 20)
    priority = random.randint(1, 10)
    processes.append(Process(i, arrival_time, burst_time, priority))

# Adding the transient process
transient_process = Process(pid=68, arrival_time=50, burst_time=10, priority=1)
processes.append(transient_process)

# Sorting processes by arrival time
processes.sort(key=lambda x: x.arrival_time)

def plot_gantt_chart(processes, title):
    fig, gnt = plt.subplots()
    gnt.set_ylim(0, 10)
    max_completion_time = max(p.completion_time for p in processes if p.completion_time is not None)
    gnt.set_xlim(0, max_completion_time + 10)
    gnt.set_xlabel('Time')
    gnt.set_yticks([5])
    gnt.set_yticklabels(['Processes'])
    gnt.grid(True)

    colors = plt.cm.get_cmap('tab20', len(processes))
    patches = []

    for idx, p in enumerate(processes):
        if p.start_time is not None:
            gnt.broken_barh([(p.start_time, p.burst_time)], (2, 6), facecolors=colors(idx))
            if p.pid == transient_process.pid:
                patches.append(mpatches.Patch(color=colors(idx), label=f'Transient Process {p.pid}'))
            else:
                patches.append(mpatches.Patch(color=colors(idx), label=f'Process {p.pid}'))

    # plt.legend(handles=patches, bbox_to_anchor=(1, 1), loc='upper left')
    plt.title(title)
    plt.show()

def calculate_metrics(processes):
    # Handle cases where waiting_time or turnaround_time might be None
    total_waiting_time = sum((p.waiting_time or 0) for p in processes)
    total_turnaround_time = sum((p.turnaround_time or 0) for p in processes)
    
    num_processes = len(processes)
    
    average_waiting_time = total_waiting_time / num_processes if num_processes > 0 else 0
    average_turnaround_time = total_turnaround_time / num_processes if num_processes > 0 else 0
    
    # Retrieve metrics for the transient process
    transient_process = next((p for p in processes if p.pid == 68), None)
    transient_waiting_time = transient_process.waiting_time if transient_process else None
    transient_turnaround_time = transient_process.turnaround_time if transient_process else None
    print(average_waiting_time, average_turnaround_time, transient_waiting_time, transient_turnaround_time)
    return average_waiting_time, average_turnaround_time, transient_waiting_time, transient_turnaround_time

def fcfs_scheduling(processes):
    current_time = 0
    for p in processes:
        if current_time < p.arrival_time:
            current_time = p.arrival_time
        p.start_time = current_time
        current_time += p.burst_time
        p.completion_time = current_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

def sjf_scheduling(processes):
    current_time = 0
    completed_processes = []
    while len(completed_processes) < len(processes):
        available_processes = [p for p in processes if p.arrival_time <= current_time and p not in completed_processes]
        if available_processes:
            p = min(available_processes, key=lambda x: x.burst_time)
            p.start_time = current_time
            current_time += p.burst_time
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            completed_processes.append(p)
        else:
            current_time += 1

def rr_scheduling(processes, time_quantum):
    current_time = 0
    queue = [p for p in processes if p.arrival_time <= current_time]
    while queue:
        p = queue.pop(0)
        if p.start_time is None:
            p.start_time = current_time
        if p.remaining_time > time_quantum:
            current_time += time_quantum
            p.remaining_time -= time_quantum
            queue.extend([p for p in processes if p.arrival_time <= current_time and p not in queue and p.remaining_time > 0])
            queue.append(p)
        else:
            current_time += p.remaining_time
            p.remaining_time = 0
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time

def priority_scheduling(processes):
    current_time = 0
    completed_processes = []
    while len(completed_processes) < len(processes):
        available_processes = [p for p in processes if p.arrival_time <= current_time and p not in completed_processes]
        if available_processes:
            p = min(available_processes, key=lambda x: x.priority)
            p.start_time = current_time
            current_time += p.burst_time
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            completed_processes.append(p)
        else:
            current_time += 1

def srtf_scheduling(processes):
    current_time = 0
    completed_processes = []
    while len(completed_processes) < len(processes):
        available_processes = [p for p in processes if p.arrival_time <= current_time and p not in completed_processes]
        if available_processes:
            p = min(available_processes, key=lambda x: x.remaining_time)
            if p.start_time is None:
                p.start_time = current_time
            current_time += 1
            p.remaining_time -= 1
            if p.remaining_time == 0:
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                completed_processes.append(p)
        else:
            current_time += 1

# Function to reset process attributes for the next scheduling algorithm
def reset_processes(processes):
    for p in processes:
        p.start_time = None
        p.completion_time = None
        p.waiting_time = None
        p.turnaround_time = None
        p.remaining_time = p.burst_time

# Running and visualizing each scheduling algorithm

# FCFS Scheduling
reset_processes(processes)  # Ensure processes are reset before each scheduling
fcfs_scheduling(processes)
plot_gantt_chart(processes, "FCFS Scheduling")
fcfs_metrics = calculate_metrics(processes)

# SJF Scheduling
reset_processes(processes)
sjf_scheduling(processes)
plot_gantt_chart(processes, "SJF Scheduling")
sjf_metrics = calculate_metrics(processes)

# Round Robin Scheduling
reset_processes(processes)
time_quantum = 4
rr_scheduling(processes, time_quantum)
plot_gantt_chart(processes, "Round Robin Scheduling")
rr_metrics = calculate_metrics(processes)

# Priority Scheduling
reset_processes(processes)
priority_scheduling(processes)
plot_gantt_chart(processes, "Priority Scheduling")
priority_metrics = calculate_metrics(processes)

# SRTF Scheduling
reset_processes(processes)
srtf_scheduling(processes)
plot_gantt_chart(processes, "SRTF Scheduling")
srtf_metrics = calculate_metrics(processes)

# Comparison of Metrics
print("\n--- Comparison of Scheduling Algorithms ---")
print(f"{'Algorithm':<25}{'Avg Waiting Time':<20}{'Avg Turnaround Time':<20}{'Transient Waiting Time':<25}{'Transient Turnaround Time':<25}")
print(f"{'FCFS':<25}{fcfs_metrics[0]:<20.2f}{fcfs_metrics[1]:<20.2f}{fcfs_metrics[2]:<25.2f}{fcfs_metrics[3]:<25.2f}")
print(f"{'SJF':<25}{sjf_metrics[0]:<20.2f}{sjf_metrics[1]:<20.2f}{sjf_metrics[2]:<25.2f}{sjf_metrics[3]:<25.2f}")
print(f"{'Round Robin':<25}{rr_metrics[0]:<20.2f}{rr_metrics[1]:<20.2f}{rr_metrics[2]:<25.2f}{rr_metrics[3]:<25.2f}")
print(f"{'Priority Scheduling':<25}{priority_metrics[0]:<20.2f}{priority_metrics[1]:<20.2f}{priority_metrics[2]:<25.2f}{priority_metrics[3]:<25.2f}")
print(f"{'SRTF':<25}{srtf_metrics[0]:<20.2f}{srtf_metrics[1]:<20.2f}{srtf_metrics[2]:<25.2f}{srtf_metrics[3]:<25.2f}")

# Conclusion based on metrics
print("\n--- Conclusion ---")
print("FCFS: Simple to implement but can have high waiting time, especially for short processes.")
print("SJF: Minimizes waiting time for short processes but can lead to starvation for long processes.")
print("Round Robin: Fairly distributes CPU time but can have high waiting time if the time quantum is not optimal.")
print("Priority Scheduling: Processes with higher priority are scheduled first, which can cause starvation for low-priority processes.")
print("SRTF: Efficient for minimizing waiting time but complex to implement and can cause starvation for long processes.")
