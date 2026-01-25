# 🧪 Testing Guide

Comprehensive testing procedures for Toolbox v2.0 + AI before deployment.

## ✅ Pre-Deployment Checklist

### Installation Tests
```bash
# 1. Clone repository
git clone https://github.com/IstiukAhmedMitul/toolbox.git
cd toolbox

# 2. Run installer
chmod +x install.sh
./install.sh

# 3. Verify global install
which toolbox
# Should output: /usr/local/bin/toolbox

# 4. Test launch
toolbox
# Should display banner without errors
```

### Core Functionality Tests
```bash
# Basic commands
toolbox> help
toolbox> list nmap
toolbox> search scan
toolbox> show nmap
toolbox> history
toolbox> config
toolbox> exit
```

## 🤖 AI Features Testing

### 1. AI Configuration
```bash
toolbox> ai-status
# Should show: "Groq API: ✗ Not Configured"

toolbox> ai-config
# Enter test API key
# Select model (option 1)
# Should show: "[✓] Configuration complete!"

toolbox> ai-status
# Should now show: "Groq API: ✓ Configured"
```

### 2. AI Command Generation (15+ Tests)

**Network Scanning:**
```bash
ai scan 192.168.1.1
ai find open ports on 192.168.1.1
ai quick scan 192.168.1.0/24
ai scan for web services on 192.168.1.1
ai discover hosts on 192.168.1.0/24
```

**Expected**: Should generate valid nmap commands

**Web Testing:**
```bash
ai scan http://example.com for directories
ai find hidden files on http://example.com
ai test http://example.com for SQL injection
ai enumerate subdomains of example.com
```

**Expected**: Should generate gobuster, sqlmap, subfinder commands

**Password Attacks:**
```bash
ai brute force SSH on 192.168.1.1
ai crack password hash
ai dictionary attack on 192.168.1.1 FTP
```

**Expected**: Should generate hydra, john commands

**Enumeration:**
```bash
ai enumerate SMB shares on 192.168.1.1
ai list SMB users on 192.168.1.1
ai scan DNS for example.com
```

**Expected**: Should generate enum4linux, smbmap, dnsenum commands

### 3. AI Context Testing
```bash
ai scan 192.168.1.100
# Note the target

ai enumerate SMB shares
# Should remember target: 192.168.1.100

ai-context
# Should show: Last Target: 192.168.1.100

ai-clear
# Should clear context

ai-context
# Should show: Last Target: None
```

### 4. AI Model Switching
```bash
ai-config
# Select "Update API key? (y/n): n"
# Select different model (option 2)
# Should update without re-entering key
```

## 🛠️ Tool Execution Testing

### 1. Basic Tool Usage
```bash
toolbox> use nmap
# Select example
# Enter target: 127.0.0.1
# Should execute scan
```

### 2. Custom Commands
```bash
toolbox> add-custom
Name: testcmd
Description: Test command
Command: echo "Test: {target}"

toolbox> list-custom
# Should show testcmd

toolbox> use testcmd
Target: hello
# Should output: Test: hello

toolbox> remove-custom testcmd
toolbox> list-custom
# Should not show testcmd
```

### 3. Favorites
```bash
toolbox> add-favorite nmap
Name: quick-scan

toolbox> list-favorites
# Should show quick-scan

toolbox> quick-scan 127.0.0.1
# Should execute nmap scan
```

### 4. Output Management
```bash
toolbox> ai scan 127.0.0.1
# Execute (y)
# Wait for completion

toolbox> view-output
# Should display last scan output

toolbox> save-output
Filename: test_output.txt
# Should save successfully

# Verify file exists
ls -la test_output.txt
```

## 🎯 Edge Cases & Error Handling

### 1. Invalid Commands
```bash
toolbox> random-command
# Should show: "[!] Unknown command"

toolbox> ai
# Should show: "[!] Please provide a request"

toolbox> ai test
# Should attempt to generate or ask for clarification
```

### 2. Missing Tools
```bash
toolbox> use nonexistent-tool
# Should show error or prompt to install
```

### 3. AI Errors
```bash
# Test with invalid API key
toolbox> ai-config
# Enter invalid key: "test123"

toolbox> ai scan 192.168.1.1
# Should show: "[!] Invalid Groq API key"
```

### 4. Network Issues
```bash
# Disconnect internet
toolbox> ai scan 192.168.1.1
# Should show: "[!] Cannot connect to Groq API"
```

## 🔐 Security Testing

### 1. Dangerous Command Detection
```bash
toolbox> ai delete all files
# Should show warning: "[!] WARNING: This command may be dangerous!"
```

### 2. Sudo Detection
```bash
toolbox> ai scan network with nmap
# Should show: "[!] Note: This command may require root privileges"
```

### 3. Command Injection Prevention
```bash
# Try various injection attempts
toolbox> use nmap
Target: 127.0.0.1; rm -rf /
# Should execute safely without injection
```

## 📊 Performance Testing

### 1. Startup Time
```bash
time toolbox --help
# Should be < 2 seconds
```

### 2. AI Response Time
```bash
# Time AI generation
toolbox> ai scan 192.168.1.1
# Should respond in < 3 seconds
```

### 3. Tool Search Speed
```bash
toolbox> search web
# Should return instantly
```

## 🔄 Regression Tests

After any code changes, run:

### Quick Test Suite
```bash
# 1. Installation
./install.sh

# 2. Basic commands
toolbox
help
exit

# 3. AI status
toolbox> ai-status
toolbox> exit

# 4. Tool usage
toolbox> list nmap
toolbox> exit
```

### Full Test Suite
Run all tests from sections above (30 minutes)

## 📝 Test Results Template

```markdown
## Test Session: [Date]

### Environment
- OS: Kali Linux 2024.x
- Python: 3.x.x
- Groq API: Active

### Installation
- [ ] Installer completes successfully
- [ ] Global command works
- [ ] Banner displays correctly

### Core Features
- [ ] Help command works
- [ ] Tool listing works
- [ ] Search works
- [ ] Tool execution works
- [ ] History works

### AI Features
- [ ] AI configuration works
- [ ] AI generates valid commands (10/10 tests)
- [ ] Context awareness works
- [ ] Model switching works
- [ ] Error handling works

### Custom Features
- [ ] Custom commands work
- [ ] Favorites work
- [ ] Output viewing works
- [ ] Output saving works

### Edge Cases
- [ ] Invalid commands handled
- [ ] Network errors handled
- [ ] Security warnings work

### Performance
- [ ] Startup < 2s
- [ ] AI response < 3s
- [ ] No memory leaks

### Issues Found
[List any issues]

### Status
[ ] Ready for deployment
[ ] Needs fixes
```

## 🐛 Known Issues

Document any known issues here:

```markdown
1. Issue: [Description]
   - Impact: [High/Medium/Low]
   - Workaround: [If any]
   - Status: [Open/Fixed]
```

## 🚀 Deployment Readiness

Before pushing to GitHub:

- [ ] All core tests pass
- [ ] AI features tested with real API
- [ ] No syntax errors in any file
- [ ] Documentation is up-to-date
- [ ] Version numbers consistent
- [ ] No sensitive data in code
- [ ] .gitignore configured
- [ ] README.md complete

## 📞 Reporting Issues

If tests fail:

1. Document the exact steps to reproduce
2. Include error messages
3. Note your environment (OS, Python version)
4. Check GitHub Issues
5. Create new issue if needed

## 🎓 Automated Testing (Future)

```python
# Future: pytest integration
# test_toolbox.py

def test_installation():
    assert os.path.exists('/usr/local/bin/toolbox')

def test_ai_generation():
    ai = ToolboxAI(tools_db, config_dir)
    success, cmd = ai.generate_command("scan 192.168.1.1")
    assert success
    assert "nmap" in cmd

def test_custom_commands():
    # Test custom command CRUD
    pass
```

---

**Testing complete! See [README.md](README.md) for deployment.**
