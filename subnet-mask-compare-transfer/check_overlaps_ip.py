"""
In this specific code, the check_overlap function takes a list of IP addresses or subnets as input, 
converts each item in the list to an IP address or network object using the ipaddress module,
and checks for overlaps between the objects. If any overlaps are found,
the function returns a list of tuples containing the overlapping objects. 
If no overlaps are found, the function returns a message saying so.

The code then reads in a list of IPs from a file using Python's built-in open function, 
calls the check_overlap function to check for overlaps in the list, and prints the results to the console.
"""


import ipaddress

# Define a function that takes a list of IP addresses or subnets and checks for overlaps
def check_overlap(ip_list):
    ip_objects = [] # create an empty list to hold the IP objects
    for ip in ip_list:
        try:
            ip_objects.append(ipaddress.ip_address(ip)) # try to create an IP address object from the string
        except ValueError:
            try:
                ip_objects.append(ipaddress.ip_network(ip, strict=False)) # if that fails, try to create a network object from the string
            except ValueError:
                return f"{ip} is not a valid IP address or subnet" # if both attempts fail, return an error message
    overlaps = [] # create an empty list to hold any overlapping subnets
    for i in range(len(ip_objects)):
        for j in range(i+1, len(ip_objects)):
            if ip_objects[i].overlaps(ip_objects[j]): # check if subnet i overlaps with subnet j
                overlaps.append((ip_objects[i], ip_objects[j])) # if so, add the overlapping subnets to the list
    if overlaps:
        return overlaps # if there are overlapping subnets, return the list
    else:
        return "No overlaps found" # if there are no overlapping subnets, return a message saying so
    

with open('remaining_ips.txt', 'r') as f: # open a file containing a list of IP addresses or subnets
    remaining_ips = [line.strip() for line in f] # read the file and create a list of strings, stripping any whitespace

overlaps = check_overlap(remaining_ips) # call the function to check for overlaps in the list of IPs

if overlaps != "No overlaps found": # if there are overlaps, print a message and list the overlapping subnets
    print('There are overlapping subnets or inclusive subnets in the remaining IPs:')
    for subnet1, subnet2 in overlaps:
        print(f'{subnet1} and {subnet2}')
else: # if there are no overlaps, print a message saying so
    print('There are no overlapping subnets or inclusive subnets in the remaining IPs.')
