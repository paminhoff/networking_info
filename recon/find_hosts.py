import csv
import argparse
import subprocess
from ipaddress import ip_network

def discover_hosts(cidr, nmap_path):
    """
    Perform host discovery using NMAP and return live hosts.
    Returns:
        - bool: True if at least one host is live
        - list: List of live IP addresses
    """
    try:
        # Run NMAP with aggressive host discovery
        command = [
            nmap_path,
            '-sn',              # No port scan, just host discovery
            '-PE',              # ICMP echo
            '-PS22,80,443',     # TCP SYN to common ports
            '-PA22,80,443',     # TCP ACK to common ports
            '-PP',              # ICMP timestamp
            '--open',           # Only show hosts that are "up"
            cidr
        ]
        result = subprocess.run(command, capture_output=True, text=True)

        # Parse NMAP output for live hosts
        live_hosts = []
        for line in result.stdout.split('\n'):
            if "Nmap scan report for" in line:
                ip = line.split()[-1].strip('()')
                if ip.replace('.', '').isdigit():  # Ensure it's an IP (not a hostname)
                    live_hosts.append(ip)

        return len(live_hosts) > 0, live_hosts

    except Exception as e:
        print(f"Error scanning {cidr}: {e}")
        return False, []

def main():
    parser = argparse.ArgumentParser(description="Discover live hosts in CIDR networks using NMAP.")
    parser.add_argument('-i', '--input', required=True, help="Input file containing CIDR networks (one per line)")
    parser.add_argument('-n', '--nmap-path', required=True, help="Path to NMAP executable")
    parser.add_argument('-o', '--output', required=True, help="Output CSV file path")
    args = parser.parse_args()

    # Read CIDRs from input file
    with open(args.input, 'r') as f:
        cidrs = [line.strip() for line in f if line.strip()]

    # Validate CIDRs
    valid_cidrs = []
    for cidr in cidrs:
        try:
            network = ip_network(cidr, strict=False)
            valid_cidrs.append(str(network))
        except ValueError:
            print(f"Invalid CIDR: {cidr}")

    results = []
    for cidr in valid_cidrs:
        is_live, live_hosts = discover_hosts(cidr, args.nmap_path)
        status = "live" if is_live else "dead"
        results.append({
            "CIDR": cidr,
            "Status": status,
            "HOSTS": live_hosts if is_live else []
        })
        print(f"CIDR: {cidr} -> {status} -> Hosts: {live_hosts if is_live else 'None'}")

    # Write results to CSV
    with open(args.output, 'w', newline='') as csvfile:
        fieldnames = ['CIDR', 'Status', 'HOSTS']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow({
                'CIDR': row['CIDR'],
                'Status': row['Status'],
                'HOSTS': ','.join(row['HOSTS']) if row['HOSTS'] else ''
            })

    print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()