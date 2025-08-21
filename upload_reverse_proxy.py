import paramiko
from config import hostname, username, password, remote_path, local_path
import os

# Ensure the local directory exists before uploading
if not os.path.isdir(local_path):
    raise NotADirectoryError(f"Local directory not found: {local_path}")

# Connect and upload files
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)
sftp = ssh.open_sftp()

try:
    local_files = [f for f in os.listdir(local_path) if os.path.isfile(os.path.join(local_path, f))]
    if not local_files:
        print(f"No files to upload in {local_path}")
    else:
        for file in local_files:
            local_file_path = os.path.join(local_path, file)
            remote_file_path = os.path.join(remote_path, file).replace("\\", "/")
            sftp.put(local_file_path, remote_file_path)
            print(f'Uploaded {file} to {remote_file_path}')
        print(f'All files uploaded to {remote_path}')
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    sftp.close()
    ssh.close()

