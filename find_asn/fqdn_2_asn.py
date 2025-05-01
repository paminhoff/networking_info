#!/usr/bin/env python3
import csv
import argparse
import socket
import ipaddress
from bisect import bisect_left

class ASNLookup:
    def __init__(self, db_path):
        self.ranges = []
        self.data = []
        with open(db_path, 'r') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if len(row) < 3:
                    continue
                try:
                    start_ip = int(ipaddress.ip_address(row[0]))
                    end_ip = int(ipaddress.ip_address(row[1]))
                    asn = row[2] if row[2] != "0" else "N/A"
                    country = row[3] if len(row) > 3 and row[3] else "N/A"
                    org = " ".join(row[4:]).strip() if len(row) > 4 else "Not routed"
                    self.ranges.append(start_ip)
                    self.data.append((start_ip, end_ip, asn, country, org))
                except ValueError:
                    continue

    def lookup(self, ip):
        try:
            ip_int = int(ipaddress.ip_address(ip))
            idx = bisect_left(self.ranges, ip_int) - 1
            if idx >= 0:
                start, end, asn, country, org = self.data[idx]
                if start <= ip_int <= end:
                    return asn, country, org
        except ValueError:
            pass
        return "N/A", "N/A", "Not found"

def resolve_fqdn(fqdn):
    try:
        return socket.gethostbyname(fqdn)
    except (socket.gaierror, socket.timeout):
        return None

def main():
    parser = argparse.ArgumentParser(description="FQDN to ASN lookup")
    parser.add_argument("-i", "--input", required=True, help="Input file with FQDNs")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file")
    parser.add_argument("-d", "--database", default="ip2asn-v4.csv", help="ASN database")
    args = parser.parse_args()

    asn_db = ASNLookup(args.database)

    with open(args.input, 'r') as f_in, open(args.output, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["FQDN", "Resolved IP", "Country", "Org"])
        
        for line in f_in:
            fqdn = line.strip()
            if not fqdn:
                continue
            
            ip = resolve_fqdn(fqdn)
            if not ip:
                writer.writerow([fqdn, "Unresolved", "N/A", "N/A"])
                continue
                
            asn, country, org = asn_db.lookup(ip)
            writer.writerow([fqdn, ip, country, org])

if __name__ == "__main__":
    main()