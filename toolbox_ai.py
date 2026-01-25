#!/usr/bin/env python3
"""
Toolbox AI Module - Natural Language Command Generation
Uses Ollama for local AI-powered command generation

Features:
- Natural language to command translation
- Context-aware conversations
- Tool database integration
- Smart parameter extraction
"""

import json
import requests
import subprocess
from typing import Optional, Dict, List, Tuple
from pathlib import Path


class ToolboxAI:
    """AI-powered natural language command generator"""
    
    def __init__(self, tools_db: Dict, config_dir: Path):
        self.tools_db = tools_db
        self.config_dir = config_dir
        self.ollama_url = "http://localhost:11434"
        self.model = "codellama"  # Default model, can be changed
        self.context = {
            "last_target": None,
            "last_tool": None,
            "conversation_history": []
        }
        self.ai_config_file = config_dir / "ai_config.json"
        self._load_ai_config()
    
    def _load_ai_config(self):
        """Load AI configuration"""
        if self.ai_config_file.exists():
            with open(self.ai_config_file, 'r') as f:
                config = json.load(f)
                self.model = config.get("model", "codellama")
        else:
            self._save_ai_config()
    
    def _save_ai_config(self):
        """Save AI configuration"""
        config = {"model": self.model}
        with open(self.ai_config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def is_ollama_available(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def is_model_available(self) -> bool:
        """Check if the configured model is downloaded"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return any(self.model in model.get('name', '') for model in models)
            return False
        except:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available Ollama models"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [model.get('name', '').split(':')[0] for model in models]
            return []
        except:
            return []
    
    def set_model(self, model_name: str) -> bool:
        """Set the AI model to use"""
        self.model = model_name
        self._save_ai_config()
        return True
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with tool database knowledge"""
        tools_info = []
        for tool_name, tool_data in list(self.tools_db.items())[:50]:  # Limit to avoid token overflow
            tools_info.append(f"- {tool_name}: {tool_data.get('description', '')}")
        
        tools_list = "\n".join(tools_info)
        
        return f"""You are a cybersecurity command-line expert assistant for Kali Linux.
Your job is to convert natural language requests into precise command-line commands.

Available tools in the database:
{tools_list}

Rules:
1. Generate ONLY the command, no explanations
2. Use proper syntax and flags
3. If target is not specified but was mentioned before, use context
4. Use common Kali Linux paths (e.g., /usr/share/wordlists/)
5. Be precise and security-focused
6. If request is unclear, ask for clarification with "CLARIFY: <question>"

Context from conversation:
- Last target: {self.context.get('last_target', 'none')}
- Last tool: {self.context.get('last_tool', 'none')}

Respond with just the command or CLARIFY if you need more information."""
    
    def _extract_target_from_request(self, request: str) -> Optional[str]:
        """Extract target (IP, domain, URL) from natural language request"""
        import re
        
        # IP address pattern
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ip_match = re.search(ip_pattern, request)
        if ip_match:
            return ip_match.group(0)
        
        # Domain pattern
        domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
        domain_match = re.search(domain_pattern, request)
        if domain_match:
            return domain_match.group(0)
        
        # URL pattern
        url_pattern = r'https?://[^\s]+'
        url_match = re.search(url_pattern, request)
        if url_match:
            return url_match.group(0)
        
        return None
    
    def generate_command(self, natural_language_request: str) -> Tuple[bool, str]:
        """
        Generate command from natural language request
        
        Returns:
            (success, command_or_error_message)
        """
        # Extract and update target if present
        target = self._extract_target_from_request(natural_language_request)
        if target:
            self.context['last_target'] = target
        
        # Build the prompt
        system_prompt = self._build_system_prompt()
        user_prompt = f"User request: {natural_language_request}"
        
        # Add conversation history for context
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            # Call Ollama API
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,  # Lower temperature for more consistent outputs
                        "top_p": 0.9
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                command = result.get('message', {}).get('content', '').strip()
                
                # Check if AI needs clarification
                if command.startswith("CLARIFY:"):
                    return (False, command.replace("CLARIFY:", "").strip())
                
                # Update context with extracted tool
                for tool_name in self.tools_db.keys():
                    if tool_name in command.lower():
                        self.context['last_tool'] = tool_name
                        break
                
                # Store in conversation history
                self.context['conversation_history'].append({
                    "request": natural_language_request,
                    "command": command
                })
                
                return (True, command)
            else:
                return (False, f"API Error: {response.status_code}")
        
        except requests.exceptions.Timeout:
            return (False, "Request timeout. Model might be loading or Ollama is slow.")
        except requests.exceptions.ConnectionError:
            return (False, "Cannot connect to Ollama. Is it running?")
        except Exception as e:
            return (False, f"Error: {str(e)}")
    
    def clear_context(self):
        """Clear conversation context"""
        self.context = {
            "last_target": None,
            "last_tool": None,
            "conversation_history": []
        }
    
    def show_context(self) -> str:
        """Show current context"""
        return f"""Current AI Context:
- Last Target: {self.context.get('last_target', 'None')}
- Last Tool: {self.context.get('last_tool', 'None')}
- Conversation History: {len(self.context.get('conversation_history', []))} entries
"""
    
    def install_instructions(self) -> str:
        """Return Ollama installation instructions for Kali Linux"""
        return """
╔═══════════════════════════════════════════════════════════════╗
║              Ollama AI Setup Instructions                     ║
╚═══════════════════════════════════════════════════════════════╝

AI features require Ollama to be installed and running.

Installation Steps:
─────────────────────────────────────────────────────────────────

1. Install Ollama:
   curl -fsSL https://ollama.com/install.sh | sh

2. Start Ollama (if not auto-started):
   ollama serve

3. Download a model (choose one):
   
   Recommended for speed:
   ollama pull codellama:7b        (~3.8 GB)
   
   For better accuracy:
   ollama pull llama3              (~4.7 GB)
   ollama pull codellama:13b       (~7.4 GB)
   
   Lightweight option:
   ollama pull phi                 (~1.6 GB)

4. Test installation:
   ollama list

5. Configure Toolbox (optional):
   toolbox> ai-config

That's it! Now you can use natural language commands:
   toolbox> ai scan this website for vulnerabilities
   toolbox> ai find subdomains of example.com
   toolbox> ai brute force SSH on 192.168.1.100

─────────────────────────────────────────────────────────────────
Documentation: https://ollama.com/
Support: https://github.com/ollama/ollama
"""


class AICommandValidator:
    """Validates AI-generated commands for safety"""
    
    # Commands that should always be confirmed
    DANGEROUS_PATTERNS = [
        r'rm\s+-rf',
        r'mkfs',
        r'dd\s+if=',
        r':\(\)\{.*\}',  # Fork bomb
        r'chmod\s+-R\s+777',
        r'shutdown',
        r'reboot',
        r'init\s+0',
        r'init\s+6',
    ]
    
    @staticmethod
    def is_safe(command: str) -> Tuple[bool, Optional[str]]:
        """
        Check if command is safe to execute
        
        Returns:
            (is_safe, warning_message)
        """
        import re
        
        for pattern in AICommandValidator.DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return (False, f"⚠️  DANGEROUS: Command contains potentially harmful pattern: {pattern}")
        
        return (True, None)
    
    @staticmethod
    def requires_root(command: str) -> bool:
        """Check if command likely requires root privileges"""
        root_tools = ['nmap', 'masscan', 'aircrack-ng', 'airmon-ng', 'wireshark']
        command_lower = command.lower()
        
        # Check for sudo
        if command.startswith('sudo'):
            return True
        
        # Check for tools that typically need root
        for tool in root_tools:
            if tool in command_lower:
                # Some nmap scans don't need root
                if tool == 'nmap' and '-sT' in command:
                    return False
                return True
        
        return False
