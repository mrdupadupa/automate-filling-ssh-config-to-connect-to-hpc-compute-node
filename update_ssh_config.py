import os
import re
import sys

def update_ssh_config(config_path, target_host, new_hostname):
    config_path = os.path.expanduser(config_path)
    
    if not os.path.exists(config_path):
        print(f"Error: SSH Config file '{config_path}' not found.")
        sys.exit(1)

    with open(config_path, 'r') as file:
        lines = file.readlines()

    in_target_host = False
    updated_lines = []
    key_found = False

    for line in lines:
        # 1. Check if entering a new Host section
        host_match = re.match(r'^\s*Host\s+(.+)', line, re.IGNORECASE)
        if host_match:
            current_host = host_match.group(1).strip()
            in_target_host = (current_host == target_host)
        
        # 2. If in 'capella_compute', look for the active HostName
        if in_target_host:
            key_match = re.match(r'^(\s*)HostName\s+.*', line, re.IGNORECASE)
            
            # Look for HostName, ensuring it's not a commented line like your c147 backup
            if key_match and not line.strip().startswith('#'):
                indent = key_match.group(1) # Keep original indentation (tabs/spaces)
                updated_lines.append(f"{indent}HostName {new_hostname}\n")
                key_found = True
                
                # Turn flag off so we only replace the FIRST active HostName in this block
                in_target_host = False 
                continue # Skip appending the old HostName line
        
        # 3. Append all other lines unmodified
        updated_lines.append(line)

    # 4. Write back to the config safely
    with open(config_path, 'w') as file:
        file.writelines(updated_lines)
        
    if key_found:
        print(f"Success: Set HostName to '{new_hostname}' for Host '{target_host}'.")
    else:
        print(f"Notice: Could not find an active 'HostName' for Host '{target_host}'.")

if __name__ == "__main__":
    # Ensure a node name was passed from the Bash script
    if len(sys.argv) < 2:
        print("Error: No node name provided to the Python script.")
        sys.exit(1)
        
    # sys.argv[1] catches the $NODE variable passed from Bash
    target_node = sys.argv[1]
    
    # Target your specific SSH config file and host block
    update_ssh_config("~/.ssh/config", "capella_compute", target_node)
