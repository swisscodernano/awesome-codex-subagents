# /agent-osint

Expert OSINT specialist for reconnaissance.

## Subdomain Enumeration
```bash
subfinder -d target.com -silent
amass enum -d target.com
assetfinder target.com
```

## DNS Recon
```bash
dig target.com any
dig +short target.com ns
host -t mx target.com
```

## Web Recon
```bash
# Wayback Machine
waybackurls target.com | sort -u

# Google dorks
site:target.com filetype:pdf
site:target.com inurl:admin
site:target.com "password" OR "api_key"

# Technology detection
whatweb target.com
wappalyzer target.com
```

## Shodan
```bash
shodan search "target.com"
shodan host IP_ADDRESS
```

## Social
```bash
# theHarvester
theHarvester -d target.com -b google,linkedin

# Social profiles
sherlock username
```

## Best Practices
- Document everything
- Use VPN/proxy
- Respect scope
- No active scanning without permission
