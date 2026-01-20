#!/bin/bash
# Toolbox Installation Script for Kali Linux
# This script automates the installation of Toolbox and essential security tools

set -e  # Exit on error

echo "=========================================="
echo "  Toolbox Installation Script"
echo "  For Kali Linux"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[i]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    print_error "Please do not run this script as root"
    exit 1
fi

# Step 1: Check Python installation
print_info "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION is installed"
else
    print_error "Python3 is not installed"
    print_info "Installing Python3..."
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

# Step 2: Make toolbox executable
print_info "Making toolbox.py executable..."
chmod +x toolbox.py
print_success "toolbox.py is now executable"

# Step 3: Install toolbox globally
print_info "Installing Toolbox globally..."
if [ -f "/usr/local/bin/toolbox" ]; then
    print_info "Removing existing installation..."
    sudo rm /usr/local/bin/toolbox
fi

CURRENT_DIR=$(pwd)
sudo ln -s "$CURRENT_DIR/toolbox.py" /usr/local/bin/toolbox
print_success "Toolbox installed to /usr/local/bin/toolbox"

# Step 4: Test installation
print_info "Testing installation..."
if command -v toolbox &> /dev/null; then
    print_success "Toolbox is accessible from PATH"
else
    print_error "Toolbox is not accessible from PATH"
    exit 1
fi

# Step 5: Offer to install essential tools
echo ""
read -p "Do you want to install essential security tools? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Updating package lists..."
    sudo apt update
    
    print_info "Installing essential reconnaissance tools..."
    sudo apt install -y nmap rustscan masscan whois dnsutils 2>/dev/null || true
    
    print_info "Installing web testing tools..."
    sudo apt install -y nikto wpscan sqlmap nuclei 2>/dev/null || true
    
    print_info "Installing directory busters..."
    sudo apt install -y gobuster dirb ffuf feroxbuster 2>/dev/null || true
    
    print_info "Installing password tools..."
    sudo apt install -y hydra john hashcat 2>/dev/null || true
    
    print_info "Installing crypto tools..."
    sudo apt install -y openssl steghide exiftool 2>/dev/null || true
    
    print_info "Installing reverse engineering tools..."
    sudo apt install -y binwalk radare2 gdb ltrace strace 2>/dev/null || true
    
    print_info "Installing network tools..."
    sudo apt install -y netcat-traditional curl wget 2>/dev/null || true
    
    print_info "Installing enumeration tools..."
    sudo apt install -y enum4linux smbmap crackmapexec 2>/dev/null || true
    
    print_success "Essential tools installation complete!"
fi

# Step 6: Offer to download wordlists
echo ""
read -p "Do you want to setup wordlists (SecLists)? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -d "/opt/SecLists" ]; then
        print_info "SecLists already exists at /opt/SecLists"
    else
        print_info "Downloading SecLists (this may take a while)..."
        sudo git clone https://github.com/danielmiessler/SecLists.git /opt/SecLists
        print_success "SecLists downloaded to /opt/SecLists"
    fi
    
    # Extract rockyou if needed
    if [ -f "/usr/share/wordlists/rockyou.txt.gz" ]; then
        print_info "Extracting rockyou.txt..."
        sudo gunzip /usr/share/wordlists/rockyou.txt.gz 2>/dev/null || print_info "rockyou.txt already extracted"
    fi
    
    print_success "Wordlists setup complete!"
fi

# Step 7: Offer to install Python tools
echo ""
read -p "Do you want to install Python-based tools (pwntools, etc.)? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Installing Python tools..."
    pip3 install --user pwntools 2>/dev/null || true
    print_success "Python tools installation complete!"
fi

# Step 8: Add aliases (optional)
echo ""
read -p "Do you want to add convenient aliases to ~/.bashrc? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if ! grep -q "# Toolbox aliases" ~/.bashrc; then
        cat >> ~/.bashrc << 'EOF'

# Toolbox aliases
alias tb='toolbox'
alias tb-list='toolbox --list'
alias tb-search='toolbox --search'
EOF
        source ~/.bashrc
        print_success "Aliases added to ~/.bashrc"
        print_info "Available aliases: tb, tb-list, tb-search"
        print_info "Run 'source ~/.bashrc' to activate them"
    else
        print_info "Aliases already exist in ~/.bashrc"
    fi
fi

# Final summary
echo ""
echo "=========================================="
echo "  Installation Complete!"
echo "=========================================="
echo ""
print_success "Toolbox is ready to use!"
echo ""
echo "Quick Start:"
echo "  toolbox              - Launch interactive mode"
echo "  toolbox --help       - Show help"
echo "  toolbox --list       - List all tools"
echo "  toolbox --tool nmap  - Use specific tool"
echo ""
echo "Documentation:"
echo "  README.md           - Full documentation"
echo "  INSTALLATION.md     - Installation guide"
echo "  QUICK_REFERENCE.md  - Quick reference card"
echo "  GITHUB_SETUP.md     - GitHub setup guide"
echo ""
print_info "Happy hacking! 🎩💻"
echo ""
