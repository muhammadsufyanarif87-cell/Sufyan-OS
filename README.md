# 🦜 Sufyan OS Hub

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=27&pause=1000&color=22C55E&center=true&vCenter=true&width=650&lines=Welcome+to+Sufyan+OS+Hub;Linux+Commands+%26+Tools;PC+Hardware+Checker;Roblox+Compatibility+Checker;Built+with+Python+%26+Flask" alt="Animated typing header" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/OS-Parrot%20Linux-green?logo=linux" alt="Parrot Linux">
  <img src="https://img.shields.io/badge/Status-Development-orange" alt="Development">
</p>

<p align="center">
  **A personal Linux dashboard, command encyclopedia, PC hardware checker and Roblox compatibility checker.**
</p>

---

## 📖 About the Project

**Sufyan OS Hub** is a Flask-based web application designed to provide useful Linux tools and system information through one dashboard.

It is developed using Python, Flask, SQLite, HTML, CSS and JavaScript.

The project is especially useful for Linux learners who want to understand their computer hardware, learn terminal commands and check whether their PC can run certain applications.

## ✨ Main Features

### 🏠 1. Dashboard
- Main dashboard with a search feature.
- Quick access to different sections.
- Search for Linux commands and hardware information.
- Simple and responsive interface.

### 🐧 2. Linux Command Encyclopedia
- Collection of useful Linux and Parrot OS commands.
- Command descriptions.
- Examples and usage information.
- Terminal commands for beginners.
- Copy commands for easy use.

### 💻 3. PC Hardware Information
The computer information section can display:

- CPU model.
- Physical CPU cores.
- CPU threads.
- RAM total and available.
- GPU model.
- Graphics driver information.
- OpenGL version.
- Vulkan information.
- Motherboard information.
- Storage capacity.
- Available disk space.
- Linux distribution.
- Linux kernel version.
- System architecture.

Hardware information is collected using Python and Linux system commands.

### 🎮 4. Roblox Compatibility Checker

The Roblox page compares your PC hardware with Roblox requirements.

**Roblox Studio — Game Development**
- CPU model and cores.
- RAM requirements.
- Graphics compatibility.
- OpenGL version.
- Vulkan version.
- Linux kernel version.
- Vinegar compatibility information.

**Roblox Player — Gaming**
- CPU architecture.
- SSE4.1 support.
- SSE4.2 support.
- OpenGL ES information.
- Vulkan information.
- Linux kernel compatibility.
- Sober compatibility information.

**Upgrade recommendations**
- CPU recommendations.
- RAM upgrade targets.
- GPU recommendations.
- SSD recommendations.
- Motherboard compatibility.
- Power supply information.

> Note: Roblox does not officially support Linux. Vinegar and Sober are community-developed Linux workarounds. Their compatibility depends on hardware, drivers and software versions.

### ✅ 5. To-Do List
- Add tasks.
- Mark tasks completed.
- Delete tasks.
- Store tasks in SQLite.
- Keep tasks after restarting the application.

### 🔐 6. Login System
- Login page.
- Protected dashboard.
- Session-based authentication.
- Password hashing.
- SQLite user database.

### 📞 7. Contact and About
- About the developer.
- Contact information.
- Project information.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application |
| SQLite | Database |
| HTML5 | Page structure |
| CSS3 | Design and responsive layout |
| JavaScript | Interactive features |
| psutil | CPU, RAM and disk information |
| lspci | Graphics and hardware detection |
| dmidecode | Motherboard and RAM information |
| Mesa utilities | OpenGL information |
| Vulkan tools | Vulkan information |

---

## 📁 Project Structure

```text
Sufyan-OS-Hub/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
│
├── instance/
│   └── hub.db
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── commands.html
│   ├── computer.html
│   ├── roblox.html
│   ├── todo.html
│   ├── contact.html
│   └── error.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    ├── js/
    │   └── script.js
    │
    └── images/
```

> Your actual database filename and folder structure may differ. Keep this tree synchronized with your project.

---

## ⚙️ Installation on Parrot OS

### Step 1 — Update the system

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2 — Install required packages

```bash
sudo apt install python3 python3-venv python3-pip pciutils dmidecode mesa-utils mesa-utils-extra vulkan-tools -y
```

### Step 3 — Open the project directory

```bash
cd ~/Documents/app/Sufyan-OS-Hub
```

### Step 4 — Create a virtual environment

```bash
python3 -m venv venv
```

### Step 5 — Activate the environment

```bash
source venv/bin/activate
```

### Step 6 — Install Python packages

```bash
pip install -r requirements.txt
```

If `psutil` is missing:

```bash
pip install psutil
```

### Step 7 — Start the application

```bash
python app.py
```

### Step 8 — Open in Firefox

```text
http://127.0.0.1:5000
```

---

## 🖥️ Hardware Checking Commands

These commands help you inspect your PC directly from Parrot OS.

### CPU

```bash
lscpu
```

Show CPU model:

```bash
lscpu | grep "Model name"
```

Show physical cores and threads:

```bash
lscpu | grep -E "Core\(s\)|Socket\(s\)|CPU\(s\)"
```

Check SSE instructions:

```bash
grep -m1 '^flags' /proc/cpuinfo
```

### RAM

```bash
free -h
```

Check RAM slots:

```bash
sudo dmidecode -t memory
```

### Motherboard

```bash
sudo dmidecode -t baseboard
```

### GPU

```bash
lspci -nnk | grep -A4 -Ei 'VGA|3D|Display'
```

### OpenGL

```bash
glxinfo -B
```

### Vulkan

```bash
vulkaninfo --summary
```

### OpenGL ES

```bash
eglinfo
```

### Storage

```bash
lsblk -o NAME,SIZE,MODEL,TYPE
```

Check free storage:

```bash
df -h /
```

### Linux kernel

```bash
uname -r
```

### System architecture

```bash
uname -m
```

---

## 🎮 Roblox Compatibility Information

There are two different Roblox applications:

| Application | Purpose | Linux workaround |
|---|---|---|
| Roblox Studio | Creating games | Vinegar |
| Roblox Player | Playing games | Sober |

### Roblox Studio

Official documentation:

https://create.roblox.com/docs/studio/setup

Vinegar project:

https://vinegarhq.org/

### Roblox Player

Sober project:

https://sober.vinegarhq.org/

**Important:** A successful hardware check does not guarantee that Roblox will run. Software compatibility, drivers and updates also matter.

---

## 🗄️ Database

Sufyan OS Hub uses SQLite for local data storage.

The database can store:

- User accounts.
- Password hashes.
- To-do tasks.
- Task completion status.

SQLite is useful for this project because it does not require a separate database server.

---

## 🔒 Security Notes

For local development:

- Keep your password private.
- Never publish your database file.
- Do not upload your virtual environment.
- Do not expose your Flask debug server to the public internet.

Before public hosting:

- Use a strong random `SECRET_KEY`.
- Disable Flask debug mode.
- Add CSRF protection.
- Use HTTPS.
- Add login rate limiting.
- Protect private user information.
- Keep dependencies updated.

Do not use the development server as a production web server.

---

## 🧰 Troubleshooting

### Flask module not found

```bash
source venv/bin/activate
pip install Flask
```

### psutil module not found

```bash
pip install psutil
```

### OpenGL command not found

```bash
sudo apt install mesa-utils -y
```

### Vulkan command not found

```bash
sudo apt install vulkan-tools -y
```

### Permission denied for hardware information

```bash
sudo dmidecode -t memory
```

Some hardware details require administrator permissions.

### Port 5000 already in use

Find the process:

```bash
sudo lsof -i :5000
```

Stop the process only if you know it is safe to do so.

---

## 🚀 Future Improvements

Possible future features:

- Live system monitoring.
- CPU temperature monitoring.
- GPU temperature monitoring.
- More Linux distributions support.
- Hardware upgrade comparison.
- PC component price comparison.
- More command categories.
- Dark and light themes.
- Improved mobile dashboard.
- More system diagnostic tools.
- User profile settings.
- Export hardware reports.

---

## 👨‍💻 Developer

**Developer:** Muhammad Sufyan Arif

**Project:** Sufyan OS Hub

**Platform:** Parrot OS / Linux

**Backend:** Python + Flask

**Database:** SQLite

---

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=1000&color=22C55E&center=true&vCenter=true&width=500&lines=Keep+Learning;Keep+Building;Keep+Coding;Made+with+Python+%26+Flask" alt="Animated footer">
</p>

<p align="center">
  **Muhammad Sufyan Arif**
</p>
