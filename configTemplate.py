# config.py
import os

hostname = '192.168.x.xx'  # Change to your server's address
username = 'username'        # Change to your SSH username
password = 'password'        # Change to your SSH password
remote_path = '/etc/nginx/sites-enabled/reverse-proxy'
host_dir = hostname.replace('.', '_')
local_path = os.path.join(os.path.dirname(__file__), host_dir, 'reverse-proxy')
