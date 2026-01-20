# 🎯 Toolbox v2.0 - Complete Feature Guide

## Quick Start Examples

### Example 1: Smart Search by Category
```bash
# Want directory bruteforce tools?
$ toolbox directorybrutforce

[+] Results for 'directorybrutforce':

[Category Match]
  - gobuster: Directory/file, DNS and VHost busting tool
  - dirb: Web content scanner
  - ffuf: Fast web fuzzer
  - feroxbuster: Fast, simple, recursive content discovery tool
  - wfuzz: Web application fuzzer

[+] Use 'toolbox -c <tool> --help' for detailed help
```

### Example 2: Detailed Tool Help
```bash
$ toolbox -c nmap --help

================================================================================
Tool: nmap
Description: Network discovery and security auditing
Requires Target: Yes
Requires Wordlist: No
Total Commands: 25
================================================================================

[+] Available commands for nmap:

  1. nmap {target}
     Basic TCP scan on the target

  2. nmap -sV {target}
     Scan open ports and determine service/version info

  3. nmap -sS -sV -O {target}
     Stealth SYN scan with version detection and OS detection
  
  ... (22 more commands)

================================================================================
Usage: toolbox use nmap
       toolbox --tool nmap
================================================================================
```

### Example 3: Multi-Target Scanning
```bash
$ toolbox

toolbox> use nmap
[+] Tool: nmap
[+] Description: Network discovery and security auditing

Enter target(s) (IP/domain, comma-separated for multiple): 192.168.1.1, 192.168.1.2, 192.168.1.5
[+] Multi-target mode: 3 targets

[+] Available commands for nmap:
  1. nmap 192.168.1.1
     Basic TCP scan on the target
  2. nmap -sV 192.168.1.1
     Scan open ports and determine service/version info
  ...

Select command (1-25): 2

[+] Executing on 3 targets...

[1/3] Target: 192.168.1.1
Execute? (y/n/s=skip remaining): y
[+] Executing: nmap -sV 192.168.1.1
...
[+] Output saved to: ~/.toolbox/outputs/scans/20260120_143022_nmap_192.168.1.1.txt

[2/3] Target: 192.168.1.2
Execute? (y/n/s=skip remaining): y
...
```

### Example 4: Using Favorites
```bash
$ toolbox

toolbox> use gobuster
Enter target(s): example.com

[+] Available commands for gobuster:
  1. gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt
     Directory brute force with wordlist
  ...

Select command: 1

Command: gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt
Execute? (y/n/f=add to favorites/t=save as template): f
Favorite name (optional): quick-gobuster
[+] Added to favorites as 'quick-gobuster'

# Later, view favorites
toolbox> favorites

[+] Favorite commands:
  1. quick-gobuster
     Tool: gobuster
     Command: gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt
```

### Example 5: Command History
```bash
$ toolbox --history

[+] Last 20 commands:
  1. [2026-01-20 14:30:22] nmap: nmap -sV 192.168.1.1
     Target: 192.168.1.1
  2. [2026-01-20 14:32:15] gobuster: gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt
     Target: example.com
  3. [2026-01-20 14:35:40] nikto: nikto -h http://example.com
     Target: example.com
  ...

# Or in interactive mode
toolbox> history 50
# Shows last 50 commands
```

### Example 6: Creating and Using Templates
```bash
# Save a template
$ toolbox --save-template nmap-full --template-cmd "nmap -sV -sC -p- -T4 -oA scan_{target} {target}"
[+] Template 'nmap-full' saved

# View templates
$ toolbox --templates

[+] Saved templates:
  - nmap-full: nmap -sV -sC -p- -T4 -oA scan_{target} {target}
    Description: nmap template

# Use template in interactive mode
toolbox> use nmap
Enter target: 192.168.1.1
...
Execute? (y/n/f=add to favorites/t=save as template): t
Template name: my-custom-scan
[+] Template 'my-custom-scan' saved
```

### Example 7: Creating Workflows
```bash
# Create a workflow
$ toolbox --create-workflow web-full-recon
[+] Workflow 'web-full-recon' created

# Add commands to workflow (in interactive mode)
toolbox> use nmap
# Select nmap command
# Choose to add to workflow when prompted

toolbox> use gobuster
# Select gobuster command
# Add to same workflow

toolbox> use nikto
# Select nikto command
# Add to workflow

# Run the workflow
$ toolbox --run-workflow web-full-recon --target example.com

[+] Running workflow: web-full-recon
[+] Total commands: 3

[1/3] Running: nmap
Execute: nmap -sV example.com? (y/n/s=skip all): y
[+] Executing: nmap -sV example.com
...

[2/3] Running: gobuster
Execute: gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt? (y/n/s=skip all): y
...

[3/3] Running: nikto
Execute: nikto -h http://example.com? (y/n/s=skip all): y
...

[+] Workflow 'web-full-recon' completed
```

### Example 8: Tool Availability Check
```bash
$ toolbox --doctor

[+] Checking tool availability...

[+] Available: 87 tools
[!] Missing: 13 tools

[!] Missing tools:
  - rustscan
  - nuclei
  - subfinder
  - httpx
  - dalfox
  - jwt_tool
  - ghidra
  - one_gadget
  - pspy
  - volatility
  - arjun
  - assetfinder
  - gau
```

### Example 9: Configuration Management
```bash
$ toolbox --config

[+] Current configuration:
  default_wordlist: /usr/share/wordlists/rockyou.txt
  output_auto_save: true
  show_banner: true
  history_limit: 1000
  theme: default

[+] Config directory: /home/user/.toolbox
[+] Output directory: /home/user/.toolbox/outputs
```

### Example 10: API Server Usage
```bash
# Start the API server
$ python3 toolbox_api.py

╔══════════════════════════════════════════╗
║      Toolbox API Server v2.0             ║
╚══════════════════════════════════════════╝

⚠️  WARNING: This API has NO authentication!
   Use only in trusted networks!

Server: http://127.0.0.1:5000
API Docs: http://127.0.0.1:5000/

Press Ctrl+C to stop

# In another terminal, use the API
$ curl http://localhost:5000/api/tools | jq '.nmap'
{
  "description": "Network discovery and security auditing",
  "requires_target": true,
  "requires_wordlist": false,
  "commands_count": 25
}

$ curl http://localhost:5000/api/search?q=directory | jq '.exact'
[
  "gobuster",
  "dirb",
  "ffuf",
  "feroxbuster",
  "wfuzz"
]

$ curl http://localhost:5000/api/history | jq '.[0]'
{
  "timestamp": "2026-01-20T14:30:22.123456",
  "tool": "nmap",
  "command": "nmap -sV 192.168.1.1",
  "target": "192.168.1.1"
}
```

## All New Commands

### Command Line
```bash
toolbox <query>                    # Search by tool name or category
toolbox -c <tool> --help          # Detailed help for tool
toolbox --list                     # List all tools
toolbox --search <query>           # Search tools
toolbox --tool <name>              # Use specific tool
toolbox --history                  # Show history
toolbox --favorites                # Show favorites
toolbox --templates                # Show templates
toolbox --workflows                # Show workflows
toolbox --doctor                   # Check tool availability
toolbox --config                   # Show configuration
toolbox --create-workflow <name>   # Create workflow
toolbox --run-workflow <name>      # Run workflow
toolbox --target <target>          # Set workflow target
toolbox --save-template <name>     # Save template
toolbox --template-cmd <cmd>       # Template command
```

### Interactive Mode
```bash
help                              # Show help
list                              # List tools
search <query>                    # Search tools
use <tool>                        # Use tool
history [n]                       # Show history
favorites                         # Show favorites
templates                         # Show templates
workflows                         # Show workflows
doctor                            # Check availability
config                            # Show config
q/quit/exit                       # Exit
```

## Category Keywords

Use these with `toolbox <category>`:

- **directorybrutforce** / **directory** - Directory discovery tools
- **subdomain** - Subdomain enumeration
- **passwords** / **cracking** - Password tools
- **bruteforce** - Brute force tools
- **web** - Web testing tools
- **scanning** / **reconnaissance** - Network scanning
- **enumeration** - Enumeration tools
- **crypto** - Cryptography tools
- **reversing** - Reverse engineering
- **forensics** - Forensics tools
- **exploitation** - Exploitation tools
- **privesc** - Privilege escalation
- **network** - Network utilities
- **wireless** - Wireless tools
- **osint** - OSINT tools
- **xss** - XSS testing
- **sql** - SQL injection
- **api** - API testing

## Output Management

All command outputs are automatically saved to:
```
~/.toolbox/outputs/scans/
```

Format: `YYYYMMDD_HHMMSS_<tool>_<target>.txt`

Example:
```
20260120_143022_nmap_192.168.1.1.txt
20260120_143545_gobuster_example.com.txt
```

Each file contains:
- Tool name
- Full command
- Target
- Timestamp
- Complete output (stdout and stderr)

## Configuration Files

Located in `~/.toolbox/`:

```
~/.toolbox/
├── config.json          # User preferences
├── history.json         # Command history
├── favorites.json       # Favorite commands
├── templates.json       # Command templates
├── workflows.json       # Saved workflows
└── outputs/
    ├── scans/           # Command outputs
    └── reports/         # Generated reports
```

## Pro Tips

1. **Quick Tool Access**: Just type the tool name
   ```bash
   toolbox nmap     # Faster than toolbox --tool nmap
   ```

2. **Category Search**: Use descriptive keywords
   ```bash
   toolbox directorybrutforce
   toolbox subdomain
   toolbox passwords
   ```

3. **Multi-Target**: Use commas for multiple targets
   ```bash
   Enter target: 10.10.10.1, 10.10.10.2, 10.10.10.3
   ```

4. **Favorites**: Press 'f' instead of 'y' to save as favorite

5. **Templates**: Press 't' to save as reusable template

6. **History**: Use `history` command to recall previous commands

7. **Skip**: In multi-target mode, press 's' to skip remaining

8. **Output**: All outputs auto-saved in `~/.toolbox/outputs/`

## Advanced Workflow Example

```bash
# 1. Create comprehensive recon workflow
toolbox --create-workflow full-recon

# 2. Add commands interactively
toolbox
toolbox> use nmap
# Add: nmap -sV -sC {target}

toolbox> use gobuster
# Add: gobuster dir -u http://{target} -w /path/wordlist

toolbox> use nikto
# Add: nikto -h http://{target}

toolbox> use wpscan
# Add: wpscan --url http://{target}

# 3. Run on multiple targets
toolbox --run-workflow full-recon --target "example.com"

# 4. Check outputs
ls ~/.toolbox/outputs/scans/

# 5. Review history
toolbox --history
```

## Troubleshooting Common Issues

### Issue: "Category not found"
**Solution**: Use `toolbox --list` to see all available tools and categories

### Issue: Output not saving
**Solution**: Check config with `toolbox --config` and ensure `output_auto_save: true`

### Issue: Can't find command history
**Solution**: Check `~/.toolbox/history.json` exists and has proper permissions

### Issue: Workflow not saving
**Solution**: Ensure `~/.toolbox/workflows.json` is writable

### Issue: API server won't start
**Solution**: Install Flask: `pip3 install flask flask-cors`

---

**You now have a professional-grade cybersecurity command assistant! 🎉**
