# 🤖 AI Features Guide - Natural Language Command Generation

## Overview

Toolbox v2.0 includes **AI-powered natural language command generation** using Groq API. Simply describe what you want to do in plain English, and the AI will generate the appropriate cybersecurity command!

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Your FREE Groq API Key

1. Visit: https://console.groq.com/
2. Sign up (no credit card needed)
3. Click "API Keys" → "Create API Key"
4. Copy your key (starts with `gsk_...`)

### Step 2: Configure Toolbox

```bash
toolbox
toolbox> ai-config
# Paste your API key
# Select model (press 1 for recommended)
```

### Step 3: Test It!

```bash
toolbox> ai-status
toolbox> ai scan 192.168.1.1
```

## 💡 Example Commands

```bash
ai scan 192.168.1.1
ai find open ports on 192.168.1.1
ai scan http://example.com for directories
ai brute force SSH on 192.168.1.1
ai enumerate SMB shares on 192.168.1.1
ai test for SQL injection on http://example.com
```

## 🎯 AI Commands

- `ai <request>` - Generate command
- `ai-status` - Check status
- `ai-config` - Configure API key/model
- `ai-context` - View context
- `ai-clear` - Clear history
- `ai-help` - Show help

## 📊 Models

| Model | Speed | Best For |
|-------|-------|----------|
| llama-3.1-8b-instant | ⚡⚡⚡ | Recommended |
| llama-3.3-70b-versatile | ⚡ | Complex commands |
| mixtral-8x7b-32768 | ⚡⚡ | Large context |

## 💰 Free Tier
- 30 requests/minute
- 14,400 requests/day
- No credit card needed

## 🔒 Privacy
- API key stored in `~/.toolbox/ai_config.json`
- HTTPS encryption
- Groq doesn't store your prompts

**Happy Hacking! 🚀**
