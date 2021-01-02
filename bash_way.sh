#!/bin/bash

# bash_way.sh : Create RDNS entries with BASH
#
# usage: ./bash_way.sh <filename>
# 
# where filename is the name of a file you have copy+pasted the 
# entries from the ticket.

RDNS_FILE="${1:?Require filename with the raw rDNS entries to parse}"

# If this file doesnt exist then complain about it.
if [ ! -f "$RDNS_FILE" ]; then
	echo "Input raw file: $RDNS_FILE does not exist."
	exit 1
fi

ENTRIES=( "$( cat thing.txt | awk '{ print $1, $2 }' | cut -d . -f 4- | tr '\t' ' ' | sed 's/\ /\tIN\tPTR\t/' | sed 's/$/\./' )" )

for ENTRY in "${ENTRIES[@]}"; do 
	echo "$ENTRY"
done
