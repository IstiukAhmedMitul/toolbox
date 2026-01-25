# Kali Linux Installation Guide for Toolbox

This guide will walk you through installing and configuring Toolbox on your Kali Linux system.

## Prerequisites

- Kali Linux (any recent version)
- Python 3.6 or higher (pre-installed on Kali)
- Basic terminal knowledge

## Step-by-Step Installation

### 1. Download the Tool

First, download or transfer the `toolbox.py` file to your Kali system.

```bash
# If downloading from GitHub
cd ~
git clone https://github.com/YOUR_USERNAME/toolbox.git
cd toolbox

# OR if you have the file already
cd /path/to/toolbox
```

### 2. Make the Script Executable

```bash
chmod +x toolbox.py
```

### 3. Test the Script

```bash
# Test if it runs correctly
./toolbox.py --help
```

You should see the help message if everything is working.

### 4. Install Globally (Recommended)

There are three methods to install globally:

#### Method A: Symbolic Link (Best for Development)

```bash
# Create a symbolic link
sudo ln -s $(pwd)/toolbox.py /usr/local/bin/toolbox

# Test it
toolbox --help
```

**Advantages:**
- Easy to update (just edit the original file)
- Changes reflect immediately
- Easy to uninstall

**To uninstall:**
```bash
sudo rm /usr/local/bin/toolbox
```

#### Method B: Copy to System Path

```bash
# Copy the script
sudo cp toolbox.py /usr/local/bin/toolbox

# Make it executable
sudo chmod +x /usr/local/bin/toolbox

# Test it
toolbox --help
```

**Advantages:**
- More permanent
- Doesn't depend on original location

**To update:**
```bash
sudo cp toolbox.py /usr/local/bin/toolbox
```

**To uninstall:**
```bash
sudo rm /usr/local/bin/toolbox
```

#### Method C: Add to PATH

```bash
# Add to your .bashrc or .zshrc
echo "export PATH=\"\$PATH:$HOME/toolbox\"" >> ~/.bashrc

# Create alias for convenience
echo "alias toolbox='python3 $HOME/toolbox/toolbox.py'" >> ~/.bashrc

# Reload configuration
source ~/.bashrc

# Test it
toolbox --help
```

### 5. Verify Installation

```bash
# Check if toolbox is accessible
which toolbox

# Should output: /usr/local/bin/toolbox

# Test interactive mode
toolbox
```

## Installing Required Tools

Toolbox is a command assistant and doesn't include the actual security tools. You need to install them separately.

### Essential Tools (Recommended)

```bash
# Update package lists
sudo apt update

# Install essential reconnaissance tools
sudo apt install -y nmap rustscan masscan whois dnsutils

# Install web testing tools
sudo apt install -y nikto wpscan sqlmap nuclei

# Install directory busters
sudo apt install -y gobuster dirb ffuf feroxbuster

# Install password tools
sudo apt install -y hydra john hashcat

# Install crypto tools
sudo apt install -y openssl steghide exiftool

# Install reverse engineering tools
sudo apt install -y binwalk radare2 gdb ltrace strace

# Install network tools
sudo apt install -y netcat-traditional curl wget

# Install enumeration tools
sudo apt install -y enum4linux smbmap crackmapexec

# Install OSINT tools
sudo apt install -y theharvester

# Install privilege escalation scripts
cd /opt
sudo git clone https://github.com/carlospolop/PEASS-ng.git
sudo git clone https://github.com/rebootuser/LinEnum.git
```

### Additional Tools (Optional but Recommended)

```bash
# Install Go-based tools (requires Go)
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/tomnomnom/waybackurls@latest
go install -v github.com/lc/gau/v2/cmd/gau@latest
go install -v github.com/tomnomnom/assetfinder@latest
go install -v github.com/OWASP/Amass/v3/...@master

# Install Python-based tools
pip3 install pwntools ropper
sudo apt install -y python3-pwntools

# Install forensics tools
sudo apt install -y volatility autopsy foremost scalpel bulk-extractor

# Install Burp Suite (if not already installed)
# Download from: https://portswigger.net/burp/communitydownload

# Install additional tools
sudo apt install -y zaproxy commix sublist3r
```

### Setting Up Wordlists

```bash
# Download SecLists (comprehensive wordlist collection)
cd /opt
sudo git clone https://github.com/danielmiessler/SecLists.git
sudo ln -s /opt/SecLists /usr/share/seclists

# Extract rockyou.txt if not already done
sudo gunzip /usr/share/wordlists/rockyou.txt.gz 2>/dev/null || true

# Verify wordlists
ls -la /usr/share/wordlists/
ls -la /usr/share/seclists/
```

## Configuration

### Setting up Shell Aliases (Optional)

Add useful aliases to your `.bashrc` or `.zshrc`:

```bash
cat >> ~/.bashrc << 'EOF'

# Toolbox aliases
alias tb='toolbox'
alias tb-nmap='toolbox --tool nmap'
alias tb-gobuster='toolbox --tool gobuster'
alias tb-search='toolbox --search'

EOF

source ~/.bashrc
```

### Setting up Auto-completion (Advanced)

Create a bash completion script:

```bash
sudo nano /etc/bash_completion.d/toolbox
```

Add the following:

```bash
_toolbox() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="--help --list --search --tool"

    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
}

complete -F _toolbox toolbox
```

Reload bash completion:

```bash
source /etc/bash_completion.d/toolbox
```

## Usage Examples

### Quick Start

```bash
# Launch interactive mode
toolbox

# List all available tools
toolbox --list

# Search for specific tools
toolbox --search "web"

# Directly use a tool
toolbox --tool nmap
```

### Common Workflows

#### Reconnaissance Workflow
```bash
toolbox
> use nmap
# Follow prompts...

> use gobuster
# Follow prompts...

> use nikto
# Follow prompts...
```

#### Password Cracking Workflow
```bash
toolbox
> use hashcat
# Select appropriate command...

> use john
# Follow prompts...
```

## Troubleshooting

### Issue: "Command not found"

**Solution 1:** Check if toolbox is in PATH
```bash
which toolbox
echo $PATH
```

**Solution 2:** Use full path
```bash
/usr/local/bin/toolbox
```

**Solution 3:** Reinstall
```bash
sudo ln -sf $(pwd)/toolbox.py /usr/local/bin/toolbox
```

### Issue: "Permission denied"

**Solution:**
```bash
chmod +x toolbox.py
sudo chmod +x /usr/local/bin/toolbox
```

### Issue: "Tool X not found"

**Solution:** Install the specific tool
```bash
sudo apt update
sudo apt install <tool-name>
```

### Issue: "Python3 not found"

**Solution:** Install Python 3 (shouldn't be needed on Kali)
```bash
sudo apt install python3
```

### Issue: Wordlist not found

**Solution:** Download and setup wordlists
```bash
cd /opt
sudo git clone https://github.com/danielmiessler/SecLists.git
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
```

## Updating Toolbox

If you used the symbolic link method:
```bash
cd /path/to/toolbox
git pull origin main  # If using Git
# Or edit toolbox.py directly
```

If you copied the file:
```bash
sudo cp toolbox.py /usr/local/bin/toolbox
sudo chmod +x /usr/local/bin/toolbox
```

## Uninstalling

To remove Toolbox:

```bash
# Remove the binary/link
sudo rm /usr/local/bin/toolbox

# Remove aliases (edit ~/.bashrc manually)
nano ~/.bashrc
# Remove toolbox-related lines

# Remove bash completion (if configured)
sudo rm /etc/bash_completion.d/toolbox
```

## Next Steps

1. ✅ Install Toolbox
2. ✅ Install your most-used security tools
3. ✅ Download wordlists
4. ✅ Practice using the interactive mode
5. ✅ Customize by adding your own tools

## Support

If you encounter any issues:
1. Check the README.md file
2. Review this installation guide
3. Create an issue on GitHub
4. Check if all dependencies are installed

---

**Happy Testing! 🔐**
