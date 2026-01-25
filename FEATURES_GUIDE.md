# ✨ Features Guide

Complete overview of all Toolbox v2.0 + AI features.

## 🤖 AI-Powered Commands (NEW!)

### Natural Language to Commands
Simply describe what you want:

```bash
toolbox> ai scan 192.168.1.1 for vulnerabilities
toolbox> ai brute force SSH on target
toolbox> ai find subdomains of example.com
```

**Features:**
- 🗣️ Natural language understanding
- 🧠 Context awareness (remembers targets)
- ✏️ Edit before execution
- 💾 Save to favorites
- ⚡ Fast & FREE (Groq API)

[Learn more: AI_SETUP.md](AI_SETUP.md)

---

## 🛠️ Tool Database (100+ Tools)

### Categories

**Network Scanning:**
- nmap, masscan, netdiscover, arp-scan

**Web Testing:**
- gobuster, dirb, nikto, wfuzz, ffuf

**Vulnerability Scanning:**
- nessus, OpenVAS, sqlmap, w3af

**Password Attacks:**
- hydra, medusa, john, hashcat

**Wireless:**
- aircrack-ng, reaver, wash, wifite

**Exploitation:**
- metasploit, searchsploit, beef

**Enumeration:**
- enum4linux, smbmap, dnsenum

**And 70+ more!**

---

## 📋 Core Features

### 1. Interactive Mode
```bash
toolbox

toolbox> list nmap
toolbox> search scan
toolbox> use nmap
```

### 2. Command History
```bash
toolbox> history
# View all previously used commands

toolbox> use <number>
# Re-run command from history
```

### 3. Favorites System
```bash
# Add favorite
toolbox> add-favorite nmap

# List favorites
toolbox> list-favorites

# Use favorite
toolbox> quick-scan 192.168.1.1
```

### 4. Search & Discover
```bash
# Search by functionality
toolbox> search web

# List tools by category
toolbox> list gobuster

# Show tool details
toolbox> show nmap
```

---

## 🎨 Custom Commands (NEW!)

Create your own shortcuts:

```bash
# Add custom command
toolbox> add-custom
Name: portscan
Description: Quick port scan
Command: nmap -p- -T4 {target}

# Use it
toolbox> portscan 192.168.1.1
```

**Features:**
- Save frequently-used commands
- Use placeholders ({target}, {wordlist})
- Works with AI context
- Share with team

[Learn more: CUSTOM_COMMANDS.md](CUSTOM_COMMANDS.md)

---

## 📊 Output Management

### View Last Output
```bash
toolbox> ai scan 192.168.1.1
# ... scan runs ...

toolbox> view-output
# Display last command output again
```

### Save Output
```bash
toolbox> save-output
Filename: scan_results.txt
[+] Output saved!
```

### Clear Data
```bash
toolbox> clear-data
# Clears history, outputs (keeps favorites & custom commands)
```

---

## 🎯 Enhanced Wordlists

Auto-detects SecLists wordlists:

```bash
toolbox> scan-wordlists

Available Wordlists:
Common Passwords:
  - rockyou.txt (14.3M - 14344391 lines)
  - 10-million-password-list.txt (...)

Web Directories:
  - dirb/common.txt (...)
  - dirbuster/directory-list-2.3-medium.txt (...)
```

**Features:**
- Auto-detection from multiple paths
- Shows file size & line count
- Quick insertion into commands
- Categories: passwords, directories, usernames, DNS, fuzzing

---

## 🎬 Hollywood Mode

Look like a movie hacker:

```bash
toolbox> hollywood

# Launches cmatrix effect
# Press Ctrl+C to exit
```

Just for fun! 😎

---

## 🔧 Configuration

### View Config
```bash
toolbox> config
# Shows current configuration
```

### AI Configuration
```bash
toolbox> ai-config
# Set API key, change model
```

### Clear Screen
```bash
toolbox> clear
# Clears terminal, shows banner
```

---

## 💡 Smart Features

### 1. Auto-Install Prompts
Missing a tool? Toolbox asks to install it:
```bash
toolbox> use nikto
[!] nikto not found. Install? (y/n): y
```

### 2. Multi-Target Support
```bash
# Use {target} placeholder
nmap -sV {target}

# Toolbox prompts for IP/domain
Target IP/Domain: 192.168.1.1
```

### 3. Wordlist Selection
```bash
# Use {wordlist} placeholder
gobuster dir -u {target} -w {wordlist}

# Toolbox shows available wordlists
```

### 4. Real-Time Output
Commands stream output in real-time (no waiting for completion)

### 5. Edit Failed Commands
If a command fails:
```bash
[!] Command exited with code: 1

Edit and retry? (y/n/view): y
# Edit and try again
```

### 6. System Command Passthrough
Run any system command:
```bash
toolbox> ifconfig
toolbox> ls -la
toolbox> sudo apt update
```

---

## 📈 Statistics

- **100+ Security Tools** in database
- **20+ Wordlist Categories** auto-detected
- **Unlimited Custom Commands**
- **Unlimited Favorites**
- **Full Command History**
- **FREE AI** (Groq API - 14,400 requests/day)

---

## 🎨 User Interface

### Beautiful Banner
ASCII art banner with version info

### Color-Coded Output
- 🟢 Green: Success messages
- 🔴 Red: Error messages
- 🟡 Yellow: Warnings
- 🔵 Cyan: Information

### Progress Indicators
- [+] Success
- [!] Warning/Error
- [*] Information
- [?] Prompt

---

## 🔐 Security Features

### AI Safety Checks
Warns about dangerous commands:
```bash
toolbox> ai delete all files
[!] WARNING: This command may be dangerous!
```

### Sudo Detection
Notifies when commands need root:
```bash
[!] Note: This command may require root privileges (sudo)
```

### No Data Leakage
- AI config stored locally
- No automatic telemetry
- Privacy-focused design

---

## 🚀 Performance

- **Fast Startup**: <1 second
- **AI Response**: <2 seconds (Groq)
- **Tool Lookup**: Instant
- **History Search**: Instant
- **Memory Efficient**: ~50 MB RAM

---

## 📚 Quick Reference

| Feature | Command |
|---------|---------|
| Help | `help` |
| List tools | `list <tool>` |
| Search | `search <keyword>` |
| Use tool | `use <tool>` |
| History | `history` |
| Favorites | `list-favorites` |
| AI command | `ai <request>` |
| AI status | `ai-status` |
| Custom commands | `add-custom` |
| View output | `view-output` |
| Save output | `save-output` |
| Clear | `clear` |
| Exit | `exit` or Ctrl+C |

---

## 🎓 Learning Resources

- [Installation Guide](INSTALLATION.md)
- [AI Setup](AI_SETUP.md)
- [AI Examples](AI_EXAMPLES.md)
- [Custom Commands](CUSTOM_COMMANDS.md)
- [Quick Reference](QUICK_REFERENCE.md)

---

**Explore all features - Happy Hacking! 🛡️**
