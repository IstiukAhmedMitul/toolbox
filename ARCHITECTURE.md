# 🏗️ Toolbox AI Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER                                  │
│                          │                                   │
│                    Natural Language                          │
│              "scan example.com for vulnerabilities"          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    TOOLBOX.PY                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Interactive Mode                                     │  │
│  │  - Command Parser                                     │  │
│  │  - AI Command Handler                                 │  │
│  │  - Traditional Tool Handler                           │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────┬────────────────────────────┬─────────────────┘
               │                            │
         AI Commands                  Traditional Commands
               │                            │
               ▼                            ▼
┌─────────────────────────────┐  ┌────────────────────────────┐
│     TOOLBOX_AI.PY           │  │   Tool Database            │
│                             │  │   - 100+ Tools             │
│  ┌──────────────────────┐  │  │   - Command Templates      │
│  │  ToolboxAI Class     │  │  │   - Categories             │
│  │  - NLP Processing    │  │  └────────────────────────────┘
│  │  - Context Memory    │  │
│  │  - Target Extraction │  │
│  └──────────────────────┘  │
│                             │
│  ┌──────────────────────┐  │
│  │  AICommandValidator  │  │
│  │  - Safety Checks     │  │
│  │  - Root Detection    │  │
│  └──────────────────────┘  │
└──────────┬──────────────────┘
           │
           │ HTTP API Call
           ▼
┌─────────────────────────────────────────────────────────────┐
│                    OLLAMA SERVER                             │
│                  (localhost:11434)                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                                                        │  │
│  │         AI Model (codellama/llama3/phi)               │  │
│  │                                                        │  │
│  │  - Natural Language Understanding                     │  │
│  │  - Command Generation                                 │  │
│  │  - Context Processing                                 │  │
│  │                                                        │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    Generated Command
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   COMMAND EXECUTION                          │
│                                                              │
│  1. Safety Validation    ✓                                  │
│  2. User Confirmation    ✓                                  │
│  3. Execute              ✓                                  │
│  4. Save to History      ✓                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. User Input
```
User: "ai scan example.com for open ports"
```

### 2. Request Processing
```python
ToolboxAI.generate_command(request)
  ├─> Extract target: "example.com"
  ├─> Build system prompt with tool database
  ├─> Send to Ollama API
  └─> Receive generated command
```

### 3. AI Generation
```
Ollama Model:
  Input: Natural language + Tool database + Context
  Output: "nmap -sV -sC example.com"
```

### 4. Validation
```python
AICommandValidator.is_safe(command)
  ├─> Check dangerous patterns
  ├─> Check root requirements
  └─> Return (is_safe, warning)
```

### 5. User Interaction
```
[AI] ✓ Generated: nmap -sV -sC example.com
Execute? (y/n/e=edit/f=favorites):
```

### 6. Execution
```python
subprocess.run(command)
  ├─> Execute command
  ├─> Capture output
  └─> Save to history
```

---

## Component Details

### Toolbox.py (Main Application)
```python
class Toolbox:
    - __init__(): Initialize AI if available
    - interactive_mode(): Main loop
    - handle_ai_command(): Process AI requests
    - show_ai_status(): Check AI readiness
    - configure_ai(): Model management
    - Traditional tool methods (unchanged)
```

### toolbox_ai.py (AI Engine)
```python
class ToolboxAI:
    - generate_command(): Main AI function
    - is_ollama_available(): Check server
    - is_model_available(): Check model
    - _build_system_prompt(): Create AI prompt
    - _extract_target_from_request(): Find IPs/domains
    - Context management methods

class AICommandValidator:
    - is_safe(): Safety validation
    - requires_root(): Privilege check
```

---

## Context Management

### Session Context
```python
context = {
    "last_target": "example.com",
    "last_tool": "nmap",
    "conversation_history": [
        {"request": "scan example.com", 
         "command": "nmap -sV example.com"},
        {"request": "scan port 8080",
         "command": "nmap -p 8080 example.com"}
    ]
}
```

### How Context Works
```
Request 1: "ai scan example.com"
  └─> Sets context.last_target = "example.com"

Request 2: "ai now scan port 8080"
  └─> Reads context.last_target
  └─> Generates: nmap -p 8080 example.com

Request 3: "ai find subdomains"
  └─> Still uses context.last_target
  └─> Generates: subfinder -d example.com
```

---

## Tool Database Integration

### How AI Uses Tool Database
```python
# AI receives tool information
tools_info = [
    "- nmap: Network discovery and security auditing",
    "- gobuster: Directory/file brute forcing",
    "- sqlmap: SQL injection detection",
    # ... 100+ more tools
]

# System Prompt includes:
"""
Available tools:
- nmap: Network discovery and security auditing
- gobuster: Directory/file brute forcing
...

User request: scan example.com
Generate the appropriate command using these tools.
"""
```

---

## Safety Features

### Dangerous Pattern Detection
```python
DANGEROUS_PATTERNS = [
    r'rm\s+-rf',      # Recursive delete
    r'mkfs',          # Format filesystem
    r'dd\s+if=',      # Disk operations
    r'shutdown',      # System shutdown
    # ... more patterns
]
```

### Validation Flow
```
Command: "rm -rf /"
  ├─> Check patterns
  ├─> Match found: rm\s+-rf
  ├─> Return: (False, "DANGEROUS: ...")
  └─> Require explicit confirmation
```

---

## File Structure

```
toolbox/
├── toolbox.py              # Main application (modified)
├── toolbox_ai.py           # AI engine (NEW)
├── toolbox_api.py          # API server (unchanged)
│
├── README_NEW.md           # Main docs (updated)
├── AI_SETUP.md             # AI setup guide (NEW)
├── AI_EXAMPLES.md          # AI examples (NEW)
├── AI_IMPLEMENTATION_SUMMARY.md  # This summary (NEW)
├── ARCHITECTURE.md         # This file (NEW)
│
├── FEATURES_GUIDE.md       # Features guide
├── WHATS_NEW.md           # Changelog
├── INSTALLATION.md         # Install guide
├── QUICK_REFERENCE.md      # Quick ref
└── install.sh             # Installer (updated)

~/.toolbox/                 # User config directory
├── history.json            # Command history
├── favorites.json          # Favorite commands
├── templates.json          # Command templates
├── workflows.json          # Workflow definitions
├── config.json             # User config
├── ai_config.json          # AI config (NEW)
└── outputs/                # Command outputs
    ├── scans/
    └── reports/
```

---

## API Communication

### Ollama API Endpoint
```
POST http://localhost:11434/api/chat
```

### Request Format
```json
{
  "model": "codellama",
  "messages": [
    {
      "role": "system",
      "content": "You are a cybersecurity command expert..."
    },
    {
      "role": "user", 
      "content": "scan example.com for open ports"
    }
  ],
  "stream": false,
  "options": {
    "temperature": 0.3,
    "top_p": 0.9
  }
}
```

### Response Format
```json
{
  "message": {
    "role": "assistant",
    "content": "nmap -sV -sC example.com"
  },
  "done": true
}
```

---

## Error Handling

### Graceful Degradation
```python
# AI module fails to import
if AI_AVAILABLE:
    # Use AI features
else:
    # Fall back to traditional mode
    print("[!] AI features not available")
```

### Common Errors
1. **Ollama not running**
   - Detect: Connection refused
   - Action: Show instructions

2. **Model not downloaded**
   - Detect: 404 from API
   - Action: Suggest `ollama pull`

3. **Request timeout**
   - Detect: Timeout exception
   - Action: Retry or suggest smaller model

---

## Performance Characteristics

### First Request
```
Cold start: 10-30 seconds
  ├─> Load model into memory: 8-25s
  ├─> Process request: 1-3s
  └─> Generate command: 1-2s
```

### Subsequent Requests
```
Warm: 1-3 seconds
  ├─> Model already loaded: 0s
  ├─> Process request: 0.5-1s
  └─> Generate command: 0.5-2s
```

### Memory Usage
```
Model in RAM:
  ├─> phi: 2-3 GB
  ├─> codellama:7b: 4-5 GB
  └─> llama3: 6-7 GB
```

---

## Security Considerations

### 1. Local Execution Only
- No cloud services
- No data leaves machine
- Complete privacy

### 2. User Confirmation
- All commands require approval
- Edit capability before execution
- Dangerous command warnings

### 3. Input Validation
- Sanitize user input
- Validate AI output
- Check for injection attempts

### 4. Logging
- All commands logged
- Timestamps recorded
- Audit trail maintained

---

## Future Enhancements

### Potential Improvements
1. **Custom Models**
   - Fine-tune on pentesting data
   - Specialized tool knowledge

2. **Multi-Step Workflows**
   - AI-generated attack chains
   - Automated exploitation paths

3. **Result Analysis**
   - AI-powered output parsing
   - Vulnerability identification

4. **Voice Interface**
   - Speech-to-text
   - Hands-free operation

5. **Collaboration**
   - Team command sharing
   - AI learning from team

---

## Technology Stack

```
┌─────────────────────────────────────┐
│  Python 3.6+                        │
│  ├─ Core language                   │
│  ├─ subprocess (command execution)  │
│  ├─ json (config management)        │
│  └─ pathlib (file operations)       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Ollama                             │
│  ├─ Local AI runtime                │
│  ├─ Model management                │
│  └─ API server                      │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  AI Models                          │
│  ├─ CodeLlama (code generation)     │
│  ├─ Llama3 (general purpose)        │
│  └─ Phi (lightweight)               │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Python Libraries                   │
│  └─ requests (HTTP client)          │
└─────────────────────────────────────┘
```

---

**This architecture provides a robust, secure, and user-friendly AI-powered command generation system while maintaining backward compatibility with traditional toolbox features.**
