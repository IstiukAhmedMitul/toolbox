# 🎨 Custom Commands Guide

## Add Your Own Commands to Toolbox!

Both AI and traditional mode can use your custom commands.

---

## Quick Start

### Add a Custom Command

```bash
toolbox> add-custom

Command name: my-quick-scan
Enter the command template:
Use {target} for target placeholder if needed
Example: nmap -p- -sV -sC {target}
Command: nmap -p- -T4 -sV -sC -A {target}
Description (optional): My fast comprehensive scan

[+] Custom command 'my-quick-scan' added successfully!
[+] Use it with: toolbox> use my-quick-scan
[+] Or with AI: toolbox> ai use my my-quick-scan on example.com
```

---

## Use Custom Commands

### Traditional Mode
```bash
toolbox> use my-quick-scan
Enter target: example.com

# Runs: nmap -p- -T4 -sV -sC -A example.com
```

### AI Mode
```bash
toolbox> ai use my custom scan on example.com

# AI recognizes your custom command and uses it!
```

---

## Manage Custom Commands

### List All Custom Commands
```bash
toolbox> list-custom

[+] Custom Commands:

1. my-quick-scan
   Description: My fast comprehensive scan
   Command: nmap -p- -T4 -sV -sC -A {target}
   Requires Target: Yes

2. my-sql-test
   Description: Quick SQL injection test
   Command: sqlmap -u {target} --batch --level=2
   Requires Target: Yes
```

### Remove Custom Command
```bash
toolbox> remove-custom my-quick-scan

[+] Custom command 'my-quick-scan' removed
```

---

## Examples

### Example 1: Custom Nmap Scan
```bash
toolbox> add-custom

Command name: full-scan
Command: nmap -p- -T4 -sV -sC -O -A -oN scan.txt {target}
Description: Complete nmap scan with all options

# Use it:
toolbox> use full-scan
Enter target: 192.168.1.1
```

### Example 2: Custom Web Scanner
```bash
toolbox> add-custom

Command name: web-recon
Command: nuclei -u {target} -t ~/nuclei-templates -o results.txt
Description: Full nuclei web reconnaissance

# Use it:
toolbox> use web-recon
Enter target: https://example.com
```

### Example 3: No Target Needed
```bash
toolbox> add-custom

Command name: update-tools
Command: sudo apt update && sudo apt upgrade -y
Description: Update all Kali tools

# Use it (no target required):
toolbox> use update-tools
```

### Example 4: Complex Custom Command
```bash
toolbox> add-custom

Command name: full-web-scan
Command: nikto -h {target} && dirb {target} /usr/share/wordlists/dirb/common.txt && whatweb {target}
Description: Complete web application scan

# Combines multiple tools in one command!
```

---

## Advanced: Edit Mode with Custom Commands

### Traditional Mode with Edit
```bash
toolbox> use my-quick-scan
Enter target: example.com

# Before execution:
Execute? (y/n/e=edit): e

Command: nmap -p- -T4 -sV -sC -A example.com
# Edit to: nmap -p 80,443 -T4 -sV -sC -A example.com

Execute edited command? (y/n): y
```

### AI Mode with Edit
```bash
toolbox> ai use my quick scan on example.com

[AI] ✓ Generated: nmap -p- -T4 -sV -sC -A example.com
Execute? (y/n/e=edit): e

Command: nmap -p- -T4 -sV -sC -A example.com
# Edit inline with arrow keys
# Add or remove flags as needed

Execute edited command? (y/n): y
```

---

## Tips & Best Practices

### 1. Use Descriptive Names
```bash
# ✅ Good
my-stealth-scan
quick-web-check
full-smb-enum

# ❌ Bad
scan1
test
x
```

### 2. Add Descriptions
Help yourself remember what each command does:
```bash
Description: Stealth SYN scan with version detection
```

### 3. Use {target} Placeholder
For commands that need a target:
```bash
Command: nmap -sS -sV {target}
```

### 4. Complex Commands Are OK
Chain multiple commands:
```bash
Command: nmap -sV {target} && nikto -h {target} && dirb {target}
```

### 5. Add Output Files
Save results automatically:
```bash
Command: nmap -sV -oN scan_{target}.txt {target}
```

---

## Real-World Examples

### Pentesting Workflow Commands

```bash
# 1. Initial Recon
toolbox> add-custom
Name: recon-full
Command: nmap -sV -sC {target} && whois {target} && dig {target}
Description: Complete initial reconnaissance

# 2. Web Application Testing
toolbox> add-custom
Name: web-full
Command: nikto -h {target} && gobuster dir -u {target} -w /usr/share/wordlists/dirb/common.txt
Description: Full web app testing

# 3. Subdomain Enumeration
toolbox> add-custom
Name: subdomain-hunt
Command: subfinder -d {target} && assetfinder {target} && amass enum -d {target}
Description: Comprehensive subdomain discovery

# 4. Password Attack
toolbox> add-custom
Name: ssh-brute
Command: hydra -L users.txt -P /usr/share/wordlists/rockyou.txt {target} ssh
Description: SSH brute force attack

# 5. Post-Exploitation
toolbox> add-custom
Name: linux-enum
Command: curl https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh | bash
Description: Linux enumeration script
```

---

## Integration with AI

Your custom commands are automatically available to AI!

```bash
# Add custom command
toolbox> add-custom
Name: my-special-scan
Command: nmap -p- -sV -sC -A {target}

# AI can now use it!
toolbox> ai use my special scan on example.com
[AI] ✓ Generated: nmap -p- -sV -sC -A example.com

# AI understands your custom tools!
toolbox> ai run my web recon on http://example.com
[AI] ✓ Generated: nikto -h http://example.com && gobuster...
```

---

## Storage

Custom commands are stored in:
```
~/.toolbox/custom_commands.json
```

They persist across sessions and are loaded automatically.

---

## FAQ

### Q: Can I edit existing custom commands?
**A:** Yes! Just add the command again with the same name. It will be updated.

### Q: Do custom commands work in workflows?
**A:** Yes! Use them like any other tool.

### Q: Can AI suggest my custom commands?
**A:** Yes! AI has access to all your custom commands.

### Q: What if my command has no target?
**A:** That's fine! Just don't use {target} in the command.

### Q: Can I share custom commands with team?
**A:** Yes! Share your `~/.toolbox/custom_commands.json` file.

### Q: Can I import someone else's custom commands?
**A:** Yes! Copy their `custom_commands.json` to your `~/.toolbox/` directory.

---

## Summary

✅ **Add**: `add-custom`  
✅ **List**: `list-custom`  
✅ **Remove**: `remove-custom`  
✅ **Use**: `use <name>` or `ai use my <name>`  
✅ **Edit**: Use `e` option when prompted  
✅ **Persistent**: Saved automatically  

Your commands + AI = Unlimited possibilities! 🚀
