import paramiko
from config import hostname, username, password, remote_path, local_path
import os

# Ensure the local file exists before uploading
if not os.path.isfile(local_path):
    raise FileNotFoundError(f"Local file not found: {local_path}")

# Connect and upload file
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)
sftp = ssh.open_sftp()
sftp.put(local_path, remote_path)
sftp.close()
ssh.close()
print(f'File uploaded to {remote_path}')
