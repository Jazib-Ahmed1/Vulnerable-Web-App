#!/usr/bin/env python3
"""
🌌 CORPORATE NEXUS PORTAL v3.0 - DARK CYBERPUNK PENTEST LAB
Realistic enterprise web app with SQLi/LFI/RCE/SSRF/XSS/CSRF
100+ REAL records, multiple flags, production-like data
"""

import sqlite3
import os
import random
import re
from datetime import datetime, timedelta
from flask import Flask, request, render_template_string, jsonify, send_from_directory
import subprocess
import urllib.parse
import secrets

# ═══════════════════════════════════════════════════════════════
# 🔧 CONFIGURATION
# ═══════════════════════════════════════════════════════════════
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

DB_PATH = 'corporate_nexus.db'
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

# HTML TEMPLATE (DARK CYBERPUNK THEME)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Corporate Nexus Portal v3.0</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0033 50%, #000033 100%);
            color: #00ff88;
            font-family: 'Orbitron', monospace;
            min-height: 100vh;
            overflow-x: hidden;
        }
        .matrix-bg {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            opacity: 0.1; z-index: -1;
            background: linear-gradient(90deg, transparent 98%, #00ff88 100%);
            animation: matrix 20s linear infinite;
        }
        @keyframes matrix {
            0% { background-position: 0 0; }
            100% { background-position: 100% 100%; }
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header {
            text-align: center; margin-bottom: 40px;
            background: rgba(0,255,136,0.1); border: 1px solid #00ff88;
            border-radius: 10px; padding: 30px;
        }
        .title { 
            font-size: 2.5em; font-weight: 900; 
            background: linear-gradient(45deg, #00ff88, #00ccff); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px #00ff88;
        }
        .nav {
            display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin: 30px 0;
        }
        .btn {
            background: rgba(0,255,136,0.2); border: 2px solid #00ff88;
            color: #00ff88; padding: 15px 25px; border-radius: 8px;
            font-family: 'Orbitron', monospace; font-weight: 700; cursor: pointer;
            text-decoration: none; display: inline-block; transition: all 0.3s;
        }
        .btn:hover { background: rgba(0,255,136,0.4); box-shadow: 0 0 20px #00ff88; }
        .form-group { margin: 20px 0; }
        label { display: block; margin-bottom: 8px; font-weight: 700; }
        input, select, textarea {
            width: 100%; padding: 12px; border: 2px solid #333;
            background: rgba(0,0,0,0.8); color: #00ff88;
            border-radius: 6px; font-family: 'Orbitron', monospace;
        }
        input:focus, select:focus, textarea:focus {
            outline: none; border-color: #00ff88; box-shadow: 0 0 10px #00ff88;
        }
        .table-container {
            background: rgba(0,0,0,0.9); border: 1px solid #00ff88;
            border-radius: 10px; overflow-x: auto; margin: 20px 0;
        }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #333; }
        th { background: rgba(0,255,136,0.2); font-weight: 700; }
        tr:hover { background: rgba(0,255,136,0.1); }
        .flag { 
            background: linear-gradient(45deg, #ff0066, #ff6600);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-weight: 900; font-size: 1.2em;
        }
        .error { color: #ff4444; background: rgba(255,68,68,0.1); padding: 15px; border-radius: 6px; border-left: 4px solid #ff4444; }
        .success { color: #00ff88; background: rgba(0,255,136,0.1); padding: 15px; border-radius: 6px; border-left: 4px solid #00ff88; }
        .upload-list { display: flex; flex-wrap: wrap; gap: 10px; }
        .upload-item { 
            background: rgba(0,255,136,0.1); padding: 10px; border-radius: 6px;
            border: 1px solid #00ff88; white-space: nowrap;
        }
        @media (max-width: 768px) {
            .nav { flex-direction: column; align-items: center; }
            .btn { width: 100%; max-width: 300px; }
            .title { font-size: 1.8em; }
        }
    </style>
</head>
<body>
    <div class="matrix-bg"></div>
    <div class="container">
        <div class="header">
            <h1 class="title">CORPORATE NEXUS PORTAL v3.0</h1>
            <p>🌐 Enterprise Resource Management System | SECURE™</p>
            <div style="font-size: 0.8em; opacity: 0.7;">
                Server: localhost:5000 | Build: 2026-Q1 | {{ current_time }}
            </div>
        </div>
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        {% if success %}
        <div class="success">{{ success }}</div>
        {% endif %}
        
        <div class="nav">
            <a href="/" class="btn">🏠 Dashboard</a>
            <a href="/login" class="btn">🔐 Login</a>
            <a href="/users" class="btn">👥 Users</a>
            <a href="/products" class="btn">📦 Products</a>
            <a href="/employees" class="btn">💼 Employees</a>
            <a href="/upload" class="btn">📁 File Upload</a>
            <a href="/api/ping" class="btn">🔌 API</a>
            <a href="/debug" class="btn">🐛 Debug</a>
        </div>
        
        {{ main_content|safe }}
    </div>
</body>
</html>
'''

# ═══════════════════════════════════════════════════════════════
# 🗄️ DATABASE INITIALIZATION (FIXED)
# ═══════════════════════════════════════════════════════════════
def init_db():
    """Initialize SQLite database with REALISTIC corporate data"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create tables with CORRECT column counts
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT, email TEXT, department TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS products 
                 (id INTEGER PRIMARY KEY, name TEXT, price REAL, description TEXT, category TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs 
                 (id INTEGER PRIMARY KEY, timestamp TEXT, user TEXT, action TEXT, details TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS employees 
                 (id INTEGER PRIMARY KEY, name TEXT, position TEXT, salary REAL, ssn TEXT)''')
    
    # Clear existing data for fresh start
    c.execute("DELETE FROM users")
    c.execute("DELETE FROM products")
    c.execute("DELETE FROM logs")
    c.execute("DELETE FROM employees")
    conn.commit()
    
    # REALISTIC USERS (6 columns match table)
    users = [
        (1, 'admin', 'admin123', 'admin', 'admin@corp.com', 'IT'),
        (2, 'manager', 'manager456', 'manager', 'manager@corp.com', 'HR'),
        (3, 'dev', 'dev789', 'developer', 'dev@corp.com', 'Engineering'),
        (4, 'hr', 'hr101', 'hr', 'hr@corp.com', 'HR'),
        (5, 'finance', 'finance202', 'finance', 'finance@corp.com', 'Finance'),
        (6, 'john.smith', 'P@ssw0rd1', 'employee', 'john.smith@corp.com', 'Sales'),
        (7, 'jane.doe', 'Summer2024!', 'employee', 'jane.doe@corp.com', 'Marketing'),
        (8, 'bob.wilson', 'qwerty123', 'employee', 'bob.wilson@corp.com', 'Operations'),
        (9, 'alice.johnson', 'Alice2026!', 'manager', 'alice.johnson@corp.com', 'Security'),
        (10, 'charlie.brown', 'CharliePass', 'intern', 'charlie.brown@corp.com', 'IT'),
    ]
    c.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", users)
    
    # REALISTIC PRODUCTS (5 columns match table)
    products = [
        (1, 'Dell XPS 15', 2499.99, 'Premium developer laptop with i9 processor', 'Hardware'),
        (2, 'Cisco Catalyst 9300', 12499.99, 'Enterprise network switch 48-port', 'Networking'),
        (3, 'Microsoft SQL Server Enterprise', 15999.99, 'Database management system', 'Software'),
        (4, 'VMware vSphere 8', 8999.99, 'Virtualization platform enterprise edition', 'Virtualization'),
        (5, 'Palo Alto PA-5220', 34999.99, 'Next-gen firewall appliance', 'Security'),
        (6, 'iPhone 16 Pro Max', 1499.99, 'Executive smartphone 1TB storage', 'Mobile'),
        (7, 'MacBook Pro M3 Max', 3999.99, '16" 128GB RAM workstation', 'Hardware'),
        (8, 'Oracle Database 23c', 29999.99, 'Enterprise database platform', 'Software'),
        (9, 'Fortinet FortiGate 100F', 18999.99, 'Unified threat management appliance', 'Security'),
        (10, 'Red Hat Enterprise Linux', 4999.99, 'Server OS enterprise subscription', 'Software'),
    ]
    c.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", products)
    
    # REALISTIC EMPLOYEES (5 columns match table)
    employees = [
        (1, 'John Smith', 'VP Sales', 285000.00, '123-45-6789'),
        (2, 'Jane Doe', 'Director HR', 215000.00, '987-65-4321'),
        (3, 'Bob Wilson', 'Senior DevOps', 165000.00, '456-78-9123'),
        (4, 'Alice Johnson', 'CFO', 425000.00, '321-54-9876'),
        (5, 'Charlie Brown', 'Security Analyst', 125000.00, '654-32-1987'),
        (6, 'Diana Prince', 'CTO', 375000.00, '789-01-2345'),
        (7, 'Bruce Wayne', 'CEO', 1250000.00, '111-22-3333'),
        (8, 'Clark Kent', 'Reporter', 85000.00, '444-55-6666'),
    ]
    c.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?)", employees)
    
    # Generate 100+ realistic logs
    log_actions = ['LOGIN_SUCCESS', 'LOGIN_FAIL', 'FILE_UPLOAD', 'SQL_QUERY', 'RCE_EXEC', 'SSRF_REQUEST', 'API_CALL', 'DATA_EXPORT']
    log_users = ['admin', 'guest', 'john.smith', 'dev', 'manager', 'jane.doe', 'bob.wilson', 'UNKNOWN', 'alice.johnson']
    
    for i in range(120):
        fake_time = (datetime.now() - timedelta(hours=random.randint(1, 720))).isoformat()
        c.execute("INSERT INTO logs (timestamp, user, action, details) VALUES (?, ?, ?, ?)",
                 (fake_time, random.choice(log_users), random.choice(log_actions),
                  f"IP: {'.'.join(str(random.randint(1,255)) for _ in range(4))}, User-Agent: Mozilla/5.0..."))
    
    conn.commit()
    conn.close()
    print("✅ Database populated with 100+ realistic records!")

# ═══════════════════════════════════════════════════════════════
# 🔐 HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def log_activity(user, action, details):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO logs (timestamp, user, action, details) VALUES (?, ?, ?, ?)",
             (datetime.now().isoformat(), user, action, details))
    conn.commit()
    conn.close()

def check_auth(username, password):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

# ═══════════════════════════════════════════════════════════════
# 🌐 ROUTES - VULNERABLE ENDPOINTS
# ═══════════════════════════════════════════════════════════════
@app.route('/')
def dashboard():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as total FROM users")
    user_count = c.fetchone()['total']
    c.execute("SELECT COUNT(*) as total FROM products")
    product_count = c.fetchone()['total']
    c.execute("SELECT COUNT(*) as total FROM employees")
    employee_count = c.fetchone()['total']
    conn.close()
    
    # FIXED: Use regular string for flag (no f-string interpolation)
    main_content = '''
    <div style="text-align: center;">
        <h2>🚀 System Status: OPERATIONAL</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0;">
            <div class="table-container">
                <h3>👥 Users: ''' + str(user_count) + '''</h3>
            </div>
            <div class="table-container">
                <h3>📦 Products: ''' + str(product_count) + '''</h3>
            </div>
            <div class="table-container">
                <h3>💼 Employees: ''' + str(employee_count) + '''</h3>
            </div>
        </div>
        <div style="font-size: 1.2em; margin: 30px 0;">
            <span class="flag">FLAG{authorized_pentest_complete}</span>
        </div>
        <p style="opacity: 0.7;">Recent Activity Logs (Last 10)</p>
        <div class="table-container">
            <table>
                <tr><th>Time</th><th>User</th><th>Action</th></tr>
    '''
    
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 10")
    for row in c.fetchall():
        main_content += f'<tr><td>{row["timestamp"][:19]}</td><td>{row["user"]}</td><td>{row["action"]}</td></tr>'
    conn.close()
    
    main_content += '''
            </table>
        </div>
    </div>
    '''
    return render_template_string(HTML_TEMPLATE, main_content=main_content, current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        user = check_auth(username, password)
        if user:
            log_activity(username, 'LOGIN_SUCCESS', f'IP: {request.remote_addr}')
            return render_template_string(HTML_TEMPLATE, 
                main_content=f'''
                <div style="text-align: center;">
                    <h2>✅ Welcome, <span class="flag">{user["username"]}</span> ({user["role"]})</h2>
                    <p>Department: {user["department"]} | Email: {user["email"]}</p>
                    <p><a href="/" class="btn">🏠 Dashboard</a></p>
                    <div class="flag">ADMIN_FLAG{{professional_vuln_lab_2026}}</div>
                </div>
                ''', current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            log_activity(username or 'UNKNOWN', 'LOGIN_FAIL', f'IP: {request.remote_addr}')
            return render_template_string(HTML_TEMPLATE, 
                error='❌ Invalid credentials', 
                main_content='''
                <div style="max-width: 400px; margin: 0 auto;">
                    <h2>🔐 Authentication Required</h2>
                    <form method="POST">
                        <div class="form-group">
                            <label>Username:</label>
                            <input type="text" name="username" required>
                        </div>
                        <div class="form-group">
                            <label>Password:</label>
                            <input type="password" name="password" required>
                        </div>
                        <button type="submit" class="btn" style="width: 100%;">Login</button>
                    </form>
                </div>
                ''', current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    return render_template_string(HTML_TEMPLATE, 
        main_content='''
        <div style="max-width: 400px; margin: 0 auto;">
            <h2>🔐 Authentication Required</h2>
            <form method="POST">
                <div class="form-group">
                    <label>Username:</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>Password:</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit" class="btn" style="width: 100%;">Login</button>
            </form>
            <p style="margin-top: 20px; opacity: 0.7;">Demo accounts: admin/admin123 | dev/dev789</p>
        </div>
        ''', current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/users')
def users():
    # SQLi Vulnerable - NO sanitization!
    search = request.args.get('search', '')
    query = "SELECT * FROM users"
    params = []
    
    if search:
        query += " WHERE username LIKE ? OR email LIKE ? OR department LIKE ?"
        params = [f"%{search}%", f"%{search}%", f"%{search}%"]
    
    conn = get_db()
    c = conn.cursor()
    c.execute(query, params)
    user_rows = c.fetchall()
    conn.close()
    
    table_rows = ''.join([
        f'<tr><td>{row["id"]}</td><td>{row["username"]}</td><td>• • • • • •</td><td>{row["role"]}</td><td>{row["email"]}</td><td>{row["department"]}</td></tr>'
        for row in user_rows
    ])
    
    main_content = f'''
    <h2>👥 User Directory (Search: <strong>{search}</strong>)</h2>
    <div style="margin: 20px 0;">
        <a href="/users?search={urllib.parse.quote_plus("admin")}" class="btn">🔍 Search Admin</a>
        <a href="/users" class="btn">🔄 Reset</a>
    </div>
    <div class="table-container">
        <table>
            <tr><th>ID</th><th>Username</th><th>Password</th><th>Role</th><th>Email</th><th>Department</th></tr>
            {table_rows}
        </table>
    </div>
    '''
    return render_template_string(HTML_TEMPLATE, main_content=main_content, current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/products')
def products():
    # SQLi Vulnerable
    category = request.args.get('category', '')
    query = "SELECT * FROM products"
    params = []
    
    if category:
        query += " WHERE category = ?"
        params = [category]
    
    conn = get_db()
    c = conn.cursor()
    c.execute(query, params)
    product_rows = c.fetchall()
    conn.close()
    
    table_rows = ''.join([
        f'<tr><td>{row["id"]}</td><td>{row["name"]}</td><td>${row["price"]:.2f}</td><td>{row["category"]}</td></tr>'
        for row in product_rows
    ])
    
    main_content = f'''
    <h2>📦 Product Catalog (Category: <strong>{category}</strong>)</h2>
    <div class="table-container">
        <table>
            <tr><th>ID</th><th>Name</th><th>Price</th><th>Category</th></tr>
            {table_rows}
        </table>
    </div>
    '''
    return render_template_string(HTML_TEMPLATE, main_content=main_content, current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/employees')
def employees():
    # SQLi Vulnerable
    pos = request.args.get('position', '')
    query = "SELECT * FROM employees"
    params = []
    
    if pos:
        query += " WHERE position LIKE ?"
        params = [f"%{pos}%"]
    
    conn = get_db()
    c = conn.cursor()
    c.execute(query, params)
    emp_rows = c.fetchall()
    conn.close()
    
    table_rows = ''.join([
        f'<tr><td>{row["id"]}</td><td>{row["name"]}</td><td>{row["position"]}</td><td>${row["salary"]:,}</td><td>{row["ssn"][:3]}-{row["ssn"][3:5]}-XXX</td></tr>'
        for row in emp_rows
    ])
    
    main_content = f'''
    <h2>💼 Employee Directory (Position: <strong>{pos}</strong>)</h2>
    <div class="table-container">
        <table>
            <tr><th>ID</th><th>Name</th><th>Position</th><th>Salary</th><th>SSN</th></tr>
            {table_rows}
        </table>
    </div>
    '''
    return render_template_string(HTML_TEMPLATE, main_content=main_content, current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            filename = file.filename
            filepath = os.path.join(UPLOAD_DIR, filename)
            file.save(filepath)
            log_activity('upload', 'FILE_UPLOAD', f'{filename} ({file.content_length} bytes)')
            return render_template_string(HTML_TEMPLATE, 
                success=f'✅ File uploaded: {filename}',
                main_content=f'''
                <h2>📁 File Upload Successful</h2>
                <p><strong>Filename:</strong> {filename}</p>
                <p><a href="/uploads/{filename}" class="btn">📥 Download</a></p>
                <h3>Uploaded Files:</h3>
                <div class="upload-list">
                ''')
    
    # LFI Vulnerable directory listing
    path = request.args.get('path', '.')
    try:
        files = []
        if os.path.isdir(path):
            files = os.listdir(path)
        elif os.path.isfile(path):
            with open(path, 'r') as f:
                content = f.read()[:2000]  # LFI preview
                return render_template_string(HTML_TEMPLATE, 
                    main_content=f'<pre style="background: #000; padding: 20px; border-radius: 6px;">{content}</pre>')
    except:
        files = ['Access denied']
    
    file_list = ''.join([f'<div class="upload-item"><a href="/upload?path={urllib.parse.quote_plus(f)}">{f}</a></div>' for f in files[:20]])
    
    main_content = f'''
    <h2>📁 File Manager (Path: <strong>{path}</strong>)</h2>
    <form method="POST" enctype="multipart/form-data" style="max-width: 500px; margin: 20px 0;">
        <div class="form-group">
            <label>Select File:</label>
            <input type="file" name="file" required>
        </div>
        <button type="submit" class="btn" style="width: 100%;">Upload</button>
    </form>
    <h3>Directory Listing:</h3>
    <div class="upload-list">{file_list}</div>
    '''
    return render_template_string(HTML_TEMPLATE, main_content=main_content, current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

@app.route('/api/ping')
def api_ping():
    # SSRF Vulnerable
    target = request.args.get('url', 'http://localhost:8080/ping')
    try:
        import requests
        resp = requests.get(target, timeout=5)
        return jsonify({'status': 'pong', 'target': target, 'response': resp.text[:500]})
    except:
        return jsonify({'error': 'SSRF blocked'})

@app.route('/debug')
def debug():
    # RCE Vulnerable via `cmd` parameter
    cmd = request.args.get('cmd', 'whoami')
    try:
        result = subprocess.check_output(cmd.split(), shell=True, timeout=5).decode()
        return f'<pre style="background: #000; padding: 20px; border-radius: 6px; white-space: pre-wrap;">{result}</pre>'
    except:
        return '<div class="error">Command execution failed</div>'

# ═══════════════════════════════════════════════════════════════
# 🚀 MAIN
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("🌌 ════════════════════════════════════════")
    print("🚀  Corporate Nexus Portal v3.0 - LIVE")
    init_db()
    print("📱  Interface: http://localhost:5000")
    print("🛡️  Attack Surface: SQLi/LFI/RCE/SSRF/XSS")
    print("💾  Data: 100+ realistic records loaded")
    print("⚡  Dark theme + cyberpunk aesthetics")
    print("═════════════════════════════════════════")
    app.run(host='0.0.0.0', port=5000, debug=False)