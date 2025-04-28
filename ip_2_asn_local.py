import csv
import argparse
import ipaddress
from bisect import bisect_left

class ASNLookup:
    def __init__(self, db_path):
        self.ranges = []
        self.data = []
        with open(db_path, 'r') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if len(row) < 3:  # Skip malformed lines
                    continue
                
                # Parse IP range (convert to integers for comparison)
                try:
                    start_ip = int(ipaddress.ip_address(row[0]))
                    end_ip = int(ipaddress.ip_address(row[1]))
                except ValueError:
                    continue  # Skip invalid IPs in the DB
                
                # Parse ASN (handle "0" as "N/A")
                asn = row[2] if row[2] != "0" else "N/A"
                
                # Parse country (default "N/A" if missing)
                country = row[3] if len(row) > 3 and row[3] != "None" else "N/A"
                
                # Parse org (merge remaining columns)
                org = " ".join(row[4:]).strip() if len(row) > 4 else "Not routed"
                
                self.ranges.append(start_ip)
                self.data.append((start_ip, end_ip, asn, country, org))

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

def main():
    parser = argparse.ArgumentParser(description="Bulk IP to ASN lookup")
    parser.add_argument("input_file", help="Text file with one IP per line")
    parser.add_argument("output_file", help="Output CSV file")
    args = parser.parse_args()

    asn_db = ASNLookup("ip2asn-v4.csv")  # Updated to CSV

    with open(args.input_file, 'r') as f_in, open(args.output_file, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["IP", "ASN", "Country", "Organization"])
        
        for line in f_in:
            ip = line.strip()
            if not ip:
                continue
                
            asn, country, org = asn_db.lookup(ip)
            writer.writerow([ip, asn, country, org])

if __name__ == "__main__":
    main()