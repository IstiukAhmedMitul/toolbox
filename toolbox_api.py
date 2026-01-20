#!/usr/bin/env python3
"""
Toolbox API Server
A simple REST API for Toolbox - allows remote command execution via HTTP

Usage:
    python3 toolbox_api.py [--port 5000] [--host 0.0.0.0]

WARNING: This API has no authentication. Use only in trusted networks!
For production, add authentication, HTTPS, and rate limiting.
"""

import sys
import json
import argparse
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import toolbox
sys.path.insert(0, str(Path(__file__).parent))
from toolbox import Toolbox

app = Flask(__name__)
CORS(app)  # Enable CORS for web interface

toolbox = Toolbox()

@app.route('/')
def index():
    """API information"""
    return jsonify({
        "name": "Toolbox API",
        "version": "2.0",
        "endpoints": {
            "/api/tools": "GET - List all tools",
            "/api/tools/<name>": "GET - Get tool information",
            "/api/search": "GET - Search tools (query parameter)",
            "/api/categories": "GET - List all categories",
            "/api/category/<name>": "GET - Get tools in category",
            "/api/execute": "POST - Execute a command",
            "/api/history": "GET - Get command history",
            "/api/favorites": "GET - Get favorites",
            "/api/templates": "GET - Get templates",
            "/api/workflows": "GET - Get workflows"
        }
    })

@app.route('/api/tools', methods=['GET'])
def list_tools():
    """List all available tools"""
    tools = {}
    for name, info in toolbox.tools_db.items():
        tools[name] = {
            "description": info["description"],
            "requires_target": info["requires_target"],
            "requires_wordlist": info["requires_wordlist"],
            "commands_count": len(info["commands"])
        }
    return jsonify(tools)

@app.route('/api/tools/<name>', methods=['GET'])
def get_tool(name):
    """Get detailed information about a specific tool"""
    tool_info = toolbox.get_tool_info(name)
    if tool_info:
        return jsonify(tool_info)
    return jsonify({"error": "Tool not found"}), 404

@app.route('/api/search', methods=['GET'])
def search_tools():
    """Search tools by query"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Query parameter 'q' required"}), 400
    
    results = toolbox.search_by_category(query)
    return jsonify(results)

@app.route('/api/categories', methods=['GET'])
def list_categories():
    """List all tool categories"""
    return jsonify(toolbox.tool_categories)

@app.route('/api/category/<name>', methods=['GET'])
def get_category(name):
    """Get tools in a specific category"""
    tools = toolbox.get_category_tools(name)
    if tools:
        return jsonify({"category": name, "tools": tools})
    return jsonify({"error": "Category not found"}), 404

@app.route('/api/execute', methods=['POST'])
def execute_command():
    """Execute a command (USE WITH CAUTION!)"""
    data = request.get_json()
    
    if not data or 'command' not in data:
        return jsonify({"error": "Command required in JSON body"}), 400
    
    command = data['command']
    tool = data.get('tool', 'unknown')
    target = data.get('target', '')
    
    try:
        import subprocess
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Save to history
        toolbox.add_to_history(tool, command, target)
        
        return jsonify({
            "success": True,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Command timed out"}), 408
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get command history"""
    try:
        history = json.loads(toolbox.history_file.read_text())
        limit = request.args.get('limit', 50, type=int)
        return jsonify(history[-limit:])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/favorites', methods=['GET', 'POST'])
def favorites():
    """Get or add favorites"""
    if request.method == 'GET':
        try:
            favorites = json.loads(toolbox.favorites_file.read_text())
            return jsonify(favorites)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'tool' not in data or 'command' not in data:
            return jsonify({"error": "tool and command required"}), 400
        
        toolbox.add_to_favorites(
            data['tool'],
            data['command'],
            data.get('name', '')
        )
        return jsonify({"success": True})

@app.route('/api/templates', methods=['GET', 'POST'])
def templates():
    """Get or add templates"""
    if request.method == 'GET':
        try:
            templates = json.loads(toolbox.templates_file.read_text())
            return jsonify(templates)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    elif request.method == 'POST':
        data = request.get_json()
        if not data or 'name' not in data or 'command' not in data:
            return jsonify({"error": "name and command required"}), 400
        
        toolbox.save_template(
            data['name'],
            data['command'],
            data.get('description', '')
        )
        return jsonify({"success": True})

@app.route('/api/workflows', methods=['GET'])
def workflows():
    """Get workflows"""
    try:
        workflows = json.loads(toolbox.workflows_file.read_text())
        return jsonify(workflows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/doctor', methods=['GET'])
def doctor():
    """Check tool availability"""
    import shutil
    available = []
    missing = []
    
    for tool in toolbox.tools_db.keys():
        if shutil.which(tool) or shutil.which(tool.replace("-", "_")):
            available.append(tool)
        else:
            missing.append(tool)
    
    return jsonify({
        "available": available,
        "missing": missing,
        "total": len(toolbox.tools_db),
        "available_count": len(available),
        "missing_count": len(missing)
    })

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Toolbox API Server')
    parser.add_argument('--port', type=int, default=5000, help='Port to run on')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to (use 0.0.0.0 for all interfaces)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    print(f"""
╔══════════════════════════════════════════╗
║      Toolbox API Server v2.0             ║
╚══════════════════════════════════════════╝

⚠️  WARNING: This API has NO authentication!
   Use only in trusted networks!

Server: http://{args.host}:{args.port}
API Docs: http://{args.host}:{args.port}/

Press Ctrl+C to stop
""")
    
    try:
        app.run(host=args.host, port=args.port, debug=args.debug)
    except ImportError:
        print("\n[!] Flask is not installed!")
        print("[+] Install with: pip3 install flask flask-cors")
        sys.exit(1)
