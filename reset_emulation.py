import subprocess
import re

def get_all_interfaces():
    # Get the output of the "ip link show" command.
    result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)
    output = result.stdout

    # Use a regular expression to find all the interface names.
    return re.findall(r'\d+: (\w+):', output)

def reset_network(interface):
    # Remove the existing ingress qdisc.
    cmd1 = f'sudo tc qdisc del dev {interface} ingress'
    # Remove the existing egress qdisc.
    cmd2 = f'sudo tc qdisc del root dev {interface}'
    
    subprocess.run(cmd1, shell=True, stderr=subprocess.DEVNULL)
    subprocess.run(cmd2, shell=True, stderr=subprocess.DEVNULL)
    
    print(f"Network interface {interface} has been reset to its default settings.")

def main():
    # Get all network interfaces.
    interfaces = get_all_interfaces()

    # Ask user to input a network interface
    user_interface = input("Please enter a network interface name: ")
    
    # Check if the user input interface is in the list of interfaces
    if user_interface in interfaces:
        reset_network(user_interface)
    else:
        print(f"Network interface {user_interface} does not exist. Please check the name.")

if __name__ == "__main__":
    main()