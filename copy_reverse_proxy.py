import paramiko
from config import hostname, username, password, remote_path, local_path
import os

# Ensure the local directory exists
os.makedirs(local_path, exist_ok=True)

# Connect and download files
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)
sftp = ssh.open_sftp()

try:
    files = sftp.listdir(remote_path)
    for file in files:
        remote_file_path = os.path.join(remote_path, file).replace("\\", "/")
        local_file_path = os.path.join(local_path, file)
        sftp.get(remote_file_path, local_file_path)
        print(f'Downloaded {file} to {local_file_path}')
    print(f'All files downloaded to {local_path}')
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    sftp.close()
    ssh.close()
