# 🎯 AI Command Examples

Complete guide with real-world examples of using AI-powered natural language commands.

## 🔍 Network Scanning

### Basic Scanning
```bash
toolbox> ai scan 192.168.1.1
Generated: nmap -sV 192.168.1.1

toolbox> ai find open ports on 192.168.1.1
Generated: nmap -p- 192.168.1.1

toolbox> ai quick scan 192.168.1.0/24
Generated: nmap -sn 192.168.1.0/24
```

### Advanced Scanning
```bash
toolbox> ai aggressive scan with OS detection on 192.168.1.1
Generated: nmap -A -T4 192.168.1.1

toolbox> ai scan for web services on 192.168.1.1
Generated: nmap -sV -p 80,443,8080,8443 192.168.1.1

toolbox> ai discover live hosts on 192.168.1.0/24
Generated: nmap -sn 192.168.1.0/24
```

## 🌐 Web Application Testing

### Directory Enumeration
```bash
toolbox> ai scan http://example.com for directories
Generated: gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt

toolbox> ai find hidden files on http://192.168.1.1
Generated: gobuster dir -u http://192.168.1.1 -w /usr/share/wordlists/dirb/common.txt -x php,txt,html

toolbox> ai brute force directories on http://example.com
Generated: dirb http://example.com /usr/share/wordlists/dirb/common.txt
```

### Vulnerability Scanning
```bash
toolbox> ai test http://example.com for SQL injection
Generated: sqlmap -u "http://example.com" --batch --dbs

toolbox> ai scan http://example.com for XSS
Generated: nikto -h http://example.com

toolbox> ai check http://example.com for vulnerabilities
Generated: nikto -h http://example.com -p 80,443
```

## 🔐 Password Attacks

### SSH Brute Force
```bash
toolbox> ai brute force SSH on 192.168.1.1
Generated: hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.1

toolbox> ai crack SSH on 192.168.1.1 with user admin
Generated: hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.1

toolbox> ai dictionary attack on 192.168.1.1
Generated: hydra -L /usr/share/wordlists/metasploit/unix_users.txt -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.1
```

### Web Login Attacks
```bash
toolbox> ai bruteforce http://example.com/login.php
Generated: hydra -l admin -P /usr/share/wordlists/rockyou.txt http-post-form "/login.php:username=^USER^&password=^PASS^:Invalid"

toolbox> ai attack FTP on 192.168.1.1
Generated: hydra -l admin -P /usr/share/wordlists/rockyou.txt ftp://192.168.1.1
```

## 📊 Enumeration

### SMB Enumeration
```bash
toolbox> ai enumerate SMB shares on 192.168.1.1
Generated: smbmap -H 192.168.1.1 -u guest

toolbox> ai list SMB users on 192.168.1.1
Generated: enum4linux -U 192.168.1.1

toolbox> ai check SMB on 192.168.1.1
Generated: enum4linux -a 192.168.1.1
```

### DNS Enumeration
```bash
toolbox> ai find subdomains of example.com
Generated: subfinder -d example.com

toolbox> ai enumerate DNS for example.com
Generated: dnsenum example.com

toolbox> ai check DNS records for example.com
Generated: dig example.com ANY
```

## 🎯 Context-Aware Examples

AI remembers your previous targets:

```bash
toolbox> ai scan 192.168.1.100
Generated: nmap -sV 192.168.1.100

toolbox> ai enumerate SMB shares
[AI] Remembering target: 192.168.1.100
Generated: smbmap -H 192.168.1.100

toolbox> ai brute force SSH
[AI] Using target: 192.168.1.100
Generated: hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.100
```

## ✏️ Edit Before Execution

```bash
toolbox> ai scan example.com
Generated: nmap -sV example.com
Execute? (y/n/e=edit/f=favorites): e

Edit command: nmap -sV -p- -T4 example.com
Execute? (y/n): y
```

## 💾 Save to Favorites

```bash
toolbox> ai scan 192.168.1.1 for all ports
Generated: nmap -p- 192.168.1.1
Execute? (y/n/e=edit/f=favorites): f

Favorite name: full-port-scan
[+] Added to favorites!

# Later use:
toolbox> full-port-scan 192.168.1.100
```

## 🚀 Advanced Examples

### Multi-Step Reconnaissance
```bash
toolbox> ai scan 192.168.1.1
toolbox> ai enumerate services
toolbox> ai check for vulnerabilities
toolbox> ai test for common exploits
```

### Wireless Testing
```bash
toolbox> ai scan for wireless networks
Generated: iwlist wlan0 scan

toolbox> ai monitor wireless on wlan0
Generated: airmon-ng start wlan0
```

### Information Gathering
```bash
toolbox> ai get whois info for example.com
Generated: whois example.com

toolbox> ai gather info about example.com
Generated: theHarvester -d example.com -b google

toolbox> ai find email addresses on example.com
Generated: theHarvester -d example.com -b all
```

## 💡 Tips for Better Results

1. **Be Specific**: More details = better commands
   - ❌ `ai scan target`
   - ✅ `ai scan 192.168.1.1 for web services`

2. **Use Context**: Reference previous targets
   - First: `ai scan 192.168.1.1`
   - Then: `ai enumerate SMB shares` (remembers target)

3. **Edit When Needed**: Use `e` to customize
4. **Save Favorites**: Use `f` for frequently used commands
5. **Clear Context**: Use `ai-clear` to start fresh

## 🎓 Learning from AI

Review AI-generated commands to learn proper syntax:

```bash
toolbox> ai scan for SQL injection on http://example.com/page.php?id=1
Generated: sqlmap -u "http://example.com/page.php?id=1" --dbs --batch

# Learn from this:
# - sqlmap is the tool for SQL injection
# - --dbs lists databases
# - --batch runs automatically
```

**Explore more at: [AI_SETUP.md](AI_SETUP.md)**
