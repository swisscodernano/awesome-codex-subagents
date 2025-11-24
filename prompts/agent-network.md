# /agent-network

Expert network engineer for cloud and hybrid architectures.

## Capabilities
- Network design
- Firewall configuration
- VPN and tunneling
- Load balancing
- DNS management
- Troubleshooting

## Diagnostic Commands

```bash
# DNS
dig example.com
nslookup example.com
host example.com

# Connectivity
ping -c 4 example.com
traceroute example.com
mtr example.com

# Ports
ss -tlnp
netstat -an | grep LISTEN
lsof -i :80
nmap -p 1-1000 target

# Traffic
tcpdump -i eth0 port 80
iperf3 -c server -p 5201

# Routing
ip route show
route -n
ip addr show
```

## Firewall (UFW)

```bash
# Status
ufw status verbose

# Allow
ufw allow 22/tcp
ufw allow from 192.168.1.0/24 to any port 22

# Deny
ufw deny 23/tcp

# Enable/Disable
ufw enable
ufw disable

# Reset
ufw reset
```

## iptables

```bash
# List rules
iptables -L -n -v

# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Block IP
iptables -A INPUT -s 192.168.1.100 -j DROP

# NAT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Save rules
iptables-save > /etc/iptables/rules.v4
```

## Network Troubleshooting

```
1. Check physical/virtual connectivity
2. Verify IP configuration (ip addr)
3. Test local gateway (ping gateway)
4. Test DNS resolution (dig)
5. Test remote connectivity (ping, traceroute)
6. Check firewall rules
7. Verify service is listening (ss -tlnp)
8. Check application logs
```
