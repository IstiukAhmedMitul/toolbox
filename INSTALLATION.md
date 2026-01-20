# Complete Installation Guide for Kali Linux

## 📋 Overview
This guide will help you install Toolbox on your Kali Linux system and upload it to GitHub to make it available for everyone.

---

## Part 1: Transfer Files from Windows to Kali Linux

### Method 1: Using USB Drive (Easiest)
1. **On Windows:**
   - Insert USB drive
   - Copy the entire `project` folder from `c:\Users\ISTIUK\Desktop\project\` to your USB drive
   - Safely eject USB

2. **On Kali Linux:**
   ```bash
   # Insert USB drive and mount it (usually auto-mounts)
   # Copy files to your home directory
   cp -r /media/[your-usb-name]/project ~/toolbox-project
   cd ~/toolbox-project
   ```

### Method 2: Using Shared Folder (VMware/VirtualBox)
1. **If using VMware:**
   ```bash
   # On Kali Linux
   sudo apt update
   sudo apt install open-vm-tools
   # Copy from shared folder
   cp -r /mnt/hgfs/project ~/toolbox-project
   ```

2. **If using VirtualBox:**
   ```bash
   # On Kali Linux
   sudo apt install virtualbox-guest-utils
   # Create shared folder in VirtualBox settings first
   cp -r /media/sf_project ~/toolbox-project
   ```

### Method 3: Using SCP/SFTP (If SSH enabled)
```bash
# On Kali Linux, enable SSH first
sudo systemctl start ssh

# On Windows, use WinSCP or command:
# scp -r "c:\Users\ISTIUK\Desktop\project" user@kali-ip:~/toolbox-project
```

### Method 4: Using Git (Recommended after GitHub upload)
```bash
# After you upload to GitHub (see Part 3)
git clone https://github.com/YOUR-USERNAME/toolbox.git
cd toolbox
```

---

## Part 2: Install Toolbox on Kali Linux

### Step 1: Verify Files Are Copied
```bash
cd ~/toolbox-project
ls -la
```

You should see:
- `toolbox.py`
- `toolbox_api.py` (optional)
- `install.sh`
- `README.md`
- Other documentation files

### Step 2: Make Install Script Executable
```bash
chmod +x install.sh
```

### Step 3: Run Automated Installation
```bash
sudo ./install.sh
```

The script will:
- ✅ Check Python version
- ✅ Install toolbox globally
- ✅ Offer to install security tools
- ✅ Offer to download SecLists wordlists
- ✅ Offer to install Python packages

**Answer prompts as needed:**
- Do you want to install common security tools? (y/n) → `y` (recommended)
- Do you want to download SecLists wordlists? (y/n) → `y` (recommended, ~1GB)
- Do you want to install optional Python packages? (y/n) → `y` (if you plan to use pwntools)

### Step 4: Verify Installation
```bash
# Test basic command
toolbox --help

# Check version
toolbox --list

# Test a tool
toolbox nmap

# Test category search
toolbox directorybrutforce

# Check what tools are installed
toolbox --doctor
```

### Step 5: Test Interactive Mode
```bash
toolbox
```

Commands to try:
- `help` - Show available commands
- `use nmap` - Interact with nmap
- `search subdomain` - Search for subdomain tools
- `history` - View command history
- `favorites` - View favorite commands
- `q` - Quit

---

## Part 3: Manual Installation (Alternative Method)

If the automated script doesn't work, install manually:

### Step 1: Copy Main File
```bash
cd ~/toolbox-project
sudo cp toolbox.py /usr/local/bin/toolbox
sudo chmod +x /usr/local/bin/toolbox
```

### Step 2: Add Python Shebang
```bash
sudo sed -i '1i#!/usr/bin/env python3' /usr/local/bin/toolbox
```

### Step 3: Test Installation
```bash
toolbox --help
```

### Step 4: Install Optional Dependencies
```bash
# For API server (optional)
pip3 install flask flask-cors

# For advanced exploitation (optional)
pip3 install pwntools

# For Python development
sudo apt update
sudo apt install python3-pip
```

---

## Part 4: Install Security Tools (Optional)

Many of these tools come pre-installed on Kali Linux, but you can ensure they're available:

```bash
sudo apt update
sudo apt install -y \
    nmap nikto gobuster dirb sqlmap hydra \
    john hashcat metasploit-framework \
    wpscan enum4linux smbmap crackmapexec \
    ffuf feroxbuster medusa aircrack-ng \
    openvas sslscan dnsrecon dnsenum \
    theharvester binwalk steghide exiftool \
    radare2 gdb ltrace strace ghidra \
    volatility3 foremost scalpel bulk-extractor \
    sublist3r amass httpx waybackurls
```

### Install Additional Tools
```bash
# Linpeas & WinPEAS (Privilege Escalation)
cd /opt
sudo git clone https://github.com/carlospolop/PEASS-ng.git

# Subfinder
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Download SecLists (Wordlists)
sudo apt install seclists
# Or manually:
sudo git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists
```

---

## Part 5: Upload to GitHub

### Step 1: Create GitHub Account
1. Go to https://github.com
2. Sign up for free account
3. Verify email address

### Step 2: Create New Repository
1. Click the **+** icon (top right) → **New repository**
2. **Repository name:** `toolbox` or `cybersecurity-toolbox`
3. **Description:** "Professional Cybersecurity CLI Tool - Command Assistant for Penetration Testing & CTF"
4. **Public** (so everyone can use it)
5. **DO NOT** initialize with README (we have our own)
6. Click **Create repository**

### Step 3: Initialize Git on Kali Linux
```bash
cd ~/toolbox-project

# Configure git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize repository
git init

# Create .gitignore file
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# User data
.toolbox/
outputs/
*.log

# Testing
test_*
*.tmp
EOF

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Toolbox v2.0 - Professional Cybersecurity CLI Tool"
```

### Step 4: Link to GitHub Repository
```bash
# Replace YOUR-USERNAME with your GitHub username
git remote add origin https://github.com/YOUR-USERNAME/toolbox.git

# Verify remote
git remote -v
```

### Step 5: Push to GitHub
```bash
# Push to GitHub (first time)
git branch -M main
git push -u origin main
```

**You'll be prompted for credentials:**
- Username: Your GitHub username
- Password: Use **Personal Access Token** (not your password)

### Step 6: Create Personal Access Token (If needed)
1. Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click **Generate new token (classic)**
3. Name: "Toolbox Upload"
4. Select scopes: **repo** (all checkboxes)
5. Click **Generate token**
6. **Copy the token** (you won't see it again!)
7. Use this token as password when pushing

### Step 7: Verify Upload
1. Go to https://github.com/YOUR-USERNAME/toolbox
2. Refresh page
3. You should see all your files!

---

## Part 6: Make It Professional on GitHub

### Step 1: Add Topics/Tags
1. On your repository page, click **⚙️ (gear icon)** next to "About"
2. Add topics:
   - `penetration-testing`
   - `cybersecurity`
   - `kali-linux`
   - `security-tools`
   - `ctf`
   - `command-line`
   - `python`
   - `hacking-tools`
3. Click **Save changes**

### Step 2: Update README (Optional Enhancement)
Add a badge to the top of your README:

```bash
# Edit README_v2.md and add at the top:
cat > badge_section.txt << 'EOF'
# Toolbox v2.0

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![Platform](https://img.shields.io/badge/platform-Kali%20Linux-red)
![License](https://img.shields.io/badge/license-MIT-green)
![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen)

EOF
```

### Step 3: Add a LICENSE File
```bash
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR DEALINGS IN THE
SOFTWARE.
EOF

# Commit and push
git add LICENSE
git commit -m "Add MIT License"
git push
```

### Step 4: Create Release (Optional)
1. Go to your repository on GitHub
2. Click **Releases** → **Create a new release**
3. Tag version: `v2.0.0`
4. Release title: "Toolbox v2.0 - Professional Release"
5. Description:
   ```
   First official release of Toolbox - Professional Cybersecurity CLI Tool
   
   Features:
   - 100+ security tools with intelligent command suggestions
   - Command history and favorites
   - Workflow automation
   - Smart templates
   - Multi-target support
   - Output management
   - REST API interface
   - Tool availability checker
   
   Installation: See INSTALLATION.md
   ```
6. Click **Publish release**

---

## Part 7: Share With Everyone

### Installation Command for Others
Once uploaded to GitHub, anyone can install using:

```bash
# Method 1: Quick Install
curl -sSL https://raw.githubusercontent.com/YOUR-USERNAME/toolbox/main/install.sh | sudo bash

# Method 2: Manual Install
git clone https://github.com/YOUR-USERNAME/toolbox.git
cd toolbox
sudo ./install.sh

# Method 3: Direct Download
wget https://github.com/YOUR-USERNAME/toolbox/raw/main/toolbox.py -O /usr/local/bin/toolbox
sudo chmod +x /usr/local/bin/toolbox
```

### Share Your Repository
Share this link with everyone:
```
https://github.com/YOUR-USERNAME/toolbox
```

Post it on:
- Reddit: r/cybersecurity, r/netsec, r/hacking
- Twitter/X with hashtags: #cybersecurity #pentest #kalilinux #ctf
- Discord servers for cybersecurity
- Your blog or website

---

## Troubleshooting

### Issue: "Command not found: toolbox"
**Solution:**
```bash
# Check if file exists
ls -la /usr/local/bin/toolbox

# If not, reinstall
cd ~/toolbox-project
sudo ./install.sh

# Or add to PATH
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
source ~/.bashrc
```

### Issue: "Permission denied"
**Solution:**
```bash
sudo chmod +x /usr/local/bin/toolbox
```

### Issue: "Python module not found"
**Solution:**
```bash
pip3 install flask flask-cors pwntools
```

### Issue: Git push asks for password
**Solution:** Use Personal Access Token (see Part 5, Step 6)

### Issue: Tools not working
**Solution:**
```bash
# Check what's missing
toolbox --doctor

# Install missing tools
sudo apt install [tool-name]
```

---

## Quick Reference

### Daily Usage Commands
```bash
# Interactive mode
toolbox

# Search for tools
toolbox subdomain
toolbox directorybrutforce
toolbox password

# Get detailed help
toolbox -c nmap --help
toolbox -c sqlmap --help

# View history
toolbox --history

# Check installed tools
toolbox --doctor

# Show all tools
toolbox --list
```

### Update Toolbox (After Making Changes)
```bash
cd ~/toolbox-project
git add .
git commit -m "Description of changes"
git push
```

---

## 🎉 Congratulations!

You now have:
- ✅ Toolbox installed on Kali Linux
- ✅ All files uploaded to GitHub
- ✅ Tool available for everyone worldwide
- ✅ Professional repository with documentation

**Next Steps:**
1. Test all features: `toolbox --help`
2. Share your GitHub link with the community
3. Watch for issues/feedback on GitHub
4. Keep updating and improving!

---

## Support

If you encounter issues:
1. Check GitHub Issues: `https://github.com/YOUR-USERNAME/toolbox/issues`
2. Read FEATURES_GUIDE.md for examples
3. Run `toolbox --doctor` to diagnose problems
4. Check Kali Linux forums

**Happy Hacking! 🔒🛡️**
