# Toolbox Quick Reference Card

## 🚀 Quick Start

```bash
# Launch toolbox
toolbox

# Show help
toolbox --help

# List all tools
toolbox --list

# Search for tools
toolbox --search "nmap"

# Use specific tool
toolbox --tool nmap
```

## 📖 Interactive Mode Commands

| Command | Description |
|---------|-------------|
| `help` | Show available commands |
| `list` | List all tools by category |
| `search <query>` | Search tools by name/description |
| `use <tool>` | Interact with specific tool |
| `<toolname>` | Direct tool access |
| `q` or `quit` | Exit toolbox |

## 🛠️ Most Used Tools

### Reconnaissance
```bash
toolbox> use nmap          # Network scanning
toolbox> use rustscan      # Fast port scanner
toolbox> use masscan       # Very fast scanner
```

### Web Testing
```bash
toolbox> use nikto         # Web vulnerability scanner
toolbox> use wpscan        # WordPress scanner
toolbox> use sqlmap        # SQL injection tool
toolbox> use nuclei        # Template-based scanner
```

### Directory Discovery
```bash
toolbox> use gobuster      # Directory/file brute-force
toolbox> use ffuf          # Fast fuzzer
toolbox> use dirb          # Web content scanner
toolbox> use feroxbuster   # Recursive content discovery
```

### Subdomain Enumeration
```bash
toolbox> use subfinder     # Subdomain discovery
toolbox> use sublist3r     # Subdomain enumeration
toolbox> use amass         # Attack surface mapping
toolbox> use assetfinder   # Domain finder
```

### Credential Testing
```bash
toolbox> use hydra         # Login brute-force
toolbox> use john          # Password cracker
toolbox> use hashcat       # Advanced password recovery
toolbox> use medusa        # Parallel brute-forcer
```

### Cryptography
```bash
toolbox> use openssl       # Encryption/certificates
toolbox> use gpg           # GPG encryption
toolbox> use base64        # Base64 encoding/decoding
toolbox> use hash-identifier  # Identify hash types
```

### Reverse Engineering
```bash
toolbox> use ghidra        # NSA reverse engineering
toolbox> use radare2       # RE framework
toolbox> use gdb           # GNU debugger
toolbox> use strings       # Extract strings
toolbox> use objdump       # Display object info
```

### Privilege Escalation
```bash
toolbox> use linpeas       # Linux PrivEsc script
toolbox> use winpeas       # Windows PrivEsc script
toolbox> use pspy          # Process monitor
```

### Forensics
```bash
toolbox> use volatility    # Memory forensics
toolbox> use foremost      # File carving
toolbox> use binwalk       # Firmware analysis
toolbox> use exiftool      # Metadata viewer
```

### Steganography
```bash
toolbox> use steghide      # Hide data in images
toolbox> use stegcracker   # Brute-force steghide
toolbox> use exiftool      # Check metadata
```

### Network Utilities
```bash
toolbox> use netcat        # Network swiss army knife
toolbox> use curl          # Transfer data
toolbox> use wget          # Network downloader
```

## 📁 Common Wordlist Locations

```bash
# Passwords
/usr/share/wordlists/rockyou.txt

# Directories
/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
/usr/share/wordlists/dirb/common.txt
/usr/share/seclists/Discovery/Web-Content/common.txt

# Subdomains
/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# Usernames
/usr/share/seclists/Usernames/top-usernames-shortlist.txt
```

## 💡 Workflow Examples

### Web Application Pentest
```bash
1. toolbox> use nmap           # Port scan
2. toolbox> use nikto          # Web vulnerabilities
3. toolbox> use gobuster       # Directory discovery
4. toolbox> use wpscan         # WordPress scan (if applicable)
5. toolbox> use sqlmap         # SQL injection testing
```

### Network Pentest
```bash
1. toolbox> use nmap           # Network discovery
2. toolbox> use enum4linux     # SMB enumeration
3. toolbox> use smbmap         # SMB shares
4. toolbox> use crackmapexec   # Network pentesting
5. toolbox> use hydra          # Service brute-force
```

### OSINT Workflow
```bash
1. toolbox> use whois          # Domain registration
2. toolbox> use theHarvester   # Email/subdomain gathering
3. toolbox> use sublist3r      # Subdomain enumeration
4. toolbox> use amass          # Attack surface mapping
5. toolbox> use waybackurls    # Historical URLs
```

### CTF Workflow
```bash
1. toolbox> use nmap           # Port scan
2. toolbox> use gobuster       # Directory brute-force
3. toolbox> use binwalk        # Firmware/file analysis
4. toolbox> use steghide       # Steganography
5. toolbox> use hash-identifier # Identify hashes
6. toolbox> use john           # Crack passwords
```

## ⚡ Pro Tips

1. **Target Persistence**: Toolbox remembers your target during a session
2. **Wordlist Suggestions**: Always shows available wordlists with status
3. **Command Variations**: Multiple options for each tool, choose wisely
4. **Direct Access**: Type tool name directly in interactive mode
5. **Search Smart**: Use keywords like "web", "scan", "crypto" to find tools

## 🔧 Installation Commands

```bash
# Make executable
chmod +x toolbox.py

# Install globally (symbolic link)
sudo ln -s $(pwd)/toolbox.py /usr/local/bin/toolbox

# Or copy to system path
sudo cp toolbox.py /usr/local/bin/toolbox
sudo chmod +x /usr/local/bin/toolbox

# Test installation
toolbox --help
```

## 🐛 Troubleshooting

```bash
# Command not found
which toolbox
echo $PATH

# Permission denied
chmod +x toolbox.py

# Python not found
python3 --version

# Tool not installed
sudo apt install <tool-name>
```

## 📦 Essential Tools to Install

```bash
sudo apt update

# Core tools
sudo apt install -y nmap gobuster nikto wpscan sqlmap hydra john \
  hashcat netcat-traditional curl wget enum4linux smbmap \
  crackmapexec binwalk radare2 gdb steghide exiftool

# Python tools
pip3 install pwntools

# Wordlists
sudo git clone https://github.com/danielmiessler/SecLists.git /opt/SecLists
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
```

## 🎯 Keyboard Shortcuts

- `Ctrl+C` - Cancel current operation
- `Ctrl+D` - Exit toolbox
- `↑/↓` - Navigate command history
- `Tab` - Auto-complete (if configured)

## 📞 Help & Support

- GitHub Issues: Report bugs and request features
- README.md: Comprehensive documentation
- INSTALLATION.md: Detailed installation guide
- GITHUB_SETUP.md: Repository management

## ⚠️ Legal Reminder

- Always get authorization before testing
- Use only on systems you own or have permission to test
- Follow responsible disclosure practices
- Respect privacy and laws

---

**Print this reference card and keep it handy! 📄**

*Last Updated: January 2026*
