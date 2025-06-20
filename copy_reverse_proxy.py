import paramiko
from config import hostname, username, password, remote_path, local_path

# Connect and copy file
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)
sftp = ssh.open_sftp()
sftp.get(remote_path, local_path)
sftp.close()
ssh.close()
print(f'File copied to {local_path}')
