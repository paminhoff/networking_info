#!/usr/bin/env python3
import ipaddress
import argparse
from pathlib import Path

def get_24_networks(ip_list):
    """Convert a list of IPs to their /24 network addresses."""
    networks = set()  # Using a set to avoid duplicates
    
    for ip in ip_list:
        try:
            # Parse the IP address
            ip_obj = ipaddress.ip_address(ip.strip())
            # Get the /24 network
            network = ipaddress.ip_network(f"{ip_obj}/24", strict=False)
            networks.add(network)
        except ValueError as e:
            print(f"Warning: Skipping invalid IP '{ip}': {e}")
    
    return sorted(networks, key=lambda x: x.network_address)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert IP addresses to /24 networks.')
    parser.add_argument('-s', '--source', required=True, help='Input file containing IP addresses (one per line)')
    parser.add_argument('-o', '--output', required=True, help='Output file for /24 networks')
    args = parser.parse_args()

    # Verify input file exists
    if not Path(args.source).is_file():
        print(f"Error: Input file '{args.source}' not found.")
        return

    # Read input file
    try:
        with open(args.source, 'r') as f:
            ip_list = [line.strip() for line in f if line.strip()]
    except IOError as e:
        print(f"Error reading input file: {e}")
        return

    if not ip_list:
        print("Error: No valid IP addresses found in input file.")
        return

    # Process IPs
    networks = get_24_networks(ip_list)

    # Write output
    try:
        with open(args.output, 'w') as f:
            for network in networks:
                f.write(f"{network}\n")
        print(f"Successfully wrote {len(networks)} /24 networks to '{args.output}'")
    except IOError as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    main()