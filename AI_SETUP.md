# 🤖 AI Features Guide - Natural Language Command Generation

## Overview

Toolbox v2.0 now includes **AI-powered natural language command generation** using Ollama. Simply describe what you want to do in plain English, and the AI will generate the appropriate cybersecurity command for you!

## 🌟 What Can AI Do?

Instead of remembering complex command syntax, just tell the AI what you want:

```bash
toolbox> ai scan example.com for open ports
[AI] 🤖 Generating command...
[AI] ✓ Generated: nmap -sV -sC example.com
Execute? (y/n/e=edit/f=favorites): y

toolbox> ai find subdomains of example.com
[AI] ✓ Generated: subfinder -d example.com -o subdomains.txt

toolbox> ai brute force directories on http://example.com
[AI] ✓ Generated: gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt

toolbox> ai test for SQL injection on http://example.com/login
[AI] ✓ Generated: sqlmap -u "http://example.com/login" --forms --batch
```

## 📋 Prerequisites

### System Requirements
- **Kali Linux** (or similar Debian-based pentesting distro)
- **4GB+ Free Disk Space** (for AI models)
- **4GB+ RAM** (recommended 8GB for better performance)
- **Internet Connection** (for initial model download)

### Required Software
- Python 3.6+
- Ollama (AI runtime)

---

## 🚀 Installation Guide

### Step 1: Install Ollama

```bash
# Download and install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

### Step 2: Start Ollama Service

```bash
# Ollama usually starts automatically, but you can manually start it:
ollama serve

# Or check if it's already running:
ps aux | grep ollama

# If running, you should see:
# /usr/local/bin/ollama serve
```

### Step 3: Download an AI Model

Choose one of these models based on your needs:

#### Option A: Fast & Efficient (Recommended for most users)
```bash
ollama pull codellama:7b
# Size: ~3.8 GB
# Best for: Quick command generation, lower RAM usage
```

#### Option B: Better Accuracy
```bash
ollama pull llama3
# Size: ~4.7 GB
# Best for: More accurate command generation
```

#### Option C: Lightweight
```bash
ollama pull phi
# Size: ~1.6 GB
# Best for: Systems with limited resources
```

#### Option D: Maximum Accuracy (Power Users)
```bash
ollama pull codellama:13b
# Size: ~7.4 GB
# Best for: Best accuracy, requires 8GB+ RAM
```

### Step 4: Verify Installation

```bash
# List installed models
ollama list

# Expected output:
# NAME                ID              SIZE      MODIFIED
# codellama:7b        8fdf8f752f6e    3.8 GB    2 minutes ago

# Test the model
ollama run codellama "Hello"
# Type /bye to exit the test
```

### Step 5: Configure Toolbox

```bash
# Start toolbox
toolbox

# Check AI status
toolbox> ai-status

# Expected output if everything is working:
# ╔═══════════════════════════════════════════════════════╗
# ║              AI System Status                         ║
# ╚═══════════════════════════════════════════════════════╝
# 
# Ollama Server: ✓ Running
# Current Model: codellama (✓ Available)
# 
# [✓] AI is ready to use!

# Configure model (optional)
toolbox> ai-config
```

---

## 🎯 Usage Examples

### Basic Commands

```bash
toolbox> ai scan 192.168.1.1
# Generates: nmap -sV -sC 192.168.1.1

toolbox> ai quick port scan on 192.168.1.1
# Generates: nmap -F 192.168.1.1

toolbox> ai full port scan 192.168.1.1
# Generates: nmap -p- 192.168.1.1
```

### Web Application Testing

```bash
toolbox> ai scan http://example.com for vulnerabilities
# Generates: nikto -h http://example.com

toolbox> ai find hidden directories on http://example.com
# Generates: gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt

toolbox> ai test for XSS on http://example.com
# Generates: dalfox url http://example.com
```

### Subdomain Discovery

```bash
toolbox> ai find subdomains of example.com
# Generates: subfinder -d example.com

toolbox> ai enumerate DNS records for example.com
# Generates: dnsrecon -d example.com
```

### Password Attacks

```bash
toolbox> ai brute force SSH on 192.168.1.100
# Generates: hydra -L /usr/share/wordlists/metasploit/unix_users.txt -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.100

toolbox> ai crack this hash with john
# Generates: john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

### Context-Aware Conversations

The AI remembers your previous commands and targets:

```bash
toolbox> ai scan example.com
[AI] ✓ Generated: nmap -sV -sC example.com

toolbox> ai now scan port 8080
# AI remembers "example.com" from previous command
[AI] ✓ Generated: nmap -p 8080 -sV example.com

toolbox> ai find subdomains
# Still remembers "example.com"
[AI] ✓ Generated: subfinder -d example.com
```

---

## 🎛️ AI Commands Reference

| Command | Description |
|---------|-------------|
| `ai <request>` | Generate command from natural language |
| `ai-status` | Check if Ollama is running and models are available |
| `ai-config` | Change AI model or view settings |
| `ai-context` | Show current conversation context (remembered targets) |
| `ai-clear` | Clear conversation context (fresh start) |
| `ai-help` | Show setup instructions |

---

## 🛡️ Safety Features

### Automatic Command Validation

The AI includes safety checks:

```bash
toolbox> ai delete all files
[AI] ✓ Generated: rm -rf /

⚠️  DANGEROUS: Command contains potentially harmful pattern: rm\s+-rf
This command may be dangerous. Continue? (yes/no): no
[!] Command cancelled for safety.
```

### Root Privilege Detection

```bash
toolbox> ai scan network
[AI] ✓ Generated: nmap -sS 192.168.1.0/24

[!] Note: This command may require root privileges (sudo)
Execute? (y/n): 
```

### Edit Before Execution

You can always edit AI-generated commands:

```bash
toolbox> ai scan example.com
[AI] ✓ Generated: nmap -sV -sC example.com

Execute? (y/n/e=edit/f=favorites): e
Command: nmap -sV -sC -p 80,443 example.com    ← Edited
Execute edited command? (y/n): y
```

---

## 🔧 Troubleshooting

### Problem: "Ollama is not running"

**Solution:**
```bash
# Start Ollama
ollama serve

# Or check if it's already running
systemctl status ollama
# OR
ps aux | grep ollama
```

### Problem: "Model not available"

**Solution:**
```bash
# Download the model
ollama pull codellama

# Verify it's installed
ollama list
```

### Problem: "Request timeout"

**Causes:**
- Model is loading for the first time (can take 10-30 seconds)
- System is low on RAM
- Ollama is processing another request

**Solutions:**
```bash
# Wait 30 seconds and try again
# Or use a smaller model:
ollama pull phi
toolbox> ai-config   # Select the phi model
```

### Problem: AI generates incorrect commands

**Solutions:**
1. Be more specific in your request:
   - ❌ "scan it"
   - ✅ "scan example.com for open ports"

2. Clear context if it's confused:
   ```bash
   toolbox> ai-clear
   ```

3. Try a different model:
   ```bash
   toolbox> ai-config   # Switch to llama3 for better accuracy
   ```

### Problem: "AI module not loaded"

**Solution:**
```bash
# Ensure toolbox_ai.py is in the same directory as toolbox.py
ls -la | grep toolbox
# You should see both:
# toolbox.py
# toolbox_ai.py

# Install required Python package
pip3 install requests
```

---

## 💡 Tips & Best Practices

### 1. Be Specific
```bash
# ❌ Too vague
toolbox> ai scan

# ✅ Better
toolbox> ai scan example.com for open ports
```

### 2. Include Targets
```bash
# ✅ Include IP/domain in your request
toolbox> ai find subdomains of example.com
toolbox> ai scan 192.168.1.1 ports 80 and 443
```

### 3. Use Context Feature
```bash
# First command sets context
toolbox> ai scan example.com

# Subsequent commands can reference it
toolbox> ai now scan port 8080
toolbox> ai find admin panel
```

### 4. Save Good Commands
```bash
toolbox> ai scan example.com for SQL injection
[AI] ✓ Generated: sqlmap -u http://example.com --forms --batch

Execute? (y/n/e=edit/f=favorites): f
Favorite name (optional): quick-sqlmap
[+] Added to favorites!
```

### 5. Review Before Executing
Always review AI-generated commands, especially for:
- Destructive operations
- Commands requiring root
- Network attacks
- Database modifications

---

## 🚦 Model Comparison

| Model | Size | Speed | Accuracy | RAM Usage | Best For |
|-------|------|-------|----------|-----------|----------|
| **phi** | 1.6 GB | ⚡⚡⚡ | ⭐⭐ | 2-4 GB | Limited resources |
| **codellama:7b** | 3.8 GB | ⚡⚡ | ⭐⭐⭐ | 4-6 GB | Most users (recommended) |
| **llama3** | 4.7 GB | ⚡ | ⭐⭐⭐⭐ | 6-8 GB | Better accuracy |
| **codellama:13b** | 7.4 GB | ⚡ | ⭐⭐⭐⭐⭐ | 8-12 GB | Power users |

---

## 📊 Performance Tips

### Optimize Model Performance

```bash
# Check RAM usage
free -h

# If low on memory, use a smaller model
ollama pull phi
toolbox> ai-config   # Select phi

# Restart Ollama to free memory
killall ollama
ollama serve
```

### First Request is Slow
The first AI request after starting Ollama loads the model into memory (10-30 seconds). Subsequent requests are much faster (1-3 seconds).

---

## 🔄 Uninstallation

If you want to remove AI features:

```bash
# Remove Ollama
sudo systemctl stop ollama
sudo rm /usr/local/bin/ollama
sudo rm -rf ~/.ollama

# Remove models (frees disk space)
rm -rf ~/.ollama/models

# Toolbox will continue to work without AI features
# AI commands will show: "AI features not available"
```

---

## 📚 Additional Resources

- **Ollama Documentation**: https://ollama.com/
- **Available Models**: https://ollama.com/library
- **Model Customization**: https://github.com/ollama/ollama/blob/main/docs/modelfile.md
- **Ollama API**: https://github.com/ollama/ollama/blob/main/docs/api.md

---

## 🆘 Support

If you encounter issues:

1. Check Ollama status: `toolbox> ai-status`
2. Review logs: `journalctl -u ollama`
3. Test Ollama directly: `ollama run codellama "test"`
4. Check system resources: `htop`
5. Restart Ollama: `killall ollama && ollama serve`

---

## 🎉 You're Ready!

AI features are now set up! Try your first command:

```bash
toolbox> ai scan scanme.nmap.org
```

Enjoy the power of natural language cybersecurity commands! 🚀
