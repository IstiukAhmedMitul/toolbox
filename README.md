# 🛡️ Toolbox v2.0 + AI - Professional Cybersecurity Command Assistant

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![Platform](https://img.shields.io/badge/platform-Kali%20Linux-red)
![License](https://img.shields.io/badge/license-MIT-green)
![Tools](https://img.shields.io/badge/tools-100%2B-orange)
![AI](https://img.shields.io/badge/AI-Powered-purple)

> Never forget command syntax again! Your personal cybersecurity command assistant with 100+ tools, **AI-powered natural language commands**, custom commands, and Hollywood hacker mode.

---

## 🎯 What is Toolbox?

Toolbox is a **professional command-line assistant** designed for penetration testers, ethical hackers, and CTF players. It helps you remember complex command syntax, discover new tools, and execute security scans with confidence.

### ✨ Why Toolbox?

- 🧠 **Forget Memorization** - No more googling command syntax
- 🤖 **AI-Powered** - Natural language to commands (NEW!)
- 🚀 **100+ Tools Ready** - Nmap, Gobuster, SQLMap, Metasploit, and more
- 🎨 **Interactive & Beautiful** - Metasploit-style banner and clean interface
- 💪 **Professional Features** - History, favorites, workflows, templates
- 🎨 **Custom Commands** - Add your own frequently-used commands (NEW!)
- 🎬 **Hollywood Mode** - Look like a movie hacker (just for fun!)
- 🔧 **Auto-Install** - Prompts to install missing tools automatically
- 📝 **Enhanced Wordlists** - Dynamic SecLists detection with 20+ lists (NEW!)

---

## 🤖 NEW: AI-Powered Natural Language Commands

Simply describe what you want to do in plain English:

```bash
toolbox> ai scan example.com for vulnerabilities
[AI] 🤖 Generating command...
[AI] ✓ Generated: nmap -sV -sC example.com
Execute? (y/n/e=edit): y

toolbox> ai find subdomains of example.com
[AI] ✓ Generated: subfinder -d example.com

toolbox> ai test for SQL injection on http://example.com/login
[AI] ✓ Generated: sqlmap -u "http://example.com/login" --forms --batch
```

**AI Features:**
- 🗣️ Natural language understanding
- 🧠 Context-aware conversations (remembers targets)
- ✅ Safety validation
- ✏️ Edit before execution
- 💾 Save to favorites
- ⚡ Fast & FREE (powered by Groq)
- ☁️ No local installation required

**See [AI_SETUP.md](AI_SETUP.md) for setup instructions**

---

## 🎥 Demo

```bash
$ toolbox

╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ████████╗ ██████╗  ██████╗ ██╗     ██████╗  ██████╗ ██╗  ██╗             ║
║   ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔══██╗██╔═══██╗╚██╗██╔╝             ║
║      ██║   ██║   ██║██║   ██║██║     ██████╔╝██║   ██║ ╚███╔╝              ║
║      ██║   ██║   ██║██║   ██║██║     ██╔══██╗██║   ██║ ██╔██╗              ║
║      ██║   ╚██████╔╝╚██████╔╝███████╗██████╔╝╚██████╔╝██╔╝ ██╗             ║
║      ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝             ║
║                                                                            ║
║              Professional Cybersecurity Command Assistant                  ║
║                          Version 2.0 + AI                                  ║
╚════════════════════════════════════════════════════════════════════════════╝

[*] Over 100+ Security Tools at Your Fingertips
[*] AI-Powered Natural Language Commands (NEW!)
[*] Command History | Favorites | Workflows | Templates
[*] Custom Commands | Enhanced Wordlists | Multi-Target Support
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

### AI Setup (Optional but Recommended!)

```bash
# 1. Get FREE Groq API key
# Visit: https://console.groq.com/
# Sign up (no credit card needed)
# Create API key

# 2. Configure AI in toolbox
toolbox
toolbox> ai-config
# Paste your API key when prompted
# Select model (recommended: llama-3.1-8b-instant)

# 3. Test AI features
toolbox> ai-status
toolbox> ai scan 192.168.1.1
```

**For detailed AI setup, see [AI_SETUP.md](AI_SETUP.md)**

### Basic Usage

```bash
# Interactive mode
toolbox

# AI-powered commands
toolbox> ai scan example.com
toolbox> ai find subdomains of example.com

# Traditional mode
toolbox directorybrutforce
toolbox subdomain

# Get detailed help for a tool
toolbox -c nmap --help

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

### 🆕 NEW in v2.0 + AI

- **🤖 AI-Powered Commands** - Natural language to security commands
- **🎨 Custom Commands** - Add your own frequently-used commands
- **🧠 Context-Aware AI** - Remembers targets and tools across commands
- **📝 Enhanced Wordlists** - Dynamic SecLists scanning (20+ wordlists)
- **🔍 Wordlist Scanner** - See all available wordlists on your system
- **✏️ Inline Editing** - Edit AI-generated or traditional commands
- **🛡️ Safety Validation** - Prevents dangerous command execution

### 🎨 Advanced Features

- **Workflow Automation** - Chain multiple commands into workflows
- **Command Templates** - Save and reuse command patterns with variables
- **Output Management** - Save scan results with custom filenames
- **Configuration System** - Customize behavior with JSON config
- **Tool Availability Checker** - See what's installed on your system
- **REST API Interface** - Optional Flask API for automation

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

### 📂 Directory Discovery
- Gobuster, Dirb, FFuf
- Feroxbuster, Wfuzz

### 🔓 Password Cracking
- Hydra, John the Ripper
- Hashcat, Medusa

### 🕵️ OSINT & Enumeration
- TheHarvester, Subfinder
- Amass, Sublist3r, HTTPx

### 🛠 Exploitation
- Metasploit, SearchSploit
- Msfvenom, Weevely

### 🔐 Privilege Escalation
- LinPEAS, WinPEAS
- PSPY, Linux Smart Enumeration

### 🔬 Forensics & Analysis
- Volatility, Autopsy
- Foremost, Binwalk, Ghidra

### 🎯 Reverse Engineering
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

### Example 1: AI-Powered Scan

```bash
$ toolbox

toolbox> ai scan example.com for vulnerabilities
[AI] 🤖 Generating command...
[AI] ✓ Generated: nmap -sV -sC example.com
Execute? (y/n/e=edit): y
```

### Example 2: Add Custom Command

```bash
toolbox> add-custom

Command name: my-quick-scan
Command: nmap -p- -T4 -sV -sC -A {target}
Description: My fast comprehensive scan

[+] Custom command 'my-quick-scan' added successfully!

# Now use it
toolbox> use my-quick-scan
Enter target: example.com
```

### Example 3: Edit Command Before Running

```bash
Command: nmap -p- -T4 192.168.1.100
Execute? (y/n/e=edit): e

Command: nmap -p 80,443,8080 -T4 192.168.1.100  # Edited!
Execute edited command? (y/n): y
```

### Example 4: Multi-Target Scanning

```bash
Enter targets: 192.168.1.1,192.168.1.2,192.168.1.3
[+] Multi-target mode: 3 targets
# Executes on each target sequentially
```

### Example 5: Scan Available Wordlists

```bash
toolbox> scan-wordlists

[+] Directory Wordlists (7 found):
  ✓ common.txt
    Path: /usr/share/seclists/Discovery/Web-Content/common.txt
    Size: 4.7 KB | Lines: 4,614

[+] Total wordlists found: 24
```

---

## 🤖 AI Commands Reference

| Command | Description |
|---------|-------------|
| `ai <request>` | Generate command from natural language |
| `ai-status` | Check if AI is ready and running |
| `ai-config` | Configure AI model settings |
| `ai-context` | Show current conversation context |
| `ai-clear` | Clear conversation context |
| `ai-help` | Show AI setup instructions |

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

User data stored in `~/.toolbox/`:
- `history.json` - Command history
- `favorites.json` - Favorite commands
- `templates.json` - Command templates
- `workflows.json` - Saved workflows
- `custom_commands.json` - Your custom commands (NEW!)
- `ai_config.json` - AI configuration (NEW!)

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

- [README.md](README.md) - This file
- [AI_SETUP.md](AI_SETUP.md) - AI features setup guide
- [AI_EXAMPLES.md](AI_EXAMPLES.md) - AI usage examples
- [CUSTOM_COMMANDS.md](CUSTOM_COMMANDS.md) - Custom commands guide
- [INSTALLATION.md](INSTALLATION.md) - Installation guide
- [FEATURES_GUIDE.md](FEATURES_GUIDE.md) - Complete features guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing guide

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
- AI powered by [Groq](https://groq.com) - Fast, free AI inference
- Wordlists from [SecLists](https://github.com/danielmiessler/SecLists)

---

## 🎯 Roadmap

- [x] AI-powered natural language commands
- [x] Custom commands system
- [x] Enhanced SecLists integration
- [x] Context-aware AI conversations
- [ ] Add more tools (200+ goal)
- [ ] GUI interface (optional)
- [ ] Plugin system
- [ ] Tool version checking
- [ ] Custom wordlist manager
- [ ] Scan result parser
- [ ] Report generation
- [ ] Team collaboration features

---

## 🔥 Why Toolbox is Different

| Feature | Toolbox v2.0 + AI | Manual Commands | Other Tools |
|---------|-------------------|-----------------|-------------|
| 100+ Tools | ✅ | ❌ | ⚠️ Some |
| AI-Powered | ✅ NEW! | ❌ | ❌ |
| Custom Commands | ✅ NEW! | ❌ | ❌ |
| Command History | ✅ | ❌ | ⚠️ Limited |
| Edit Before Run | ✅ | ❌ | ❌ |
| Multi-Target | ✅ | ❌ | ⚠️ Some |
| Workflows | ✅ | ❌ | ❌ |
| Auto-Install | ✅ | ❌ | ❌ |
| Hollywood Mode | ✅ | ❌ | ❌ |
| Free & Open Source | ✅ | ✅ | ⚠️ Some |

---

## 💻 System Requirements

### Base Requirements
- **OS**: Kali Linux (recommended), Parrot OS, Ubuntu, Debian
- **Python**: 3.6 or higher
- **Storage**: ~1 MB (base toolbox)
- **Internet**: Required for installing tools

### For AI Features (Optional)
- **Groq API Key**: Free cloud AI (get at https://console.groq.com/)
- **Internet Connection**: Required for AI command generation
- **Storage**: None (cloud-based AI)
- **RAM**: No additional requirements (runs in cloud)

---

## 🚀 Quick Commands Cheat Sheet

```bash
# Traditional Commands
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

# NEW: AI Commands
toolbox> ai scan example.com                    # AI command generation
toolbox> ai find subdomains of example.com      # Natural language
toolbox> ai-status                              # Check AI readiness
toolbox> ai-config                              # Configure AI model

# NEW: Custom Commands
toolbox> add-custom              # Add your own command
toolbox> list-custom             # List custom commands
toolbox> use my-custom-scan      # Use custom command

# NEW: Wordlist Commands
toolbox> scan-wordlists          # Scan all available wordlists

# Fun Commands
toolbox hollywood                # Hollywood hacker mode!
```

---

## 📞 Contact & Support

### Get Help
- **GitHub Issues**: [Report bugs or request features](https://github.com/IstiukAhmedMitul/toolbox/issues)
- **Documentation**: Check the [docs](https://github.com/IstiukAhmedMitul/toolbox)
- **Discussions**: Share your experience and ask questions

### Connect with the Developer

**Md. Istiuk Ahmed Mitul**

[![Email](https://img.shields.io/badge/Email-istiukahmedmitul@gmail.com-red?style=for-the-badge&logo=gmail)](mailto:istiukahmedmitul@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Md%20Istiuk%20Ahmed%20Mitul-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/md-istiuk-ahmed-mitul-4b800033b)
[![GitHub](https://img.shields.io/badge/GitHub-IstiukAhmedMitul-black?style=for-the-badge&logo=github)](https://github.com/IstiukAhmedMitul)



---

<div align="center">

### Made with ❤️ for the Cybersecurity Community

**[⭐ Star](https://github.com/IstiukAhmedMitul/toolbox)** • **[🐛 Report Bug](https://github.com/IstiukAhmedMitul/toolbox/issues)** • **[✨ Request Feature](https://github.com/IstiukAhmedMitul/toolbox/issues)**

---

**Hack Responsibly. Always Get Permission. Stay Legal.** 🛡️

</div>

