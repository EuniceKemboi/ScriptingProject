import sched
import time
import threading

# Create a scheduler object
scheduler = sched.scheduler(time.time, time.sleep)

# Define the task to be executed
def print_hello():
    print("Hello, world!")

# Schedule the task to run at fixed intervals
def schedule_task(interval, task):
    scheduler.enter(interval, 1, schedule_task, (interval, task))
    task()  # Execute the task

# Function to start the scheduler in a separate thread
def start_scheduler():
    threading.Thread(target=scheduler.run).start()

# Main function to start the scheduler
def main():
    interval = float(input("Enter interval for the task (in seconds): "))
    schedule_task(interval, print_hello)
    start_scheduler()  # Start the scheduler in a separate thread

# Run the main function
if __name__ == "__main__":
    main()

def get_processes_info():
    processes_info = []
    unique_processes={}
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            process_info = process.info
            
            if process_info['name'] not in unique_processes:
                #write_to_txt(process_info['name'],'whitelist.txt')
                unique_processes[process_info['name']]=1
            else:
                unique_processes[process_info['name']]+=1
            email_service.send_email('edwynkemboy@gmail.com','TEST',process_info['name'])
            processes_info.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    #print(unique_processes)
    return processes_info

def main():
    
    processes_info = get_processes_info()
    print(len(processes_info))
    print("{:<10} {:<20} {:<10} {:<10}".format('PID', 'NAME', 'CPU %', 'MEM %'))
    for process in processes_info:
        print("{:<10} {:<20} {:<10.2f} {:<10.2f}".format(
            process['pid'], process['name'], process['cpu_percent'], process['memory_percent']))
        