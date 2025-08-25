import nmap

Target = "<target IP or hostname>"

def hostDiscovery(target: str):
    nm = nmap.PortScanner()
    nm.scan(hosts=target, arguments='-sn')  # ping/host discovery
    return nm.all_hosts()

def portScan(target: str, ports="1-1024"):
    nm = nmap.PortScanner()
    # On Windows, -sT (TCP connect) works without admin; -sS (SYN) needs admin
    nm.scan(hosts=target, arguments=f'-sT -p {ports}')
    results = {}
    for host in nm.all_hosts():
        results[host] = {}
        for proto in nm[host].all_protocols():
            for port in sorted(nm[host][proto].keys()):
                state = nm[host][proto][port]['state']
                name = nm[host][proto][port].get('name', '')
                results[host][port] = {'state': state, 'service': name}
    return results

def vulnScan(target: str):
    nm = nmap.PortScanner()
    # Requires Nmap scripts installed; often needs admin rights and takes time
    nm.scan(hosts=target, arguments='-sV --script vuln')
    return nm.csv()  # simple printable summary

if __name__ == "__main__":
    try:
        print("Host discovery:")
        print(hostDiscovery(Target))

        print("\nPort scan:")
        ports = portScan(Target, "1-1024")
        for host, ps in ports.items():
            print(f"{host}:")
            for p, info in ps.items():
                print(f"  {p}/tcp  {info['state']}  {info['service']}")

        print("\nVulnerability scan (summary):")
        print(vulnScan(Target))
    except nmap.PortScannerError as e:
        print("Nmap error:", e)
    except Exception as e:
        print("Unexpected error:", e)