/*This code reads IP address ranges from a CSV file and calculates the subnet mask for each range. 
It then writes the start IP address and subnet mask to an output file in the format "startIP/subnetMask".

Requires a CSV file containing IP address ranges in the format "startIP,endIP", 
and an output file to write the calculated subnet masks.*/
package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"net"
	"os"
	"strconv"
)


// ipToInt converts a dotted-quad IP address string to a 32-bit unsigned integer.
func ipToInt(ip string) uint32 {
	
	// Parse the IP address string into a net.IP struct.
	parsedIP := net.ParseIP(ip)
	
	// If the IP address is invalid, log a fatal error and exit the program.
	if parsedIP == nil {
		log.Fatalf("Invalid IP address: %s", ip)
	}
	
	// Convert the net.IP struct to a 4-byte slice containing the IP address in network byte order.
	ipBytes := parsedIP.To4()
	
	// If the IP address is not an IPv4 address, log a fatal error and exit the program.
	if ipBytes == nil {
		log.Fatalf("Invalid IPv4 address: %s", ip)
	}
	
	// Convert the 4-byte slice to a 32-bit unsigned integer, by shifting each byte to the left by the correct number of bits,
	// and adding them together using the bitwise OR operator.
	return (uint32(ipBytes[0]) << 24) + (uint32(ipBytes[1]) << 16) + (uint32(ipBytes[2]) << 8) + uint32(ipBytes[3])
}



// intToIP converts a 32-bit unsigned integer to a dotted-quad IP address string.
func intToIP(num uint32) string {
	
	// Extract the first octet (8 bits) from the 32-bit integer, and shift it all the way to the right.
	// Then, use a bitmask to isolate the lower 8 bits and discard the rest.
	first := (num >> 24) & 0xff
	
	// Extract the second octet (8 bits) from the 32-bit integer, shift it 16 bits to the right,
	// and use a bitmask to isolate the lower 8 bits and discard the rest.
	second := (num >> 16) & 0xff
	
	// Extract the third octet (8 bits) from the 32-bit integer, shift it 8 bits to the right,
	// and use a bitmask to isolate the lower 8 bits and discard the rest.
	third := (num >> 8) & 0xff
	
	// Extract the fourth octet (8 bits) from the 32-bit integer, and use a bitmask to isolate the lower 8 bits and discard the rest.
	fourth := num & 0xff
	
	// Return a formatted string containing the four octets separated by periods.
	return fmt.Sprintf("%d.%d.%d.%d", first, second, third, fourth)
}



/*this function takes two IP addresses (in string format) as input,
calculates the subnet mask for the range between them, and returns the mask as a uint32 value.*/
func calculateSubnetMask(startIP string, endIP string) uint32 {

	// Convert the start and end IP addresses from string format to uint32
	startNum := ipToInt(startIP)
	endNum := ipToInt(endIP)

	// Calculate the XOR difference between the start and end IP addresses
	xorNum := startNum ^ endNum

	// Convert the XOR result to a binary string
	xorBin := strconv.FormatInt(int64(xorNum), 2)

	// Determine the number of leading zeros in the binary representation of the XOR result
	prefixLen := 0
	for i := 0; i < len(xorBin); i++ {
		if xorBin[i:i+1] == "1" {
			prefixLen = i + 1
		}
	}

	// Calculate the subnet mask length in decimal format
	subnetMaskDecimal := uint32(32 - prefixLen)

	// Return the subnet mask as a uint32 value
	return subnetMaskDecimal
}

func main() {
	// Open the CSV file containing the IP address ranges
	file, err := os.Open("ips-range.csv")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// Create a new CSV reader to read the contents of the file
	reader := csv.NewReader(file)

	// Loop through each row in the CSV file
	for {
		// Read the next row of data from the CSV file
		row, err := reader.Read()

		// If an error occurs while reading the row, log the error and exit the program
		if err != nil {
			// Check if the error is due to reaching the end of the file, and break out of the loop if so
			if err.Error() == "EOF" {
				break
			}
			log.Fatal(err)
		}

		// Extract the start and end IP addresses from the current row of the CSV file
		startIP := row[0]
		endIP := row[1]

		// Calculate the subnet mask for the IP address range between the start and end addresses
		subnetMask := calculateSubnetMask(startIP, endIP)

		// Open the output file to write the calculated subnet mask
		output, err := os.OpenFile("subnet_masks.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		if err != nil {
			log.Fatal(err)
		}
		defer output.Close()

		// Write the start IP address and subnet mask to the output file in the format "startIP/subnetMask"
		output.WriteString(fmt.Sprintf("%s/%d\n", startIP, subnetMask))
	}
}

