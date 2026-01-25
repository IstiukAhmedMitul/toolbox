# 🏗️ Architecture

Technical architecture and design of Toolbox v2.0 + AI.

## 📊 System Overview

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│              (Interactive CLI / Direct Mode)             │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│                  Main Controller                         │
│                   (toolbox.py)                          │
│  ┌──────────────┬──────────────┬──────────────────────┐│
│  │ Tool Manager │ AI Engine    │ Command Executor     ││
│  │              │ Integration  │                      ││
│  └──────────────┴──────────────┴──────────────────────┘│
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│                Backend Services                          │
│  ┌────────────┬──────────────┬─────────────────────────┤
│  │ Tools DB   │ AI Module    │ Storage & Config        │
│  │(toolbox_   │(toolbox_ai.  │(~/.toolbox/)            │
│  │ api.py)    │py)           │                         │
│  └────────────┴──────────────┴─────────────────────────┘
└─────────────────────────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│              External Services                           │
│  ┌────────────────────┬────────────────────────────────┐│
│  │ Security Tools     │ Groq AI API                    ││
│  │ (nmap, gobuster..) │ (api.groq.com)                 ││
│  └────────────────────┴────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

## 🗂️ File Structure

```
toolbox/
├── toolbox.py              # Main application (4600+ lines)
├── toolbox_ai.py          # AI module (260 lines)
├── toolbox_api.py         # Tools database (100+ tools)
├── install.sh             # Automated installer
│
├── README.md              # Main documentation
├── LICENSE                # MIT License
│
├── AI_SETUP.md           # AI configuration guide
├── AI_EXAMPLES.md        # AI usage examples
├── INSTALLATION.md       # Installation guide
├── FEATURES_GUIDE.md     # Features overview
├── CUSTOM_COMMANDS.md    # Custom commands guide
├── QUICK_REFERENCE.md    # Quick reference
├── ARCHITECTURE.md       # This file
└── TESTING_GUIDE.md      # Testing guide
```

## 🔧 Core Components

### 1. Main Controller (toolbox.py)

**Responsibilities:**
- User interaction & CLI
- Command parsing & routing
- Tool execution & output management
- History & favorites management
- Configuration management

**Key Classes:**
```python
class Toolbox:
    def __init__(self)
    def run(self)
    def interact_with_tool(tool_name)
    def run_command(command)
    def handle_ai_command(request)
    def add_to_favorites()
    def add_custom_command()
```

**Key Features:**
- Interactive mode with readline support
- Real-time command output (subprocess.Popen)
- System command passthrough
- Multi-target support with placeholders

### 2. AI Module (toolbox_ai.py)

**Responsibilities:**
- Natural language processing
- Command generation
- Context management
- Groq API communication

**Key Classes:**
```python
class ToolboxAI:
    def __init__(tools_db, config_dir)
    def generate_command(request)
    def _build_system_prompt()
    def _clean_command(command)
    def get_status()
```

**AI Flow:**
```
User Request
    ↓
Extract Context (target, tool)
    ↓
Build System Prompt (tools + rules)
    ↓
Groq API Call
    ↓
Clean Response (remove labels)
    ↓
Return Command
```

### 3. Tools Database (toolbox_api.py)

**Structure:**
```python
{
    "nmap": {
        "description": "Network scanner",
        "category": "network-scanner",
        "requires_target": True,
        "examples": [
            {
                "name": "Basic scan",
                "command": "nmap -sV {target}"
            }
        ]
    }
}
```

**Categories:**
- network-scanner
- web-scanner
- vulnerability-scanner
- password-cracker
- wireless
- enumeration
- exploitation
- forensics

## 💾 Data Storage

### Configuration Directory: `~/.toolbox/`

```
~/.toolbox/
├── config.json              # Main configuration
├── history.json             # Command history
├── favorites.json           # Saved favorites
├── custom_commands.json     # Custom commands
├── ai_config.json          # AI configuration
├── templates.json          # Command templates (future)
├── workflows.json          # Workflows (future)
└── outputs/                # Saved outputs
```

### Data Formats

**history.json:**
```json
[
    {
        "tool": "nmap",
        "command": "nmap -sV 192.168.1.1",
        "target": "192.168.1.1",
        "timestamp": "2026-01-25T10:30:00"
    }
]
```

**ai_config.json:**
```json
{
    "provider": "groq",
    "model": "llama-3.1-8b-instant",
    "groq_api_key": "gsk_..."
}
```

**custom_commands.json:**
```json
{
    "quickscan": {
        "description": "Quick port scan",
        "command": "nmap -p- -T4 {target}"
    }
}
```

## 🔄 Command Execution Flow

### Normal Tool Execution
```
1. User selects tool
2. Load tool definition from database
3. Build command with examples
4. Prompt for target/wordlist (if needed)
5. Execute with subprocess.Popen
6. Stream output in real-time
7. Store in history
8. Offer post-execution options (save, favorite, retry)
```

### AI-Powered Execution
```
1. User types "ai <request>"
2. Send to ToolboxAI.generate_command()
3. AI builds command from natural language
4. Show command to user
5. User confirms/edits/saves
6. Execute command (same as normal)
7. Store in AI context & history
```

## 🌐 API Integration

### Groq AI API

**Endpoint:** `https://api.groq.com/openai/v1/chat/completions`

**Request:**
```json
{
    "model": "llama-3.1-8b-instant",
    "messages": [
        {"role": "system", "content": "<system_prompt>"},
        {"role": "user", "content": "scan 192.168.1.1"}
    ],
    "temperature": 0.3,
    "max_tokens": 500
}
```

**Response:**
```json
{
    "choices": [{
        "message": {
            "content": "nmap -sV 192.168.1.1"
        }
    }]
}
```

## ⚡ Performance Optimizations

1. **Lazy Loading**: AI module loaded only when needed
2. **Caching**: Tools database loaded once at startup
3. **Streaming Output**: Real-time display (no buffering)
4. **JSON Storage**: Fast file-based storage
5. **Minimal Dependencies**: Only `requests` library

## 🔐 Security Design

### Input Validation
- Command sanitization
- Dangerous command detection
- API key encryption in transit

### Isolation
- No shell injection (subprocess with list args)
- Separate config directory
- User-level permissions only

### Privacy
- Local storage only
- No telemetry
- API calls over HTTPS

## 🧩 Extensibility

### Adding New Tools
```python
# In toolbox_api.py
TOOLS_DB = {
    "newtool": {
        "description": "New security tool",
        "category": "category",
        "requires_target": True,
        "examples": [...]
    }
}
```

### Adding Custom Commands
Users can add via UI:
```bash
toolbox> add-custom
```

### AI Model Support
Easy to add new models:
```python
# In toolbox_ai.py
def get_available_models():
    return [
        "llama-3.1-8b-instant",
        "new-model-name"  # Add here
    ]
```

## 📈 Scalability

**Current Limits:**
- Tools: 100+ (can easily add 1000+)
- History: Unlimited (JSON-based)
- Favorites: Unlimited
- Custom Commands: Unlimited
- AI Requests: 14,400/day (Groq free tier)

**Memory Usage:**
- Idle: ~20 MB
- Active: ~50 MB
- With AI: ~50 MB (cloud-based)

## 🔮 Future Architecture

**Planned Enhancements:**
- Plugin system for tools
- Database backend (SQLite)
- Multi-user support
- Web dashboard
- Team collaboration features
- Offline AI mode (optional)

## 🛠️ Development Stack

- **Language**: Python 3.6+
- **HTTP Client**: requests
- **Process Management**: subprocess
- **CLI**: readline (optional)
- **Storage**: JSON files
- **AI Provider**: Groq API

## 📊 Dependencies

**Required:**
- Python 3.6+
- requests

**Optional:**
- readline (for better CLI UX)
- Security tools (nmap, gobuster, etc.)

**External Services:**
- Groq AI API (free tier)

---

**Technical documentation complete! See [TESTING_GUIDE.md](TESTING_GUIDE.md) for testing procedures.**
