import subprocess
import re

def update_local_repository_and_return_number_of_upgradable_packages(package_manager):
    try:
        # Use subprocess to run the package manager command to get the installed version
        process = subprocess.Popen([package_manager, 'update'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()

        # Check for errors
        if process.returncode != 0:
            print(f"Error: {error}")
            return None

        # Extract the version information from the output
        for line in output.split('\n'):
            if "packages can be upgraded" in line:
                no_of_packages_to_update=line.split(' ')[0]
                print(no_of_packages_to_update + " -> Number of packages to update:")

                return no_of_packages_to_update
            # if line.startswith('Version:'):
            #     return line.split(':')[-1].strip()

    except Exception as e:
        print(f"An error occurred: {e}")
    return None

# update_local_repository_and_return_number_of_upgradable_packages('apt')

def get_current_and_latest_version(package_manager):
    try:
        # Use subprocess to run the package manager command to get the latest version
        process = subprocess.Popen([package_manager, 'list','--installed'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()

        # Check for errors
        if process.returncode != 0:
            print(f"Error: {error}")
            return None

        # Extract the version information from the output
        for line in output.split('\n'):
            if "upgradable" in line:
                split_space=line.split(' ')
                package_name=split_space[0].split('/')[0]
                package_current_version=split_space[1]
                package_new_version=split_space[5].split(']')[0]

                
                print('package_name='+ package_name+ ',package_current_version='+package_current_version+ ',package_new_version='+package_new_version) #-> "nmap/now 7.92+dfsg2-1kali1 amd64 [installed,upgradable to: 7.94+git20230807.3be01efb1+dfsg-2+kali1]"

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
updateResults = get_current_and_latest_version('apt')


