"""

This code reads the contents of a text file named "country_90.txt" and searches for subnet masks
in CIDR notation within the file using regular expressions. It then converts the subnet masks to binary representation
and checks whether any subnet masks are fully contained within another subnet mask. If a subnet mask is fully contained,
it is added to a list of deleted masks, and if not, it is added to a list of remaining masks.

The code then writes the remaining subnet masks to a file named "remaining_ips.txt" 
and the deleted subnet masks to a file named "deleted_ips.txt". Finally, it prints a message indicating whether 
any subnet masks were deleted and lists the remaining subnet masks if any.

The purpose of this code is to identify and remove any redundant subnet masks in a network configuration file
to optimize network performance and avoid conflicts.

"""


import re

# Define a function to convert a CIDR notation subnet mask to a netmask
def cidr_to_netmask(cidr):

     # Calculate the bitmask by performing a bitwise XOR of a 32-bit number
    # with a left shift of 1 by the difference between 32 and the CIDR value,
    # subtracted by 1
    bits = 0xffffffff ^ (1 << 32 - int(cidr)) - 1

    # Split the bitmask into four 8-bit sections and convert each to a string
    netmask = [str(bits >> (i * 8) & 0xff) for i in range(4)]

    # Join the sections with periods to create the netmask
    return '.'.join(netmask[::-1])

# Open a file named 'country_90.txt' in read mode and read its contents into a variable
with open('country_90.txt', 'r') as file:
    contents = file.read()

# Use a regular expression to find all instances of a subnet mask in CIDR notation in the file contents
subnet_masks = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b', contents)

# Create a list of tuples containing the binary representation of the subnet mask and its CIDR notation equivalent
binary_masks = []
for mask in subnet_masks:

    # Split the subnet mask into its IP address and CIDR notation parts
    ip, cidr = mask.split('/')

    # Convert each octet of the IP address to its binary representation and concatenate them
    binary_mask = ''
    for octet in ip.split('.'):
        binary_octet = bin(int(octet))[2:].zfill(8)
        binary_mask += binary_octet

    # Append a tuple containing the binary representation and the original subnet mask to the list
    binary_masks.append((binary_mask[:int(cidr)], mask))

# Create two lists: one for subnet masks that are fully contained within another, and one for those that are not
remaining_masks = []
deleted_masks = []
for i in range(len(binary_masks)):

    # Assume that the current subnet mask will be kept
    keep_mask = True
    for j in range(len(binary_masks)):
        if i != j:

            # Find the smaller and larger binary representations of the two subnet masks
            smaller_mask, larger_mask = sorted([binary_masks[i][0], binary_masks[j][0]])

            # If the larger binary mask starts with the smaller binary mask, the smaller one is fully contained
            if larger_mask.startswith(smaller_mask):

                # Append the original subnet mask to the list of deleted masks
                deleted_masks.append(binary_masks[i][1])

                # Indicate that the current subnet mask should not be kept
                keep_mask = False
                # Exit the loop over j since the current subnet mask has already been determined to be contained
                break

    # If the current subnet mask has not been marked for deletion, append it to the list of remaining masks
    if keep_mask:
        remaining_masks.append(binary_masks[i][1])

# Loop through the subnet masks in the remaining_masks list
with open('remaining_ips.txt', 'w') as file:
    for mask in remaining_masks:

        # Split the IP address and CIDR notation
        ip, cidr = mask.split('/')

        # Convert the CIDR notation to netmask format
        network, netmask = ip, cidr_to_netmask(cidr)

        # Split the network address into decimal octets
        network_decimal = [str(int(x)) for x in network.split('.')]
        # Write the network address and CIDR notation to a file
        file.write('.'.join(network_decimal) + '/' + cidr + '\n')


# Loop through the subnet masks in the deleted_masks list
with open('deleted_ips.txt', 'w') as file:
    for mask in deleted_masks:

        # Split the IP address and CIDR notation
        ip, cidr = mask.split('/')

        # Convert the CIDR notation to netmask format
        network, netmask = ip, cidr_to_netmask(cidr)

        # Calculate the network address using a bitwise AND operation
        for i in range(4):
            network_octet = int(network.split('.')[i])
            netmask_octet = int(netmask.split('.')[i])
            if i < 3:
                file.write(str(network_octet & netmask_octet) + '.')
            else:
                file.write(str(network_octet & netmask_octet))

        # Write the network address and CIDR notation to a file
        file.write('/' + cidr + '\n')

# Print a message indicating whether any subnet masks were deleted
if deleted_masks:
    print('Deleted subnet masks:')
    for mask in deleted_masks:
        print(mask)
else:
    print('No subnet masks were deleted.')

# Print a message indicating the remaining subnet masks
if remaining_masks:
    print('Remaining subnet masks:')
    for mask in remaining_masks:
        print(mask)
else:
    print('No remaining subnet masks.')
