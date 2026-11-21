# Sufyan OS Hub

Flask + SQLite personal dashboard with a Parrot OS-inspired interface.

## Install on Parrot OS

```bash
cd ~/Documents/app/Sufyan-OS-Hub
sudo apt update
sudo apt install python3-venv python3-pip pciutils -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in Firefox.

## Login

- Username: `sufyan`
- Password: `MSufyan141R`

For a different initial password, set `HUB_PASSWORD` before the first database is created. The user is only seeded when the SQLite database has no `sufyan` account.

## Notes

- `sufyan_hub.db` stores users and tasks.
- The password is stored as a Werkzeug password hash.
- `psutil` supplies live system metrics; `pciutils` provides `lspci` for GPU detection.
- The commands page is a learning reference. It does not execute commands from the website.
- Roblox Studio's official documentation lists Windows and macOS; Linux is not officially supported.
- This project is intended for local learning. Before public hosting, configure a strong `SECRET_KEY`, disable Flask debug mode, add CSRF protection, HTTPS, login rate limiting, and review whether you want your phone number publicly visible.
