# Automate Filling SSH Config to Connect to HPC compute node
# Capella SSH Config Updater

A quick automation tool to seamlessly connect to dynamically allocated Slurm compute nodes on the HPC cluster.

As the example used Capella cluster of TU Dresden HPC

Since compute node hostnames change with every job allocation, these scripts fetch your currently running node and automatically inject it into your local `~/.ssh/config` file.

## Files

* **`script_for_capella_compute.sh`**: The main entry point. It connects to the `capella` login node, queries Slurm (`squeue`) to find your currently running compute node, and passes the node name to the Python script.
* **`update_ssh_config.py`**: The configuration manager. It takes the node name from the Bash script and surgically updates the active `HostName` under the `Host capella_compute` block in your `~/.ssh/config` file without altering any other settings or formatting.

## Prerequisites

1. Python 3 installed on your local machine.
2. Ensure you have a `Host capella_compute` block in your `~/.ssh/config` file with an active `HostName` directive (not commented out). Example:
   ```ssh-config
   Host capella_compute
       ProxyJump capella
       User your_username
       HostName c126  # <-- This is the line the script will update