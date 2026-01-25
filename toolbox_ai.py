#!/usr/bin/env python3
"""
Toolbox AI Module - Natural Language Command Generation
Uses Groq API for fast, free AI-powered command generation

Features:
- Natural language to command translation
- Context-aware conversations
- Tool database integration
- Fast inference with Groq
"""

import json
import requests
from typing import Optional, Dict, List, Tuple
from pathlib import Path
import re


class ToolboxAI:
    """AI-powered natural language command generator using Groq"""
    
    def __init__(self, tools_db: Dict, config_dir: Path):
        self.tools_db = tools_db
        self.config_dir = config_dir
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"  # Fast and accurate
        self.api_key = None
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
                self.model = config.get("model", "llama-3.1-8b-instant")
                self.api_key = config.get("groq_api_key")
        else:
            self._save_ai_config()
    
    def _save_ai_config(self):
        """Save AI configuration"""
        config = {
            "provider": "groq",
            "model": self.model,
            "groq_api_key": self.api_key
        }
        with open(self.ai_config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def is_groq_available(self) -> bool:
        """Check if Groq API key is configured"""
        return self.api_key is not None and len(self.api_key) > 0
    
    def set_api_key(self, api_key: str):
        """Set Groq API key"""
        self.api_key = api_key
        self._save_ai_config()
    
    def get_available_models(self) -> List[str]:
        """Get list of available Groq models"""
        return [
            "llama-3.1-8b-instant",      # Fast, recommended
            "llama-3.3-70b-versatile",   # Most capable
            "mixtral-8x7b-32768",         # Large context
            "gemma2-9b-it"                # Efficient
        ]
    
    def set_model(self, model_name: str) -> bool:
        """Set the AI model to use"""
        self.model = model_name
        self._save_ai_config()
        return True
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with tool database knowledge"""
        tools_info = []
        for tool_name, tool_data in list(self.tools_db.items())[:50]:
            tools_info.append(f"- {tool_name}: {tool_data.get('description', '')}")
        
        tools_list = "\n".join(tools_info)
        
        return f"""You are a cybersecurity command-line expert for Kali Linux 2026.
Convert natural language requests into precise command-line commands.

Available tools:
{tools_list}

CRITICAL RULES:
1. Return ONLY the executable command
2. NO labels, explanations, or extra text
3. NO prefixes like "Command:", "You:", etc.
4. Just the raw command that can be executed directly
5. Use ONLY widely-compatible flags that work across tool versions
6. Use common Kali Linux paths: /usr/share/wordlists/
7. If unclear, respond with: CLARIFY: <question>
8. Prefer simple, tested flags over advanced ones

COMMON TOOL SYNTAX (use these exactly):
- nmap: Use -sV, -p-, -A, -sS, -sU, -T4, -Pn
- gobuster: Use dir -u URL -w WORDLIST -t 50
- hydra: Use -l USER -P WORDLIST protocol://TARGET
- smbmap: Use -H HOST -u USER (avoid -R, use -r for recursion)
- nikto: Use -h TARGET -p PORT
- sqlmap: Use -u URL --dbs --tables --dump
- dirb: Use URL WORDLIST
- enum4linux: Use -a TARGET
- metasploit: Use msfconsole commands

Examples:
Request: scan 192.168.1.1
Response: nmap -sV 192.168.1.1

Request: find directories on http://example.com
Response: gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt

Request: brute force SSH on 10.0.0.5
Response: hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://10.0.0.5

Request: list SMB users on 192.168.1.1
Response: enum4linux -U 192.168.1.1

Request: enumerate SMB shares on 192.168.1.1
Response: smbmap -H 192.168.1.1 -u guest

Context:
- Last target: {self.context.get('last_target', 'none')}
- Last tool: {self.context.get('last_tool', 'none')}"""
    
    def _extract_target_from_request(self, request: str) -> Optional[str]:
        """Extract target (IP, domain, URL) from natural language request"""
        # IP address pattern
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ip_match = re.search(ip_pattern, request)
        if ip_match:
            return ip_match.group(0)
        
        # Domain pattern
        domain_pattern = r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]\b'
        domain_match = re.search(domain_pattern, request, re.IGNORECASE)
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
        if not self.is_groq_available():
            return (False, "Groq API key not configured. Run 'ai-config' to set it up.")
        
        # Extract and update target if present
        target = self._extract_target_from_request(natural_language_request)
        if target:
            self.context['last_target'] = target
        
        # Build the prompt
        system_prompt = self._build_system_prompt()
        user_prompt = f"{natural_language_request}"
        
        # Build messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            # Call Groq API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.groq_url,
                headers=headers,
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                command = result['choices'][0]['message']['content'].strip()
                
                # Check if AI needs clarification
                if command.startswith("CLARIFY:"):
                    return (False, command.replace("CLARIFY:", "").strip())
                
                # Clean up the command
                command = self._clean_command(command)
                
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
            
            elif response.status_code == 401:
                return (False, "Invalid Groq API key. Run 'ai-config' to update it.")
            elif response.status_code == 429:
                return (False, "Rate limit exceeded. Wait a moment and try again.")
            else:
                return (False, f"Groq API Error: {response.status_code} - {response.text}")
        
        except requests.exceptions.Timeout:
            return (False, "Request timeout. Check your internet connection.")
        except requests.exceptions.ConnectionError:
            return (False, "Cannot connect to Groq API. Check your internet connection.")
        except Exception as e:
            return (False, f"Error: {str(e)}")
    
    def _clean_command(self, command: str) -> str:
        """Clean up AI-generated command"""
        # Remove common prefixes
        prefixes = ["Command:", "You:", "Assistant:", "Output:", "$", "#", ">"]
        for prefix in prefixes:
            if command.startswith(prefix):
                command = command[len(prefix):].strip()
        
        # Remove explanation sections
        if "Explanation:" in command:
            command = command.split("Explanation:")[0].strip()
        
        # Take first line only (the actual command)
        command = command.split('\n')[0].strip()
        
        # Remove markdown code blocks
        command = command.replace('```bash', '').replace('```', '').strip()
        
        # Clean up extra whitespace
        command = ' '.join(command.split())
        
        return command
    
    def clear_context(self):
        """Clear conversation context"""
        self.context['last_target'] = None
        self.context['last_tool'] = None
        self.context['conversation_history'] = []
    
    def get_status(self) -> Dict:
        """Get current AI status"""
        return {
            "provider": "Groq",
            "api_configured": self.is_groq_available(),
            "model": self.model,
            "context": self.context
        }
