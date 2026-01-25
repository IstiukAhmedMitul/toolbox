# 🚀 AI Quick Start Examples

Get started with AI-powered commands in seconds!

## Basic Usage

```bash
# Start Toolbox
toolbox

# Your first AI command
toolbox> ai scan example.com
[AI] 🤖 Generating command...
[AI] ✓ Generated: nmap -sV -sC example.com
Execute? (y/n/e=edit/f=favorites): y
```

## Common Tasks

### 1. Port Scanning
```bash
toolbox> ai quick scan of 192.168.1.1
toolbox> ai full port scan on 192.168.1.100
toolbox> ai scan ports 80 and 443 on example.com
```

### 2. Web Scanning
```bash
toolbox> ai scan http://example.com for vulnerabilities
toolbox> ai find hidden directories on http://example.com
toolbox> ai enumerate http://example.com
```

### 3. Subdomain Discovery
```bash
toolbox> ai find subdomains of example.com
toolbox> ai enumerate DNS for example.com
toolbox> ai discover all subdomains of target.com
```

### 4. Web Application Attacks
```bash
toolbox> ai test for SQL injection on http://example.com/login
toolbox> ai find XSS vulnerabilities on http://example.com
toolbox> ai brute force directories on http://example.com
```

### 5. Password Attacks
```bash
toolbox> ai brute force SSH on 192.168.1.100
toolbox> ai crack password hash in hash.txt
toolbox> ai brute force FTP on 192.168.1.50
```

### 6. Network Enumeration
```bash
toolbox> ai enumerate SMB shares on 192.168.1.100
toolbox> ai scan network 192.168.1.0/24
toolbox> ai find live hosts on 192.168.1.0/24
```

## Context-Aware Conversations

The AI remembers your targets:

```bash
toolbox> ai scan example.com
[AI] ✓ Generated: nmap -sV -sC example.com

toolbox> ai now scan port 8080
# AI remembers "example.com"
[AI] ✓ Generated: nmap -p 8080 -sV example.com

toolbox> ai find subdomains
# Still working on example.com
[AI] ✓ Generated: subfinder -d example.com

toolbox> ai-clear
[+] AI context cleared

toolbox> ai scan another target
# Now it will ask for a new target
```

## Editing Commands

```bash
toolbox> ai scan example.com
[AI] ✓ Generated: nmap -sV -sC example.com
Execute? (y/n/e=edit/f=favorites): e

Command: nmap -sV -sC -p 1-1000 example.com  ← Edit here
Execute edited command? (y/n): y
```

## Saving Favorites

```bash
toolbox> ai comprehensive scan of example.com
[AI] ✓ Generated: nmap -sV -sC -O -A -p- example.com
Execute? (y/n/e=edit/f=favorites): f

Favorite name (optional): full-scan
[+] Added to favorites!

# Later, use it from favorites
toolbox> favorites
```

## AI Management Commands

```bash
# Check if AI is working
toolbox> ai-status

# Configure AI model
toolbox> ai-config

# Show conversation context
toolbox> ai-context

# Clear context (fresh start)
toolbox> ai-clear

# Show setup help
toolbox> ai-help
```

## Tips for Better Results

### ✅ DO: Be Specific
```bash
toolbox> ai scan example.com for open ports
toolbox> ai find admin directories on http://example.com
toolbox> ai test http://example.com/login for SQL injection
```

### ❌ DON'T: Be Too Vague
```bash
toolbox> ai scan
toolbox> ai test it
toolbox> ai find stuff
```

### ✅ DO: Include Targets
```bash
toolbox> ai scan 192.168.1.1 port 80
toolbox> ai enumerate SMB on 192.168.1.100
```

### ❌ DON'T: Forget the Target (unless using context)
```bash
toolbox> ai scan port 80  # Which target?
```

## Safety Features

The AI includes automatic safety checks:

```bash
toolbox> ai delete everything
[AI] ✓ Generated: rm -rf /

⚠️  DANGEROUS: Command contains potentially harmful pattern
This command may be dangerous. Continue? (yes/no): no
[!] Command cancelled for safety.
```

## Example Workflow

Complete penetration test workflow using AI:

```bash
# 1. Initial port scan
toolbox> ai scan 192.168.1.100
[AI] ✓ Generated: nmap -sV -sC 192.168.1.100
Execute? (y/n): y

# 2. Found port 80 open, scan web server
toolbox> ai scan web server on port 80
[AI] ✓ Generated: nikto -h http://192.168.1.100
Execute? (y/n): y

# 3. Find hidden directories
toolbox> ai find hidden directories
[AI] ✓ Generated: gobuster dir -u http://192.168.1.100 -w /usr/share/wordlists/dirb/common.txt
Execute? (y/n): y

# 4. Found /admin, test for SQL injection
toolbox> ai test http://192.168.1.100/admin for SQL injection
[AI] ✓ Generated: sqlmap -u "http://192.168.1.100/admin" --forms --batch
Execute? (y/n): y

# 5. Clear context for next target
toolbox> ai-clear
```

---

## Need Help?

- **Setup Issues**: See [AI_SETUP.md](AI_SETUP.md)
- **Troubleshooting**: `toolbox> ai-status`
- **Commands Not Working**: `toolbox> ai-clear` and try again
- **Model Issues**: `toolbox> ai-config` to switch models

---

## Ready to Go!

Try your first command:

```bash
toolbox> ai scan scanme.nmap.org
```

Enjoy the power of natural language! 🚀
