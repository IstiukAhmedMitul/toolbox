# 🧪 Testing Guide - Verify Your AI Implementation

## Quick Test Checklist

Use this guide to verify your AI implementation is working correctly.

---

## ✅ Phase 1: Basic Functionality (No AI Required)

### Test 1: Toolbox Starts
```bash
cd /path/to/toolbox
python3 toolbox.py

# Expected output:
# - ASCII banner appears
# - "toolbox>" prompt shows
# - No errors
```
**Status**: ⬜ Pass / ⬜ Fail

---

### Test 2: Traditional Commands Work
```bash
toolbox> help

# Expected: Shows command list including AI commands

toolbox> list

# Expected: Shows all 100+ tools

toolbox> use nmap

# Expected: Shows nmap options and prompts for target
```
**Status**: ⬜ Pass / ⬜ Fail

---

### Test 3: AI Commands Show Properly
```bash
toolbox> help

# Expected: Should see:
# [+] AI Commands (Natural Language):
#   ai <request>
#   ai-status
#   ai-config
#   etc.
```
**Status**: ⬜ Pass / ⬜ Fail

---

## ✅ Phase 2: AI Availability Check

### Test 4: Check AI Module Loaded
```bash
toolbox> ai-status

# If AI module loaded:
# ╔═══════════════════════════════════╗
# ║      AI System Status             ║
# ╚═══════════════════════════════════╝
#
# Ollama Server: ✗ Not Running  (OK if Ollama not installed yet)

# If AI module NOT loaded:
# [!] AI module not loaded
```
**Status**: ⬜ Pass / ⬜ Fail

---

### Test 5: AI Help Shows
```bash
toolbox> ai-help

# Expected: Shows Ollama installation instructions
```
**Status**: ⬜ Pass / ⬜ Fail

---

## ✅ Phase 3: Ollama Installation (Optional)

### Test 6: Install Ollama
```bash
# On Kali Linux:
curl -fsSL https://ollama.com/install.sh | sh

# Verify:
ollama --version

# Expected: ollama version X.X.X
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

### Test 7: Start Ollama
```bash
# Start server
ollama serve

# In another terminal:
ps aux | grep ollama

# Expected: Process running
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

### Test 8: Download Model
```bash
ollama pull codellama

# Expected: Downloads ~3.8GB model
# Time: 5-20 minutes depending on connection

# Verify:
ollama list

# Expected: Shows codellama in list
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

## ✅ Phase 4: AI Integration Tests

### Test 9: AI Status Check
```bash
toolbox> ai-status

# Expected with Ollama running:
# Ollama Server: ✓ Running
# Current Model: codellama (✓ Available)
# [✓] AI is ready to use!
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

### Test 10: First AI Command
```bash
toolbox> ai scan scanme.nmap.org

# Expected:
# [AI] 🤖 Generating command...
# [AI] Request: scan scanme.nmap.org
# [AI] ✓ Generated: nmap -sV -sC scanme.nmap.org
# Execute? (y/n/e=edit/f=favorites):

# Type: n (don't execute, just testing)
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

**Notes**:
- First request may take 10-30 seconds (model loading)
- Subsequent requests should be faster (1-3 seconds)

---

### Test 11: Context Awareness
```bash
toolbox> ai scan example.com
# Type: n

toolbox> ai now scan port 8080

# Expected: Should generate command with example.com
# [AI] ✓ Generated: nmap -p 8080 -sV example.com

toolbox> ai-context

# Expected: Shows last_target: example.com
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

### Test 12: Safety Validation
```bash
toolbox> ai delete all files

# Expected:
# [AI] ✓ Generated: rm -rf /
# ⚠️  DANGEROUS: Command contains harmful pattern
# This command may be dangerous. Continue? (yes/no):

# Type: no
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

### Test 13: Edit Mode
```bash
toolbox> ai scan example.com

# When prompted:
# Execute? (y/n/e=edit/f=favorites): e

# Expected: Pre-filled command that you can edit
# Command: nmap -sV -sC example.com

# Edit it and press Enter
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

### Test 14: Add to Favorites
```bash
toolbox> ai scan example.com

# When prompted:
# Execute? (y/n/e=edit/f=favorites): f

# Favorite name: test-scan
# Expected: [+] Added to favorites!

toolbox> favorites

# Expected: Shows "test-scan" in list
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

### Test 15: Clear Context
```bash
toolbox> ai-clear

# Expected:
# [+] AI context cleared
# [+] Starting fresh conversation

toolbox> ai-context

# Expected: Shows empty context
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

### Test 16: Model Configuration
```bash
toolbox> ai-config

# Expected: Shows current model and available models
# Allows selecting different model if multiple installed
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

## ✅ Phase 5: Advanced AI Tests

### Test 17: Complex Request
```bash
toolbox> ai find all subdomains of example.com and save to file

# Expected: Generates appropriate command
# Example: subfinder -d example.com -o subdomains.txt
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

### Test 18: Multiple Tools
```bash
toolbox> ai scan http://example.com for vulnerabilities

# Could generate nikto, nuclei, or other web scanners
# Verify it picks appropriate tool
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

### Test 19: Specific Tool Request
```bash
toolbox> ai use gobuster to find directories on http://example.com

# Expected: Should generate gobuster command
# Not nmap or other tools
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

### Test 20: Root Privilege Detection
```bash
toolbox> ai perform syn scan on 192.168.1.1

# Expected:
# [AI] ✓ Generated: nmap -sS 192.168.1.1
# [!] Note: This command may require root privileges (sudo)
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

## ✅ Phase 6: Error Handling

### Test 21: Ollama Not Running
```bash
# Stop Ollama:
killall ollama

# Then:
toolbox> ai scan example.com

# Expected:
# [!] Ollama is not running.
# [!] Start Ollama with: ollama serve
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

### Test 22: Model Not Available
```bash
# Change to non-existent model in config
toolbox> ai-config
# Select invalid model

toolbox> ai scan example.com

# Expected:
# [!] Model 'xyz' is not available.
# [!] Download it with: ollama pull xyz
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

### Test 23: Empty Request
```bash
toolbox> ai

# Expected:
# [!] Please provide a request. Example: ai scan example.com
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

## ✅ Phase 7: Integration Tests

### Test 24: History Tracking
```bash
toolbox> ai scan example.com
# Execute: y

toolbox> history

# Expected: AI-generated command appears in history
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

### Test 25: Workflow with AI
```bash
# Use AI multiple times in sequence
toolbox> ai scan example.com
toolbox> ai find hidden directories
toolbox> ai test for SQL injection

# Verify context is maintained
# Verify all execute properly
```
**Status**: ⬜ Pass / ⬜ Fail / ⬜ Skipped

---

## 📊 Test Results Summary

### Required Tests (No AI)
- [ ] Test 1: Toolbox starts
- [ ] Test 2: Traditional commands work
- [ ] Test 3: AI commands show in help
- [ ] Test 4: AI module loaded
- [ ] Test 5: AI help shows

**Result**: ___/5 passed

---

### AI Tests (Requires Ollama)
- [ ] Test 6: Ollama installed
- [ ] Test 7: Ollama running
- [ ] Test 8: Model downloaded
- [ ] Test 9: AI status check
- [ ] Test 10: First AI command
- [ ] Test 11: Context awareness
- [ ] Test 12: Safety validation
- [ ] Test 13: Edit mode
- [ ] Test 14: Add to favorites
- [ ] Test 15: Clear context
- [ ] Test 16: Model config
- [ ] Test 17: Complex request
- [ ] Test 18: Multiple tools
- [ ] Test 19: Specific tool
- [ ] Test 20: Root detection
- [ ] Test 21: Error: Ollama not running
- [ ] Test 22: Error: Model not available
- [ ] Test 23: Error: Empty request
- [ ] Test 24: History tracking
- [ ] Test 25: Workflow with AI

**Result**: ___/20 passed

---

## 🔍 Common Issues & Solutions

### Issue 1: "AI module not loaded"
**Cause**: toolbox_ai.py not found or import error

**Solution**:
```bash
# Check file exists
ls -la toolbox_ai.py

# Check for syntax errors
python3 -m py_compile toolbox_ai.py

# Install dependencies
pip3 install --user requests
```

---

### Issue 2: "Ollama is not running"
**Cause**: Ollama service not started

**Solution**:
```bash
# Start Ollama
ollama serve

# Or check if already running
ps aux | grep ollama
systemctl status ollama
```

---

### Issue 3: First request takes forever
**Cause**: Model loading into memory

**Solution**:
- This is normal for first request (10-30 seconds)
- Subsequent requests are much faster
- Consider using smaller model (phi) if too slow

---

### Issue 4: Command quality is poor
**Cause**: Model not suitable for task

**Solution**:
```bash
# Try different model
toolbox> ai-config

# Recommended order:
# 1. llama3 (best accuracy)
# 2. codellama:13b (if you have RAM)
# 3. codellama:7b (balanced)
# 4. phi (fast but less accurate)
```

---

### Issue 5: "requests module not found"
**Cause**: Python requests library not installed

**Solution**:
```bash
pip3 install --user requests
# OR
python3 -m pip install --user requests
```

---

## ✅ Final Verification

All tests passing? Great! Your AI implementation is working perfectly! 🎉

Some tests failing? Check:
1. Python version: `python3 --version` (need 3.6+)
2. Dependencies: `pip3 list | grep requests`
3. File permissions: `ls -la toolbox*.py`
4. Ollama status: `toolbox> ai-status`
5. Error logs in terminal output

---

## 📝 Test Log Template

Copy this to track your testing:

```
Test Date: _____________
Tester: ________________
Python Version: ________
OS: ____________________

Phase 1 (Basic): ___/5
Phase 2 (AI Check): ___/2
Phase 3 (Ollama): ___/3 (or skipped)
Phase 4 (Integration): ___/8
Phase 5 (Advanced): ___/4
Phase 6 (Errors): ___/3
Phase 7 (Integration): ___/2

Total: ___/27

Notes:
_______________________
_______________________
_______________________
```

---

**Happy Testing! 🧪✅**
