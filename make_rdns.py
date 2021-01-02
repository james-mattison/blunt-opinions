#!/usr/bin/env python3
import argparse
import os
import re 

"""
make_rdns.py: A simple python script to create DNS entries from the input a customer 
              gives in an rDNS request ticket.


usage: ./make_rdns.py <filename>
<filename> should be where you have copied and pasted this input from the ticketing system.
"""


parser = argparse.ArgumentParser()
parser.add_argument("input_filename", action = "store", help = "The filepath of the customer rDNS request.")

def parse_customer_file(filename):
    bad_lines = []

    # Open the file that we get and read it line by line into an array.
    with open(filename, "r") as _o:
        lines = _o.readlines()

    for line in lines:
        # Match any four sets of numbers, like an ip, wth 3 periods in the middle
        # [0-9] <-- means 'ANY number at all'
        # {1,3} <-- means 'ANY number - one, two, or three digits'
        # \.    <-- means the period in the ip. It must be escaped with \. due to globbing.
        if not re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", line):
            continue

        # We have an ip address in the line. let's split it and see if we have a
        # value as well.

        # First, change any tab characters to spaces:
        line = line.replace("\t", " ")

        # Next, split the line at the spaces, to get <ip> <entry>
        line = line.split(" ")

        # If we it didn't split into at least two pieces, but does have an IP address in it,
        # then something is fucked up about this line. Therefore add it to the bad lines. We
        # will inform the user afterwards.
        if len(line) < 2:
            bad_lines.append(line)
            continue

        # assign these to variables to make it easy to understand
        ip = line[0]

        # get rid of the newline at the end of the entry itself.
        entry = line[1].strip("\n")

        # do we have a period in the dns entry itself? ie .com - this makes sure its valid.
        if not "." in entry:
            bad_lines.append(line)
            continue

        # Split the last octet off the IP address (I think this is how it works, right? I can't remember)
        last_octet = ip.split(".")[-1]

        # print the line that we have created - this will be copy+pasted into the zone file
        # Note that the period that is required at the end of the line is added here:
        print(f"{last_octet}\tIN\tPTR\t{entry}.")

    if bad_lines:
        print("=" * 40)
        for bad_line in bad_lines:
            print(f"BAD INPUT LINE: {bad_line}")


if __name__ == "__main__":
    args = parser.parse_args()
    # if TJ is tsoned and the file doesnt exist, warn him
    if not os.path.exists(args.input_filename):
        print("Hey dummy, quit smoking so much weed. The file needs to exist.")
        quit(1)

    parse_customer_file(args.input_filename)

