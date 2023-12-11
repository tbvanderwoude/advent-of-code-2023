#!/bin/bash

# Check if the correct number of arguments is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <n>"
    exit 1
fi

# Extract the numerical argument
n=$1

# Check if the argument is a valid number
if ! [[ $n =~ ^[0-9]+$ ]]; then
    echo "Error: Please provide a valid numerical argument."
    exit 1
fi

# Check if the source file day_X.py exists
source_file="day_X.py"
if [ ! -e "$source_file" ]; then
    echo "Error: Source file '$source_file' not found."
    exit 1
fi

# Destination file name
destination_file="day_$n.py"

# Copy and rename the file
cp "$source_file" "$destination_file"
echo "File copied and renamed to $destination_file."

# Create an empty inputs file
inputs_dir="inputs"
input_file="$inputs_dir/day-$n.txt"

# Check if the inputs directory exists, if not, create it
if [ ! -d "$inputs_dir" ]; then
    mkdir "$inputs_dir"
    echo "Created directory $inputs_dir."
fi

# Create an empty file
touch "$input_file"
echo "Empty input file created at $input_file."