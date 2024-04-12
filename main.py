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
    task() 
    threading.Thread(target=scheduler.run).start()


def get_processes_info():
    processes_info = []
    whitelisted_processes=read_file('whitelist.txt').split('\n')

    trows=''
    

    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            process_info = process.info
            if process_info['name'].split('/')[0] not in whitelisted_processes:
                   
                trow=f"""<tr>
                    <td>{process_info['pid']}</td>
                    <td>{process_info['name']}</td>
                    <td>{process_info['cpu_percent']}</td>
                    <td>{process_info['memory_percent']}</td>
                </tr>"""
                print(trow)
                trows=trows+trow
                
            processes_info.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

        print(trows)
        content=f"""<div class="container">
        <h1>UnWhitelisted processes running on server {get_server_ip()}</h1>
        <table>
            <thead>
                <tr>
                    <th>PID</th>
                    <th>Process Name</th>
                    <th>CPU usage</th>
                    <th>MEM usage</th>
                </tr>
            </thead>
            <tbody>
                """+trows+"""
                <tr>
                    <td>Jane Smith</td>
                    <td>jane@example.com</td>
                </tr>`
            </tbody>
        </table>
        </div>"""

        email_service.send_email('TEST',email_service.get_html_message(content))

    return processes_info

def main():
    sysmonitor.main()
    processes_info = get_processes_info()
    print('Total running processes :'+str(len(processes_info)))
        
def start_monitoring_service():
    print('*******************************************************')
    print('**************PROCESS MONITORING TOOL******************')
    print('*******************************************************')
    print(' ')
    print('Enter 1 to start monitoring')
    print('Enter 2 to start monitoring in background')
    print('Enter 3 to add/remove process from whitelist')
    user_input = input_value()
    while user_input not in ['1','2','3']:
        print("Invalid input")
        input_value()
        
    if(user_input=='3'):
        output='use command "add <process_name>" to whitelist \nuse command "rm <process_name>" to unwhitelist\nuse command "ls -all" to show all whitelisted processes'
        print(output)
        command=input('Enter command:')
        command_arr=command.split(' ')

        while len(command_arr)<2 or len(command_arr)>2 or command_arr[0] not in ['add','rm','ls']:
            print('Invalid command')
            command=input('Enter command:')
            command_arr=command.split(' ')

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
        schedule_task(5, main)

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

if __name__ == "__main__":
    #main()
    start_monitoring_service()



    

    

# Schedule the task to run after 5 seconds

    
