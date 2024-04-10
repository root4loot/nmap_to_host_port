Simple script to parse .nmap and output list of hostnames and open ports.

```sh
usage: nmap_to_host_port.py [-h] [--unique-hosts] filename

Extract open port information from Nmap scan reports.

positional arguments:
  filename        The Nmap scan file to process.

options:
  -h, --help      show this help message and exit
  --unique-hosts  Output only the first hostname for each unique IP address.
```

## Example

```sh
➜  nmap scanme.sh -o results.nmap
Starting Nmap 7.94 ( https://nmap.org ) at 2024-04-10 15:21 CEST
Nmap scan report for scanme.sh (128.199.158.128)
Host is up (0.27s latency).
Other addresses for scanme.sh (not scanned): 2400:6180:0:d0::91:1001
Not shown: 993 closed tcp ports (conn-refused)
PORT      STATE SERVICE
22/tcp    open  ssh
53/tcp    open  domain
80/tcp    open  http
443/tcp   open  https
444/tcp   open  snpp
445/tcp   open  microsoft-ds
15000/tcp open  hydap

Nmap done: 1 IP address (1 host up) scanned in 64.32 seconds
```

```sh
➜  nmap ./nmap_to_host_port.py results.nmap
scanme.sh:15000
scanme.sh:22
scanme.sh:443
scanme.sh:444
scanme.sh:445
scanme.sh:53
scanme.sh:80
```
