import psutil

import sched
import time
import threading
import email_service
import socket
import sysmonitor



scheduler = sched.scheduler(time.time, time.sleep)

def schedule_task(interval, task):
    scheduler.enter(interval, 1, schedule_task, (interval, task))
    task() # Execute the task
    threading.Thread(target=scheduler.run).start()


def get_processes_info():
    sysmonitor.main()
    all_processes_info = []
    unwhitelisted_processes=[]
    whitelisted_processes=read_file('whitelist.txt').split('\n')
    
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            all_processes_info.append(process.info)
            process_info = process.info
            if process_info['name'].split('/')[0] not in whitelisted_processes:
                unwhitelisted_processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    email_service.send_email('Alert! UnWhitelisted process', build_email_body(unwhitelisted_processes))
    print('Total running processes :'+str(len(all_processes_info)))
        
def start_monitoring_service():
    print('*******************************************************')
    print('**************PROCESS MONITORING TOOL******************')
    print('*******************************************************')
    print(' ')
    print('Enter 1 to start monitoring')
    print('Enter 2 to add/remove process from whitelist')
    user_input = input_value()
    while user_input not in ['1','2']:
        print("Invalid input")
        input_value()
        
    if(user_input == '2'):
        output='use command "add <process_name>" to whitelist \nuse command "rm <process_name>" to unwhitelist\nuse command "ls -all" to show all whitelisted processes'
        print(output)
        command=input('Enter command:')
        command_arr=command.split(' ')

        # input validation
        while len(command_arr)<2 or len(command_arr)>2 or command_arr[0] not in ['add','rm','ls']:
            print('Invalid command')
            command=input('Enter command:')
            command_arr=command.split(' ')

        #variable Stores process name
        process_name=command_arr[1]
        whitelisted_processes_arr=read_file('whitelist.txt').split('\n')


        if command_arr[0] == 'add':
            if process_name not in whitelisted_processes_arr:
                write_to_txt(process_name,'whitelist.txt')
                print('Process '+process_name+ ' whitelisted')
            else:
                print('Process '+process_name+ ' already whitelisted')
        elif command_arr[0] == 'ls':
            for process in whitelisted_processes_arr:
                print(process)
        else:
            if process_name not in whitelisted_processes_arr:
                print('Process '+process_name+ ' not whitelisted')
            else:
                whitelisted_processes_arr.remove(process_name)
                delete_file_content('whitelist.txt')
                write_lines_to_txt(whitelisted_processes_arr,'whitelist.txt')

                print('Process '+process_name+ ' unwhitelisted')
            
            
    if(user_input=='1'):
        #a function that uses pythons scheduler library to run a task /function at an interval
        schedule_task(30, get_processes_info)


def input_value():
    return input("Input: ")

        
def write_to_txt(data,file):
    with open(file, 'a') as file:
        file.write("\n" +data)

def write_lines_to_txt(lines,file):
    for line in lines:
        write_to_txt(line,file)


def delete_file_content(file_path):
    with open(file_path, 'w') as file:
        file.write('')


def read_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

def get_server_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def build_email_body(unwhitelisted_processes:list):
    trows=''
 
    for unwhitelisted_process in unwhitelisted_processes:
        trow=f"""<tr>
                    <td>{str(unwhitelisted_process['pid'])}</td>
                    <td>{str(unwhitelisted_process['name'])}</td>
                    <td>{str(round(unwhitelisted_process['cpu_percent'],2))}</td>
                    <td>{str(round(unwhitelisted_process['memory_percent'],2))}</td>
                </tr>"""
        trows=trows+trow
 
    html_div_table=f"""<div class="container">
    <h1>UnWhitelisted processes running on server {get_server_ip()}</h1>
    <table>
        <thead>
            <tr>
                <th>PID</th>
 
                <th>Process Name</th>
                <th>CPU usage(%)</th>
                <th>MEM usage(%)</th>
            </tr>
        </thead>
        <tbody>
            {trows}
        </tbody>
    </table>
    </div>"""
 
    return email_service.get_base_html(html_div_table)
 
if __name__ == "__main__":
    start_monitoring_service()

    
