#!/bin/sh

# Execute commands from the file
cat commands.txt

# Prompt for standard input
while true; do
    read user_input
    echo $user_input
done

