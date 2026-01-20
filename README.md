# 🛡️ Toolbox v2.0 - Professional Cybersecurity Command Assistant

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![Platform](https://img.shields.io/badge/platform-Kali%20Linux-red)
![License](https://img.shields.io/badge/license-MIT-green)
![Tools](https://img.shields.io/badge/tools-100%2B-orange)

> Never forget command syntax again! Your personal cybersecurity command assistant with 100+ tools, intelligent features, and Hollywood hacker mode.

---

## 🎯 What is Toolbox?

Toolbox is a **professional command-line assistant** designed for penetration testers, ethical hackers, and CTF players. It helps you remember complex command syntax, discover new tools, and execute security scans with confidence.

### ✨ Why Toolbox?

- 🧠 **Forget Memorization** - No more googling command syntax
- 🚀 **100+ Tools Ready** - Nmap, Gobuster, SQLMap, Metasploit, and more
- 🎨 **Interactive & Beautiful** - Metasploit-style banner and clean interface
- 💪 **Professional Features** - History, favorites, workflows, templates
- 🎬 **Hollywood Mode** - Look like a movie hacker (just for fun!)
- 🔧 **Auto-Install** - Prompts to install missing tools automatically

---

## 🎥 Demo

```bash
$ toolbox

╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ████████╗ ██████╗  ██████╗ ██╗     ██████╗  ██████╗ ██╗  ██╗          ║
║   ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔══██╗██╔═══██╗╚██╗██╔╝          ║
║      ██║   ██║   ██║██║   ██║██║     ██████╔╝██║   ██║ ╚███╔╝           ║
║      ██║   ██║   ██║██║   ██║██║     ██╔══██╗██║   ██║ ██╔██╗           ║
║      ██║   ╚██████╔╝╚██████╔╝███████╗██████╔╝╚██████╔╝██╔╝ ██╗          ║
║      ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝          ║
║                                                                            ║
║              Professional Cybersecurity Command Assistant                  ║
║                          Version 2.0                                       ║
╚════════════════════════════════════════════════════════════════════════════╝

[*] Over 100+ Security Tools at Your Fingertips
[*] Command History | Favorites | Workflows | Templates
[*] Multi-Target Support | Output Management | API Interface
[*] Hollywood Hacker Mode Included (Just For Fun!)

toolbox> 
```

---

## 🚀 Quick Start

### Installation (Kali Linux)

```bash
# Clone the repository
git clone https://github.com/IstiukAhmedMitul/toolbox.git
cd toolbox

# Run automated installer
chmod +x install.sh
./install.sh

# Or manual installation
sudo cp toolbox.py /usr/local/bin/toolbox
sudo chmod +x /usr/local/bin/toolbox
```

### Basic Usage

```bash
# Interactive mode
toolbox

# Search by category
toolbox directorybrutforce
toolbox subdomain

# Get detailed help for a tool
toolbox -c nmap --help

# Use a tool interactively
toolbox --tool nmap

# List all tools
toolbox --list

# Check installed tools
toolbox --doctor
```

---

## 🎯 Features

### 🔥 Core Features

- **100+ Security Tools** - Comprehensive database of penetration testing tools
- **Smart Search** - Find tools by category, name, or description
- **Interactive Mode** - User-friendly CLI with command completion
- **Command History** - Track all executed commands with timestamps
- **Favorites System** - Save frequently used commands for quick access
- **Multi-Target Support** - Execute commands on multiple targets sequentially
- **Edit on the Fly** - Modify commands before execution with inline editing
- **Auto-Install Prompt** - Automatically asks to install missing tools

### 🎨 Advanced Features

- **Workflow Automation** - Chain multiple commands into workflows
- **Command Templates** - Save and reuse command patterns with variables
- **Output Management** - Save scan results with custom filenames
- **Configuration System** - Customize behavior with JSON config
- **Tool Availability Checker** - See what's installed on your system
- **REST API Interface** - Optional Flask API for automation (v2.0)

### 🎬 Hollywood Hacker Mode

Just for fun! Look like you're in a movie:

```bash
toolbox cmatrix      # Matrix falling code
toolbox hollywood    # Full hacker terminal
toolbox cowsay       # ASCII cow says things
toolbox figlet       # Big ASCII art text
toolbox lolcat       # Rainbow colors
```

---

## 📚 Tool Categories

### 🔍 Reconnaissance & Scanning
- Nmap (35 commands including combinations!)
- RustScan, Masscan, Netdiscover
- Whois, Dig, NSLookup

### 🌐 Web Application Testing
- SQLMap, Nikto, WPScan
- Nuclei, Burp Suite, ZAP
- Commix, JWT Tool

### 📁 Directory Discovery
- Gobuster, Dirb, FFuf
- Feroxbuster, Wfuzz

### 🔐 Password Cracking
- Hydra, John the Ripper
- Hashcat, Medusa

### 🕵️ OSINT & Enumeration
- TheHarvester, Subfinder
- Amass, Sublist3r, HTTPx

### 🐛 Exploitation
- Metasploit, SearchSploit
- Msfvenom, Weevely

### 🔓 Privilege Escalation
- LinPEAS, WinPEAS
- PSPY, Linux Smart Enumeration

### 🔬 Forensics & Analysis
- Volatility, Autopsy
- Foremost, Binwalk, Ghidra

### 🎭 Reverse Engineering
- Radare2, GDB, Ghidra
- PwnTools, Ropper, Checksec

### 🔒 Cryptography
- OpenSSL, GPG, Steghide
- Hash-Identifier, Base64

### 🎬 Hollywood Hacker (Fun!)
- CMatrix, Hollywood, Cowsay
- Figlet, Lolcat, SL

**And 70+ more tools!**

---

## 💡 Usage Examples

### Example 1: Quick Nmap Scan

```bash
$ toolbox --tool nmap
Enter target: 192.168.1.100
Select command (1-35): 2
Command: nmap -sV 192.168.1.100
Execute? (y/n/e=edit/f=favorites/t=template): y
```

### Example 2: Edit Command Before Running

```bash
Command: nmap -p- -T4 192.168.1.100
Execute? (y/n/e=edit/f=favorites/t=template): e

[+] Edit mode - Command is pre-filled, modify as needed:
Command: nmap -p- -T4 -A 192.168.1.100█  # Add -A with cursor
```

### Example 3: Multi-Target Scanning

```bash
Enter targets: 192.168.1.1,192.168.1.2,192.168.1.3
[+] Multi-target mode: 3 targets
# Executes on each target sequentially
```

### Example 4: Save Custom Output

```bash
[+] Command completed with exit code: 0
[?] Next action? (r=run another/s=save as/q=quit): s
Save output as: scan_results.txt
[+] Output saved to: scan_results.txt
```

### Example 5: Create Workflow

```bash
toolbox --create-workflow recon
# Add commands to workflow
toolbox --run-workflow recon --target example.com
```

---

## 🔧 Configuration

Configuration file: `~/.toolbox/config.json`

```json
{
  "default_wordlist": "/usr/share/wordlists/rockyou.txt",
  "output_auto_save": false,
  "show_banner": true,
  "history_limit": 1000,
  "theme": "default"
}
```

---

## 🌐 REST API (Optional)

Start the API server:

```bash
python3 toolbox_api.py
```

Endpoints:
- `GET /api/tools` - List all tools
- `GET /api/tools/<name>` - Get tool details
- `POST /api/execute` - Execute command
- `GET /api/history` - Command history
- `GET /api/doctor` - Check tool availability

---

## 📖 Documentation

- [Installation Guide](INSTALLATION.md)
- [Features Guide](FEATURES_GUIDE.md)
- [Quick Reference](QUICK_REFERENCE.md)
- [GitHub Setup](GITHUB_SETUP.md)
- [What's New in v2.0](WHATS_NEW.md)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Add New Tools** - Submit tools with command examples
2. **Report Bugs** - Open an issue with details
3. **Improve Docs** - Help make documentation better
4. **Share Ideas** - Suggest new features

### Adding a Tool

```python
"tool_name": {
    "description": "Tool description",
    "requires_target": True,
    "requires_wordlist": False,
    "commands": [
        {
            "command": "tool {target}",
            "description": "What this command does"
        }
    ]
}
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by Metasploit Framework
- Built for the cybersecurity community
- Special thanks to all penetration testers and CTF players

---

## 📞 Support

- **GitHub Issues**: Report bugs or request features
- **Documentation**: Check the docs folder
- **Community**: Share your experience!

---

## ⭐ Star This Project

If you find Toolbox useful, please give it a star! It helps others discover the tool.

---

## 🎯 Roadmap

- [ ] Add more tools (200+ goal)
- [ ] GUI interface (optional)
- [ ] Plugin system
- [ ] Tool version checking
- [ ] Custom wordlist manager
- [ ] Scan result parser
- [ ] Report generation
- [ ] Team collaboration features

---

## 📸 Screenshots

### Interactive Mode
![Interactive Mode](screenshots/interactive.png)

### Tool Selection
![Tool Selection](screenshots/tool-selection.png)

### Hollywood Mode
![Hollywood Mode](screenshots/hollywood.png)

---

## 🔥 Why Toolbox is Different

| Feature | Toolbox | Manual Commands | Other Tools |
|---------|---------|-----------------|-------------|
| 100+ Tools | ✅ | ❌ | ⚠️ Some |
| Command History | ✅ | ❌ | ⚠️ Limited |
| Edit Before Run | ✅ | ❌ | ❌ |
| Multi-Target | ✅ | ❌ | ⚠️ Some |
| Workflows | ✅ | ❌ | ❌ |
| Auto-Install | ✅ | ❌ | ❌ |
| Hollywood Mode | ✅ | ❌ | ❌ |
| Free & Open Source | ✅ | ✅ | ⚠️ Some |

---

## 💻 System Requirements

- **OS**: Kali Linux (recommended), Parrot OS, Ubuntu, Debian
- **Python**: 3.6 or higher
- **Storage**: ~50MB
- **Internet**: Required for installing tools

---

## 🚀 Quick Commands Cheat Sheet

```bash
toolbox                           # Interactive mode with banner
toolbox nmap                      # Show nmap commands
toolbox -c nmap --help           # Detailed nmap help
toolbox --tool nmap              # Use nmap interactively
toolbox --list                   # List all tools by category
toolbox --doctor                 # Check installed tools
toolbox --history                # View command history
toolbox --favorites              # View favorite commands
toolbox directorybrutforce       # Find directory bruteforce tools
toolbox subdomain                # Find subdomain enumeration tools
toolbox hollywood                # Hollywood hacker mode!
```

---

<div align="center">

### Made with ❤️ for the Cybersecurity Community

**[⭐ Star](https://github.com/YOUR-USERNAME/toolbox)** • **[🐛 Report Bug](https://github.com/YOUR-USERNAME/toolbox/issues)** • **[✨ Request Feature](https://github.com/YOUR-USERNAME/toolbox/issues)**

---

**Hack Responsibly. Always Get Permission. Stay Legal.** 🛡️

</div>

