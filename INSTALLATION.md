# 🚀 Installation Guide

> Quick and easy installation guide for Toolbox - Your Professional Cybersecurity CLI Assistant

---

## 📋 Requirements

- **Operating System**: Kali Linux (recommended), Parrot OS, Ubuntu, or Debian
- **Python**: 3.6 or higher (pre-installed on Kali Linux)
- **Internet Connection**: For downloading tools
- **Sudo Access**: For installing system-wide

---

## 🎯 Quick Installation (Recommended)

### Step 1: Clone the Repository

```bash
cd ~/Desktop
git clone https://github.com/IstiukAhmedMitul/toolbox.git
cd toolbox
```

### Step 2: Run the Installer

```bash
chmod +x install.sh
sudo ./install.sh
```

The installer will:
- ✅ Check Python version
- ✅ Install Toolbox globally
- ✅ Offer to install common security tools
- ✅ Offer to download SecLists wordlists (~1GB)
- ✅ Set up configuration

**Answer the prompts:**
- Install security tools? → `y` (recommended)
- Download SecLists? → `y` (recommended for beginners)
- Install Python packages? → `y` (if you want pwntools support)

### Step 3: Verify Installation

```bash
toolbox --help
```

You should see the help menu. Installation complete! 🎉

---

## 🔧 Manual Installation

If the automated installer doesn't work, follow these steps:

### Step 1: Clone the Repository

```bash
cd ~/Desktop
git clone https://github.com/IstiukAhmedMitul/toolbox.git
cd toolbox
```

### Step 2: Install Toolbox

```bash
sudo cp toolbox.py /usr/local/bin/toolbox
sudo chmod +x /usr/local/bin/toolbox
```

### Step 3: Verify Installation

```bash
toolbox --help
```

---

## 🎨 First Run

Launch Toolbox in interactive mode:

```bash
toolbox
```

You'll see the **professional Metasploit-style banner**:

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ████████╗ ██████╗  ██████╗ ██╗     ██████╗  ██████╗ ██╗  ██╗          ║
║   ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔══██╗██╔═══██╗╚██╗██╔╝          ║
║      ██║   ██║   ██║██║   ██║██║     ██████╔╝██║   ██║ ╚███╔╝           ║
║      ██║   ██║   ██║██║   ██║██║     ██╔══██╗██║   ██║ ██╔██╗           ║
║      ██║   ╚██████╔╝╚██████╔╝███████╗██████╔╝╚██████╔╝██╔╝ ██╗          ║
║      ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝          ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

[*] Over 100+ Security Tools at Your Fingertips
[*] 483 Pre-configured Commands Ready to Use
```

---

## 📚 Basic Usage

### View All Tools

```bash
toolbox --list
```

### Search by Category

```bash
toolbox directorybrutforce    # Directory brute-forcing tools
toolbox subdomain             # Subdomain enumeration
toolbox passwordcracking      # Password cracking tools
```

### Get Detailed Help for a Tool

```bash
toolbox -c nmap --help        # Shows all 35 nmap commands!
toolbox -c gobuster --help
toolbox -c sqlmap --help
```

### Use a Tool Interactively

```bash
toolbox --tool nmap
```

Then:
1. **Enter target**: `192.168.1.1` or `example.com`
2. **Select command**: Choose from 1-35
3. **Edit if needed**: Press `e` to modify the command
4. **Execute**: Press `y` to run
5. **Save output**: Press `s` to save with custom filename

### Interactive Mode

```bash
toolbox
```

Commands available:
- `help` - Show available commands
- `use [tool]` - Select a tool (e.g., `use nmap`)
- `search [keyword]` - Find tools (e.g., `search web`)
- `history` - View command history
- `favorites` - View saved favorites
- `q` or `exit` - Quit

---

## 🔍 Check Installed Tools

See what security tools you have installed:

```bash
toolbox --doctor
```

This shows:
- ✅ Tools that are installed
- ❌ Tools that are missing
- 📦 Installation commands for missing tools

---

## 🛠️ Installing Security Tools

### Option 1: Auto-Install (Easiest)

When you try to use a tool that's not installed, Toolbox will ask:

```
[!] Tool 'nmap' is not installed on your system
[?] Would you like to install it now? (y/n):
```

Type `y` and it will install automatically!

### Option 2: Install Common Tools Manually

```bash
sudo apt update
sudo apt install -y nmap nikto gobuster dirb sqlmap hydra john \
    metasploit-framework wpscan enum4linux crackmapexec ffuf \
    feroxbuster medusa aircrack-ng sslscan theharvester
```

### Option 3: Install All Recommended Tools

```bash
sudo apt update
sudo apt install -y \
    nmap rustscan masscan netdiscover \
    nikto wpscan sqlmap nuclei \
    gobuster dirb ffuf feroxbuster wfuzz \
    hydra medusa john hashcat \
    metasploit-framework msfvenom \
    enum4linux smbclient smbmap crackmapexec \
    aircrack-ng wifite reaver bully \
    theharvester sublist3r amass subfinder httpx \
    binwalk steghide exiftool foremost \
    radare2 gdb ltrace strace \
    hashid hash-identifier openssl
```

---

## 📖 Download Wordlists (Recommended)

Essential for password cracking and directory brute-forcing:

```bash
sudo apt install seclists
```

Or manually:

```bash
sudo git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists
```

Common wordlist locations:
- `/usr/share/wordlists/rockyou.txt`
- `/usr/share/seclists/Discovery/Web-Content/`
- `/usr/share/seclists/Passwords/`

---

## 🎬 Fun Features

### Hollywood Hacker Mode

Just for fun! Look like you're in a movie:

```bash
toolbox cmatrix      # Matrix falling code effect
toolbox hollywood    # Full Hollywood hacker terminal
toolbox cowsay       # ASCII cow says things
toolbox figlet       # Big ASCII art text
toolbox lolcat       # Rainbow colored text
toolbox sl           # Steam locomotive animation
```

Install Hollywood tools:

```bash
sudo apt install cmatrix hollywood cowsay figlet lolcat sl -y
```

---

## 🔥 Pro Tips

### 1. Edit Commands Before Running

When selecting a command, press `e` to edit it:

```bash
Command: nmap -p- -T4 192.168.1.1
Execute? (y/n/e=edit): e

# Command appears with cursor - edit as needed!
Command: nmap -p- -T4 -A -sC -sV 192.168.1.1█
```

### 2. Multi-Target Scanning

Enter multiple targets separated by commas:

```bash
Enter target: 192.168.1.1,192.168.1.2,192.168.1.3
[+] Multi-target mode: 3 targets detected
```

### 3. Save Output with Custom Name

After running a command:

```bash
[?] Next action? (r=run another/s=save as/q=quit): s
Save output as: my_scan_results.txt
[+] Output saved to: my_scan_results.txt
```

### 4. Continuous Session Mode

After executing a command, you don't exit automatically:
- `r` - Run another command
- `s` - Save output with custom filename
- `q` - Quit

### 5. Clean Exit

Press `Ctrl+C` anywhere for a clean exit - no ugly errors!

---

## ⚙️ Configuration

Configuration file: `~/.toolbox/config.json`

Default settings:

```json
{
  "default_wordlist": "/usr/share/wordlists/rockyou.txt",
  "output_auto_save": false,
  "show_banner": true,
  "history_limit": 1000
}
```

You can edit this file to customize behavior.

---

## 🐛 Troubleshooting

### "Command not found: toolbox"

**Solution 1**: Add to PATH
```bash
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
source ~/.bashrc
```

**Solution 2**: Reinstall
```bash
cd ~/Desktop/toolbox
sudo cp toolbox.py /usr/local/bin/toolbox
sudo chmod +x /usr/local/bin/toolbox
```

### "Permission denied"

Make sure it's executable:
```bash
sudo chmod +x /usr/local/bin/toolbox
```

### "Tool not found"

Check if the tool is installed:
```bash
which nmap        # Check if nmap is installed
toolbox --doctor  # Check all tools
```

Install missing tool:
```bash
sudo apt install nmap
```

### "Python version too old"

Check Python version:
```bash
python3 --version   # Should be 3.6 or higher
```

Update Python:
```bash
sudo apt update
sudo apt install python3
```

### Line Ending Issues (Windows users)

If you edited on Windows, fix line endings:
```bash
sudo apt install dos2unix
dos2unix toolbox.py
```

Or:
```bash
sed -i 's/\r$//' toolbox.py
```

---

## 🔄 Updating Toolbox

To get the latest version:

```bash
cd ~/Desktop/toolbox
git pull origin main
sudo cp toolbox.py /usr/local/bin/toolbox
sudo chmod +x /usr/local/bin/toolbox
```

---

## 📖 Advanced Usage

### Create Workflows

```bash
toolbox --create-workflow recon
# Add multiple commands to workflow
toolbox --run-workflow recon --target example.com
```

### Save as Template

```bash
toolbox --save-template scan_template
# Save command with variables like {target}, {port}
```

### Command History

```bash
toolbox --history              # View all history
toolbox --history --limit 10   # Last 10 commands
```

### Favorites

```bash
# Add to favorites when executing
Execute? (y/n/e=edit/f=favorites): f

# View favorites
toolbox --favorites
```

---

## 📊 What You Get

- **100 Security Tools** in the database
- **483 Pre-configured Commands** ready to use
- **35 Nmap Commands** including advanced combinations
- **9 Netdiscover Commands** for network discovery
- **Multiple Command Variations** for each tool
- **Categories**: Recon, Web Testing, Directory Discovery, Password Cracking, Exploitation, Privilege Escalation, Forensics, Reverse Engineering, Cryptography, Wireless, and more!

---

## 🆘 Getting Help

### In-Tool Help

```bash
toolbox --help                 # General help
toolbox -c [tool] --help      # Tool-specific help
toolbox                       # Interactive mode (type 'help')
```

### GitHub Issues

Found a bug? Have a suggestion?
- **Report Issues**: https://github.com/IstiukAhmedMitul/toolbox/issues
- **Discussions**: https://github.com/IstiukAhmedMitul/toolbox/discussions

### Documentation

- **README**: Full project overview
- **FEATURES_GUIDE**: Detailed features documentation
- **QUICK_REFERENCE**: Command cheat sheet

---

## 🤝 Contributing

Want to add tools or improve Toolbox?

1. Fork the repository
2. Add your tool to the database
3. Test thoroughly
4. Submit a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📜 License

This project is licensed under the MIT License - free and open source forever!

---

## ⭐ Show Your Support

If you find Toolbox useful:
- ⭐ **Star the repository**: https://github.com/IstiukAhmedMitul/toolbox
- 🐛 **Report bugs** to help improve
- 💡 **Suggest features** you'd like to see
- 🤝 **Contribute** new tools or improvements

---

## 🎯 Quick Start Checklist

- [ ] Clone repository: `git clone https://github.com/IstiukAhmedMitul/toolbox.git`
- [ ] Run installer: `sudo ./install.sh`
- [ ] Verify installation: `toolbox --help`
- [ ] Try interactive mode: `toolbox`
- [ ] Install security tools: `sudo apt install nmap gobuster sqlmap hydra`
- [ ] Download wordlists: `sudo apt install seclists`
- [ ] Check installed tools: `toolbox --doctor`
- [ ] Try your first scan: `toolbox --tool nmap`
- [ ] Have fun with Hollywood mode: `toolbox cmatrix`
- [ ] Star the repository: ⭐

---

<div align="center">

### Ready to Start? 🚀

```bash
git clone https://github.com/IstiukAhmedMitul/toolbox.git
cd toolbox
sudo ./install.sh
toolbox
```

**Happy Hacking! Stay Legal. Get Permission.** 🛡️

</div>
