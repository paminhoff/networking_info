# networking_info

## IP to ASN Lookup (find_asn/)

A Python script that converts IP addresses to ASN (Autonomous System Number) information using a local IPtoASN database.

### Features

- Fast offline lookups using a local TSV/CSV database
- Handles both IPv4 and IPv6 addresses
- Outputs ASN, country code, and organization name
- Processes bulk IPs from a file
- Optimized with binary search for performance

### Requirements

- Python 3.6+
- `ipaddress` module (standard library)

### Usage

1. First download the IPtoASN database:
   ```bash
   wget https://iptoasn.com/data/ip2asn-v4.tsv.gz
   gunzip ip2asn-v4.tsv.gz
   tr '\t' ',' < ip2asn-v4.tsv > ip2asn-v4.csv
   ```
2. Run the script:
   ```bash
   python3 ip_2_asn_local.py input_ips.txt output.csv
   ```

### Input/Output formats
**Inputs:** Text file with one IP address per line
**Output:** CSV with columns `IP, ASN, Country, Organization`

### Example

**Input**
```bash
echo -e "1.1.1.1\n8.8.8.8" > ips.txt
python3 ip_2_asn_local.py ips.txt ips2asnresults.csv
```
**output (ips2asnresults.csv)**
```bash
IP,ASN,Country,Organization
1.1.1.1,13335,US,CLOUDFLARENET
8.8.8.8,15169,US,GOOGLE
```
### Notes
- The database file should be converted from ip2asn-v4.tsv or ip2asn-v4.csv `tr '\t' ',' < ip2asn-v4.tsv > ip2asn-v4.csv`
- Invalid IPs are automatically skipped
- For large datasets, processing may take a few minutes

## FQDN to ASN Lookup Tool (find_asn/)
Resolves domain names to IP addresses and identifies network ownership using ASN data.

### Usage
```bash
python fqdn_to_asn.py -i domains.txt -o results.csv
```
### Arguments
|Flag|	Description|	Default|
|------ |----------- |----------- |
|`-i`|	Input file (one FQDN per line)|	Required|
|`-o`|	Output CSV file path|	Required|
|`-d`|	ASN database path	ip2asn-v4.csv|Required|

<sub><sup>See ip_2_asn.py documentation for information on downloading the ASN DB</sup></sub> 

### Sample output
```csv
FQDN,Resolved IP,Country,Org
example.com,93.184.216.34,US,"CDN Example Corp"
bad.domain,Unresolved,N/A,N/A
```

## IP to /24 Networks Converter (subnet_list/)

**`subnet_list/ip_to_networks.py`**  
Converts a list of IP addresses to their containing `/24` networks.  

Usage:  
```bash
python ip_to_networks.py -s input_ips.txt -o output_networks.txt
```
## Find hosts (recon/)
- The script uses multiple NMAP discovery techniques (-PE, -PS, -PA, -PP) to avoid false negatives due to ICMP blocking.
- Provide --nmap-path, NMAP path, 
- Need to provide a source list in CIDR notation
- The output CSV will have three columns: CIDR, Status (either "live" or "dead"), and hosts found in array format.

```bash
sudo python3 find_hosts.py -i cidr.txt -o results.csv -n '/opt/rapid7/nexpose/nse/nmap/nmap'
```
