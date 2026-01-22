````markdown
 🌌 Corporate Nexus Portal v3.0 Vulnerable Pentest Lab

![Vulnerable](https://img.shields.io/badge/status-intentionally_vulnerable-red)
![Flask](https://img.shields.io/badge/flask-3.x-blue)
![CTF](https://img.shields.io/badge/use-CTF%20%7C%20Pentest%20Training-purple)

⚠️ WARNING: THIS APPLICATION IS INTENTIONALLY VULNERABLE

This project is a deliberately insecure Flask web application created for:

- 🧪 Web application penetration testing practice  
- 🏴 Capture The Flag (CTF) challenges  
- 🛡️ Secure coding education  
- 🔴 Red team / blue team training  
- 🐞 Bug bounty skill development  

❌ DO NOT deploy this application to production**  
❌ DO NOT expose it to the public internet**  

---

🎯 Attack Surface Overview

The application intentionally contains multiple real-world vulnerabilities, including:

- SQL Injection (SQLi) — multiple endpoints
- Local File Inclusion (LFI) — arbitrary file reads
- Remote Code Execution (RCE) — OS command execution
- Server-Side Request Forgery (SSRF) — internal metadata access
- Cross-Site Scripting (XSS) — reflected & stored
- Cross-Site Request Forgery (CSRF) — no protections
- Insecure File Uploads
- Sensitive Data Exposure

This lab simulates a realistic corporate internal portal with 100+ realistic records.

---

 🚀 Quick Start (Local Only)

 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/corporate-nexus-portal.git
cd corporate-nexus-portal
````

 2️⃣ Create Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

4️⃣ Run the Application

```
python3 app.py
```

Application will be available at:

```
http://localhost:5000
```

---

## 🔐 Demo Credentials

| Username   | Password   |
| ---------- | ---------- |
| admin      | admin123   |
| dev        | dev789     |
| manager    | manager456 |
| john.smith | P@ssw0rd1  |

---

## 🧪 Vulnerability Examples

### 🔓 SQL Injection

```http
GET /users?search=' OR 1=1--
```

### 📂 Local File Inclusion (LFI)

```http
GET /upload?path=/etc/passwd
```

### 💥 Remote Code Execution (RCE)

```http
GET /debug?cmd=whoami
```

### 🌐 Server-Side Request Forgery (SSRF)

```http
GET /api/ping?url=http://169.254.169.254/latest/meta-data/
```

---

## 🏴 Flags

The lab includes multiple flags for CTF-style progression:

* `FLAG{authorized_pentest_complete}`
* `ADMIN_FLAG{professional_vuln_lab_2026}`

---

## 🗂️ Data & Environment

* SQLite database auto-generated at runtime
* 100+ realistic corporate records
* Logs simulate enterprise activity
* No external services required

---

## 🛑 Security Notice

This repository contains **intentionally vulnerable code**.

The author assumes **no responsibility** for:

* Illegal use
* Deployment to live systems
* Misuse outside controlled lab environments

Use **ONLY** on systems you own or have explicit permission to test.

---

## 📜 License

This project is provided **for educational purposes only**.

You are free to:

* Study
* Modify
* Use in private labs or classrooms

You are **NOT permitted** to:

* Deploy publicly
* Monetize without modification
* Use for unauthorized testing

---

## ⭐ Suggested Use Cases

* Bug bounty training
* Web security courses
* Red team exercises
* Secure code review practice
* Blue team detection labs

---

## 🧠 Future Improvements (Optional)

* Dockerized deployment
* Secure / patched branch
* Automated exploit scripts
* CI-based SAST scans
* OWASP ASVS mapping

---

Happy hacking — **ethically**. 🛡️🏴
