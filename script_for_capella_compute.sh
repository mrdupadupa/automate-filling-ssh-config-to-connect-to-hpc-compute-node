#!/usr/bin/env bash

NODE=$(ssh -T capella "squeue --me --states=R --noheader --format=%N" 2>/dev/null | grep -E '^c[0-9]+' | head -n 1)


if [[ -z "$NODE" ]]; then
	echo "No running node on the capella compute found"
	exit 1
fi

echo "Found running node: $NODE"

# 3. Find the directory where THIS bash script lives
# This ensures it can find the Python script even if you run this from a different folder
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 4. Run the Python script and pass the $NODE variable as an argument
python3 "$DIR/update_ssh_config.py" "$NODE"
