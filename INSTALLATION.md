# 📦 Installation Guide

Complete installation instructions for Toolbox v2.0 + AI.

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Kali Linux 2020+ (or Debian-based distro)
- **Python**: 3.6 or higher
- **Disk Space**: 100 MB
- **RAM**: 1 GB
- **Internet**: Required for AI features

### Recommended
- **OS**: Kali Linux 2024+
- **Python**: 3.10+
- **RAM**: 2 GB+
- **Internet**: Stable connection

---

## 🚀 Quick Install (Recommended)

### Method 1: Automated Installer

```bash
# Clone repository
git clone https://github.com/IstiukAhmedMitul/toolbox.git
cd toolbox

# Run installer
chmod +x install.sh
./install.sh

# Toolbox is now installed!
toolbox
```

The installer automatically:
- ✅ Installs Python dependencies
- ✅ Makes toolbox executable
- ✅ Creates global command
- ✅ Sets up configuration directory

---

## 🔧 Manual Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/IstiukAhmedMitul/toolbox.git
cd toolbox
```

### Step 2: Install Dependencies

**On Kali Linux / Debian:**
```bash
# Try apt first (recommended for Python 3.13+)
sudo apt update
sudo apt install python3-requests

# Or use pip if apt fails
pip3 install requests
```

**Using pip:**
```bash
pip3 install requests
```

### Step 3: Make Executable

```bash
chmod +x toolbox.py
```

### Step 4: Install Globally (Optional)

```bash
sudo cp toolbox.py /usr/local/bin/toolbox
sudo chmod +x /usr/local/bin/toolbox
```

Now you can run `toolbox` from anywhere!

---

## 🤖 AI Setup (Optional)

### Get Groq API Key (FREE)

1. Visit https://console.groq.com/
2. Sign up (no credit card needed)
3. Create API key
4. Copy the key

### Configure in Toolbox

```bash
toolbox
toolbox> ai-config
# Paste your API key
# Select model (press 1)
```

**Detailed guide**: See [AI_SETUP.md](AI_SETUP.md)

---

## ✅ Verify Installation

```bash
# Run toolbox
toolbox

# You should see the banner:
╔════════════════════════════════════════════════════════════════════════════╗
║                            TOOLBOX v2.0 + AI                               ║
╚════════════════════════════════════════════════════════════════════════════╝

# Test basic commands
toolbox> help
toolbox> list nmap
toolbox> ai-status
```

---

## 🔧 Troubleshooting

### Issue: `toolbox: command not found`

**Solution 1** - Add to PATH:
```bash
sudo ln -s $(pwd)/toolbox.py /usr/local/bin/toolbox
```

**Solution 2** - Run directly:
```bash
cd ~/toolbox
python3 toolbox.py
```

### Issue: `ModuleNotFoundError: No module named 'requests'`

**Solution**:
```bash
# On Kali Linux 2024+
sudo apt install python3-requests

# Or use pip
pip3 install requests
```

### Issue: Permission denied

**Solution**:
```bash
chmod +x toolbox.py
chmod +x install.sh
```

### Issue: AI features not working

**Solution**: Configure Groq API key
```bash
toolbox> ai-config
# Enter your API key from https://console.groq.com/
```

---

## 📁 Directory Structure

After installation:

```
~/.toolbox/              # Configuration directory
├── config.json          # Main configuration
├── history.json         # Command history
├── favorites.json       # Saved favorites
├── custom_commands.json # Custom commands
├── ai_config.json       # AI configuration
└── outputs/             # Saved command outputs
```

---

## 🔄 Updating Toolbox

```bash
cd ~/toolbox
git pull
./install.sh  # Re-run installer if needed
```

---

## 🗑️ Uninstallation

```bash
# Remove global command
sudo rm /usr/local/bin/toolbox

# Remove configuration
rm -rf ~/.toolbox/

# Remove repository
rm -rf ~/toolbox/
```

---

## 🌐 Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| Kali Linux | ✅ Full Support | Recommended |
| Ubuntu | ✅ Supported | Install security tools manually |
| Debian | ✅ Supported | Install security tools manually |
| Arch Linux | ⚠️ Untested | Should work |
| macOS | ⚠️ Untested | Security tools may differ |
| Windows (WSL) | ⚠️ Untested | Use WSL2 with Kali |

---

## 📚 Next Steps

1. ✅ Complete installation
2. ✅ Run `toolbox` and explore
3. ✅ Configure AI features ([AI_SETUP.md](AI_SETUP.md))
4. ✅ Read quick reference ([QUICK_REFERENCE.md](QUICK_REFERENCE.md))
5. ✅ Try AI examples ([AI_EXAMPLES.md](AI_EXAMPLES.md))
6. ✅ Create custom commands ([CUSTOM_COMMANDS.md](CUSTOM_COMMANDS.md))

---

## 💬 Support

- **GitHub Issues**: https://github.com/IstiukAhmedMitul/toolbox/issues
- **Email**: istiukahmedmitul@gmail.com
- **LinkedIn**: [Md. Istiuk Ahmed Mitul](https://www.linkedin.com/in/md-istiuk-ahmed-mitul-4b800033b)

---

**Installation complete! Happy hacking! 🚀**
