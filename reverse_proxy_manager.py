import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import datetime
import threading
import os
import paramiko
from config import hostname, username, password

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_SCRIPT = os.path.join(SCRIPT_DIR, 'download_reverse_proxy.bat')
UPLOAD_SCRIPT = os.path.join(SCRIPT_DIR, 'upload_reverse_proxy.bat')

class ReverseProxyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Reverse Proxy File Manager')
        self.geometry('600x500')  # Increased window size for new button
        self.resizable(False, False)
        self.configure(bg='#f7f7f7')
        self.create_widgets()

    def create_widgets(self):
        # Display server info at the top
        server_info = f"Server: {hostname}"
        tk.Label(self, text=server_info, font=('Arial', 22, 'bold'), fg='#2c3e50', bg='#f7f7f7').pack(pady=(18, 2))
        tk.Label(self, text='Reverse Proxy File Manager', font=('Arial', 20, 'bold'), bg='#f7f7f7').pack(pady=8)
        tk.Button(self, text='Download', bg='#3498db', fg='white', font=('Arial', 16), width=25, height=2,
                  command=lambda: self.run_script(DOWNLOAD_SCRIPT, 'Download')).pack(pady=7)
        tk.Button(self, text='Upload', bg='#27ae60', fg='white', font=('Arial', 16), width=25, height=2,
                  command=lambda: self.run_script(UPLOAD_SCRIPT, 'Upload')).pack(pady=7)
        tk.Button(self, text='Restart Nginx', bg='#e67e22', fg='white', font=('Arial', 16), width=25, height=2,
                  command=self.restart_nginx).pack(pady=7)
        self.status = scrolledtext.ScrolledText(self, height=13, font=('Consolas', 12), state='disabled', wrap='word')
        self.status.pack(padx=16, pady=14, fill='both', expand=True)
        self.set_status('App started. Ready.')

    def set_status(self, msg):
        now = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
        self.status['state'] = 'normal'
        self.status.insert('end', f'{now} - {msg}\n')
        self.status.see('end')
        self.status['state'] = 'disabled'
        self.update_idletasks()

    def run_script(self, script, action):
        def task():
            self.after(0, self.set_status, f'{action}: Running {os.path.basename(script)}...')
            if not os.path.isfile(script):
                self.after(0, self.set_status, f'{action}: Script not found: {script}')
                return
            try:
                result = subprocess.run([script], capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    output = result.stdout.strip() or 'Completed with no output.'
                    self.after(0, self.set_status, f'{action}: Success. {output}')
                else:
                    error = result.stderr.strip() or 'Unknown error.'
                    self.after(0, self.set_status, f'{action}: Error. {error}')
            except Exception as e:
                self.after(0, self.set_status, f'{action}: Exception: {str(e)}')
        threading.Thread(target=task, daemon=True).start()

    def restart_nginx(self):
        def task():
            self.after(0, self.set_status, 'Restart Nginx: Connecting to server...')
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname, username=username, password=password)
                stdin, stdout, stderr = ssh.exec_command('systemctl restart nginx')
                exit_status = stdout.channel.recv_exit_status()
                if exit_status == 0:
                    self.after(0, self.set_status, 'Restart Nginx: Success.')
                else:
                    error = stderr.read().decode().strip() or 'Unknown error.'
                    self.after(0, self.set_status, f'Restart Nginx: Error. {error}')
                ssh.close()
            except Exception as e:
                self.after(0, self.set_status, f'Restart Nginx: Exception: {str(e)}')
        threading.Thread(target=task, daemon=True).start()

if __name__ == '__main__':
    app = ReverseProxyApp()
    app.mainloop()
