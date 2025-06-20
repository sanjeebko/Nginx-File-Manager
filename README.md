# Reverse Proxy File Manager

A desktop application to manage your Nginx reverse proxy configuration on a remote server. It allows you to download, upload, and restart the Nginx service via a simple GUI.

## How to Run This Application

1. **Copy the configuration template:**
   - Duplicate `configTemplate.py` as `config.py` in the same folder.
   - Edit `config.py` and update the `hostname`, `username`, and `password` fields with your server's SSH details.
   - The `config.py` file is ignored by git (see `.gitignore`), so it is safe to keep your credentials there.

2. **Install dependencies:**
   - Make sure you have Python 3.12+ installed.
   - Install required packages:
     ```
     pip install paramiko
     ```

3. **Run the application:**
   - Double-click the `Reverse Proxy File Manager.lnk.bat` file (recommended, no console window), or
   - Run the app directly:
     ```
     python reverse_proxy_manager.py
     ```

## Features
- **Download**: Download the remote Nginx reverse proxy config to your local machine.
- **Upload**: Upload your local config to the remote server.
- **Restart Nginx**: Remotely restart the Nginx service on your server.
- **Status Log**: See all actions and results in a scrollable status window.

## Security
- Your SSH credentials are stored only in `config.py`, which is excluded from version control by `.gitignore`.
- Do not share your `config.py` file.

## Requirements
- Python 3.12+
- paramiko
- Tkinter (comes with most Python installations)

## Customization
- You can adjust the server address, username, and password in `config.py` at any time.
- The app can be resized or themed by editing `reverse_proxy_manager.py`.

---

For any issues or feature requests, please contact the maintainer.
