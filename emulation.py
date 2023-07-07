import pandas as pd
import subprocess
import time
import threading
import argparse

def set_up_network():
    # Set up the IFB for the ingress traffic control.
    cmd1 = 'sudo modprobe ifb numifbs=1'
    cmd2 = 'sudo ip link set dev ifb0 up'
    cmd3 = 'sudo tc qdisc add dev eth0 handle ffff: ingress'
    cmd4 = 'sudo tc filter add dev eth0 parent ffff: u32 match u32 0 0 action mirred egress redirect dev ifb0'

    subprocess.run(cmd1, shell=True, check=True)
    subprocess.run(cmd2, shell=True, check=True)
    subprocess.run(cmd3, shell=True, check=True)
    subprocess.run(cmd4, shell=True, check=True)

def change_network_conditions(file, direction):
    df = pd.read_csv(file)  # Read the CSV file.

    for index, row in df.iterrows():
        # Extract the bandwidth and latency values.
        bandwidth = row['bandwidth']
        latency = row['delay']

        # Print the current bandwidth and latency values.
        print(f"Changing {direction} bandwidth to: {bandwidth}Mbps and latency to: {latency}ms")

        # Create the command string.
        if direction == "downlink":
            cmd = f'sudo tc qdisc replace dev eth0 root netem rate {bandwidth}mbit delay {latency}ms'
        elif direction == "uplink":
            cmd = f'sudo tc qdisc replace dev ifb0 root netem rate {bandwidth}mbit delay {latency}ms'

        # Execute the command.
        subprocess.run(cmd, shell=True, check=True)

        # Wait 100ms before next iteration.
        time.sleep(0.1)

def main():
    parser = argparse.ArgumentParser(description='Change network conditions.')
    parser.add_argument('--file', type=str, help='The CSV file to read network conditions from.')
    parser.add_argument('--direction', type=str, choices=['uplink', 'downlink'], help='The direction of the network conditions to change.')
    args = parser.parse_args()

    if args.direction == "uplink":
        set_up_network()

    thread = threading.Thread(target=change_network_conditions, args=(args.file, args.direction))
    thread.start()

if __name__ == "__main__":
    main()