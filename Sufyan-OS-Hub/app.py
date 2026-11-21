import os
import platform
import subprocess
from functools import wraps
from pathlib import Path

import psutil
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from database import init_db, verify_user, get_tasks, add_task, toggle_task, delete_task

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key-before-public-hosting")
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")

init_db()

# title, description, usage/example, category
COMMANDS = {
    "pwd": ("Print Working Directory", "Current folder ka full path dikhata hai.", "pwd", "Basic"),
    "ls": ("List Files", "Folder ke files aur folders dikhata hai.", "ls -lah", "Basic"),
    "cd": ("Change Directory", "Doosre folder mein jane ke liye.", "cd ~/Downloads", "Basic"),
    "mkdir": ("Make Directory", "Naya folder banata hai.", "mkdir projects", "Basic"),
    "rmdir": ("Remove Empty Directory", "Sirf khaali folder delete karta hai.", "rmdir old_folder", "Basic"),
    "touch": ("Create File", "Nayi khaali file banata hai.", "touch main.py", "Basic"),
    "cp": ("Copy", "File ya folder copy karta hai.", "cp file.txt backup.txt", "Basic"),
    "mv": ("Move / Rename", "File move ya rename karta hai.", "mv old.txt new.txt", "Basic"),
    "rm": ("Remove", "File delete karta hai. Sambhal kar use karein.", "rm file.txt", "Basic"),
    "cat": ("Show File", "Text file ka content terminal mein dikhata hai.", "cat notes.txt", "Basic"),
    "less": ("Read File", "Bari file ko page by page parhta hai.", "less /var/log/syslog", "Basic"),
    "head": ("First Lines", "File ki pehli 10 lines dikhata hai.", "head -n 20 file.txt", "Basic"),
    "tail": ("Last Lines", "File ki aakhri 10 lines dikhata hai.", "tail -f app.log", "Basic"),
    "grep": ("Search Text", "File ke andar lafz ya pattern search karta hai.", "grep -n 'error' app.log", "Basic"),
    "find": ("Find Files", "Naam ya condition se files dhoondta hai.", "find . -name '*.py'", "Basic"),
    "which": ("Find Program Path", "Command ka executable path dikhata hai.", "which python3", "Basic"),
    "man": ("Manual", "Command ka detailed manual kholta hai.", "man ls", "Basic"),
    "clear": ("Clear Terminal", "Terminal screen saaf karta hai.", "clear", "Basic"),
    "history": ("Command History", "Pehle chalaye gaye commands dikhata hai.", "history", "Basic"),
    "echo": ("Print Text", "Text ya variable terminal par print karta hai.", "echo 'Hello Parrot'", "Basic"),
    "whoami": ("Current User", "Logged-in username dikhata hai.", "whoami", "System"),
    "id": ("User ID", "User aur group IDs dikhata hai.", "id", "System"),
    "uname": ("Kernel Info", "Kernel aur system information dikhata hai.", "uname -a", "System"),
    "hostname": ("Computer Name", "System ka hostname dikhata/set karta hai.", "hostname", "System"),
    "date": ("Date and Time", "System ki date/time dikhata hai.", "date", "System"),
    "uptime": ("System Uptime", "PC kitni der se on hai dikhata hai.", "uptime", "System"),
    "free": ("Memory Usage", "RAM aur swap usage dikhata hai.", "free -h", "System"),
    "df": ("Disk Free", "Disk partitions ki free space dikhata hai.", "df -h", "System"),
    "du": ("Directory Size", "Folder/file ki storage usage dikhata hai.", "du -sh ~/Downloads", "System"),
    "lsblk": ("Block Devices", "Disks aur partitions list karta hai.", "lsblk -f", "System"),
    "lscpu": ("CPU Details", "Processor ki detailed information dikhata hai.", "lscpu", "System"),
    "lspci": ("PCI Devices", "GPU, network aur PCI devices list karta hai.", "lspci -nn", "System"),
    "lsusb": ("USB Devices", "Connected USB devices list karta hai.", "lsusb", "System"),
    "ps": ("Processes", "Running processes ki list dikhata hai.", "ps aux", "System"),
    "top": ("Live Processes", "CPU/RAM usage live dikhata hai.", "top", "System"),
    "htop": ("Interactive Process Viewer", "Processes ko interactive view mein dikhata hai (install required).", "htop", "System"),
    "kill": ("Stop Process", "PID ke zariye process stop karta hai.", "kill 1234", "System"),
    "systemctl": ("Service Manager", "System services check/start/stop karta hai.", "systemctl status NetworkManager", "System"),
    "journalctl": ("System Logs", "systemd logs dikhata hai.", "journalctl -b -p err", "System"),
    "dmesg": ("Kernel Messages", "Kernel ring buffer messages dikhata hai.", "dmesg -T | tail -n 30", "System"),
    "ip": ("Network Settings", "IP addresses aur network links dikhata hai.", "ip -br addr", "Network"),
    "ping": ("Test Connection", "Network host tak connection test karta hai.", "ping -c 4 1.1.1.1", "Network"),
    "ip route": ("Routing Table", "Network routes dikhata hai.", "ip route", "Network"),
    "ss": ("Socket Status", "Open/listening network sockets dikhata hai.", "ss -tulpen", "Network"),
    "curl": ("URL Request", "URL se data request/download karta hai.", "curl -I https://example.com", "Network"),
    "wget": ("Download", "Internet se file download karta hai.", "wget https://example.com/file.zip", "Network"),
    "nmcli": ("Network Manager CLI", "Wi-Fi/network connections manage karta hai.", "nmcli device status", "Network"),
    "ip neigh": ("Neighbor Table", "Local network devices ki neighbor table dikhata hai.", "ip neigh", "Network"),
    "sudo": ("Run as Administrator", "Command ko elevated privileges se chalata hai.", "sudo apt update", "Admin"),
    "apt update": ("Refresh Packages", "Package lists update karta hai.", "sudo apt update", "Packages"),
    "apt upgrade": ("Upgrade Packages", "Installed packages update karta hai.", "sudo apt upgrade", "Packages"),
    "apt install": ("Install Package", "Naya package install karta hai.", "sudo apt install git", "Packages"),
    "apt remove": ("Remove Package", "Package uninstall karta hai.", "sudo apt remove package-name", "Packages"),
    "apt search": ("Search Packages", "Repositories mein package search karta hai.", "apt search firefox", "Packages"),
    "apt show": ("Package Details", "Package ki details dikhata hai.", "apt show git", "Packages"),
    "dpkg": ("Debian Package Tool", "DEB packages aur installed packages manage karta hai.", "dpkg -l | grep firefox", "Packages"),
    "apt autoremove": ("Remove Unused Packages", "Unused dependencies remove karta hai.", "sudo apt autoremove", "Packages"),
    "chmod": ("Change Permissions", "File permissions change karta hai.", "chmod +x script.sh", "Permissions"),
    "chown": ("Change Owner", "File ka owner/group change karta hai.", "sudo chown user:user file.txt", "Permissions"),
    "chgrp": ("Change Group", "File ka group change karta hai.", "sudo chgrp developers file.txt", "Permissions"),
    "tar": ("Archive Files", "Files ko tar archive mein pack/unpack karta hai.", "tar -czf backup.tar.gz folder/", "Archive"),
    "zip": ("Create ZIP", "ZIP archive banata hai.", "zip -r backup.zip folder/", "Archive"),
    "unzip": ("Extract ZIP", "ZIP archive extract karta hai.", "unzip backup.zip", "Archive"),
    "git": ("Version Control", "Code history aur collaboration manage karta hai.", "git status", "Developer"),
    "python3": ("Python Interpreter", "Python script chalata hai.", "python3 main.py", "Developer"),
    "pip": ("Python Packages", "Python libraries install karta hai.", "python -m pip install flask", "Developer"),
    "gcc": ("C Compiler", "C program compile karta hai.", "gcc main.c -o main", "Developer"),
    "g++": ("C++ Compiler", "C++ program compile karta hai.", "g++ main.cpp -o main", "Developer"),
    "make": ("Build Tool", "Makefile ke mutabiq project build karta hai.", "make", "Developer"),
    "nano": ("Terminal Editor", "Terminal mein text edit karta hai.", "nano app.py", "Developer"),
    "vim": ("Vim Editor", "Terminal-based text editor.", "vim main.c", "Developer"),
    "ssh": ("Secure Shell", "Remote computer se secure login karta hai.", "ssh user@192.168.1.10", "Network"),
    "scp": ("Secure Copy", "SSH ke zariye files copy karta hai.", "scp file.txt user@host:~/", "Network"),
    "ufw": ("Firewall", "Uncomplicated Firewall manage karta hai.", "sudo ufw status", "Security"),
    "passwd": ("Change Password", "Apne user ka password change karta hai.", "passwd", "Security"),
    "sha256sum": ("File Checksum", "File ka SHA-256 hash calculate karta hai.", "sha256sum file.iso", "Security"),
    "gpg": ("Encryption Tool", "Files/signatures encrypt aur verify karta hai.", "gpg --version", "Security"),
    "crontab": ("Scheduled Jobs", "Recurring tasks schedule karta hai.", "crontab -e", "Admin"),
    "reboot": ("Restart PC", "System restart karta hai.", "sudo reboot", "Admin"),
    "shutdown": ("Power Off", "System shutdown karta hai.", "sudo shutdown -h now", "Admin"),
    "mount": ("Mount Filesystem", "Filesystem ko directory par mount karta hai.", "findmnt", "Storage"),
    "blkid": ("Block Device IDs", "Partitions ke UUID/filesystem dikhata hai.", "sudo blkid", "Storage"),
    "smartctl": ("Disk Health", "SMART disk health check (smartmontools required).", "sudo smartctl -a /dev/sda", "Storage"),
    "neofetch": ("System Summary", "Terminal mein system summary (package availability varies).", "neofetch", "System"),
}

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

def safe_command_output(command, timeout=3):
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
        return (result.stdout or result.stderr).strip()
    except Exception:
        return ""

def get_computer_info():
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    try:
        freq = psutil.cpu_freq()
        cpu_speed = f"{freq.current / 1000:.2f} GHz" if freq and freq.current else "Not detected"
    except Exception:
        cpu_speed = "Not detected"
    cpu_name = safe_command_output(["bash", "-lc", "grep -m1 'model name' /proc/cpuinfo | cut -d: -f2"]).strip() or platform.processor() or "Unknown CPU"
    gpu = safe_command_output(["bash", "-lc", "lspci 2>/dev/null | grep -Ei 'VGA|3D|Display' | head -n 3"])
    if not gpu:
        gpu = "GPU model not detected (install pciutils / check lspci)"
    try:
        net = psutil.net_if_addrs()
        interfaces = [name for name, addrs in net.items() if name != "lo" and any(a.family == 2 for a in addrs)]
        network = ", ".join(interfaces) if interfaces else "No active interface detected"
    except Exception:
        network = "Not detected"
    try:
        boot = psutil.boot_time()
        import datetime
        uptime = str(datetime.timedelta(seconds=int(__import__("time").time() - boot)))
    except Exception:
        uptime = "Not detected"
    return {
        "cpu": cpu_name.strip(),
        "cpu_cores": psutil.cpu_count(logical=False) or "Unknown",
        "cpu_threads": psutil.cpu_count(logical=True) or "Unknown",
        "cpu_speed": cpu_speed,
        "ram_total_gb": round(mem.total / (1024**3), 1),
        "ram_used_gb": round(mem.used / (1024**3), 1),
        "ram_percent": mem.percent,
        "disk_total_gb": round(disk.total / (1024**3), 1),
        "disk_used_gb": round(disk.used / (1024**3), 1),
        "disk_free_gb": round(disk.free / (1024**3), 1),
        "gpu": gpu,
        "os": f"{platform.system()} {platform.release()}",
        "distribution": safe_command_output(["bash", "-lc", "grep '^PRETTY_NAME=' /etc/os-release | cut -d= -f2- | tr -d '\"'"]) or platform.platform(),
        "architecture": platform.machine(),
        "network": network,
        "uptime": uptime,
    }

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if verify_user(username, password):
            session.clear()
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("home"))
        error = "Username ya password ghalat hai."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def home():
    return render_template("home.html", username=session.get("username"))

@app.route("/commands")
@login_required
def commands():
    return render_template("commands.html", commands=COMMANDS)

@app.route("/computer")
@login_required
def computer():
    return render_template("computer.html", info=get_computer_info())

@app.route("/api/computer")
@login_required
def api_computer():
    return jsonify(get_computer_info())

@app.route("/api/search")
@login_required
def api_search():
    query = request.args.get("q", "").strip().lower()
    if not query:
        return jsonify({"type": "empty", "results": []})
    info = get_computer_info()
    hardware_keys = {
        "cpu": ["cpu", "processor", "core", "thread"],
        "ram": ["ram", "memory"],
        "disk": ["disk", "storage", "ssd", "hdd"],
        "gpu": ["gpu", "graphics", "vga"],
        "os": ["os", "operating system", "parrot", "linux"],
        "network": ["network", "wifi", "internet", "ip"],
    }
    for part, words in hardware_keys.items():
        if any(word in query for word in words):
            return jsonify({"type": "hardware", "label": part.upper(), "value": info.get(part, info.get("distribution", "")), "info": info})
    matches = []
    for key, item in COMMANDS.items():
        title, description, example, category = item
        if query in key.lower() or query in title.lower() or query in description.lower() or query in category.lower():
            matches.append({"command": key, "title": title, "description": description, "example": example, "category": category})
    return jsonify({"type": "commands", "results": matches[:30]})

@app.route("/roblox")
@login_required
def roblox():
    return render_template("roblox.html", info=get_computer_info())

@app.route("/todo", methods=["GET", "POST"])
@login_required
def todo():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if title:
            add_task(title[:180])
            flash("Task add ho gaya.", "success")
        else:
            flash("Pehle task ka naam likho.", "error")
        return redirect(url_for("todo"))
    return render_template("todo.html", tasks=get_tasks())

@app.route("/todo/toggle/<int:task_id>", methods=["POST"])
@login_required
def todo_toggle(task_id):
    toggle_task(task_id)
    return redirect(url_for("todo"))

@app.route("/todo/delete/<int:task_id>", methods=["POST"])
@login_required
def todo_delete(task_id):
    delete_task(task_id)
    flash("Task delete ho gaya.", "success")
    return redirect(url_for("todo"))

@app.route("/contact")
@login_required
def contact():
    return render_template("contact.html")

@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", code=404, message="Yeh page nahi mila."), 404

@app.errorhandler(500)
def server_error(error):
    return render_template("error.html", code=500, message="Server par error aa gaya."), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
