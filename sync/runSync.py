# Before running the script make sure you have paramiko and dotenv
# you can install them with the following commands:
# pip install paramiko
# pip install python-dotenv

import paramiko
import os
from dotenv import load_dotenv
import requests

load_dotenv()

keyfilename = os.getenv('SSH_PRIVATE_KEY_PATH')
host = os.getenv('SSH_HOST')
user = os.getenv('SSH_USER')
rootPassword = os.getenv('ROOT_PASS')
port= os.getenv('SSH_PORT')
sync_url= os.getenv('SYNC_URL')
url_user = os.getenv('SYNC_URL_USER')
url_pass = os.getenv('SYNC_URL_PASS')

print(keyfilename,host,user,rootPassword,port)

k = paramiko.Ed25519Key.from_private_key_file(keyfilename)
# OR k = paramiko.DSSKey.from_private_key_file(keyfilename)
ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=host, username=user, pkey=k, port=port)

cmd_to_execute = "echo {}|sudo -S su -;service neo4j restart;journalctl -u neo4j -f".format(rootPassword)
print(cmd_to_execute)

ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
print(ssh_stdin,ssh_stdout,ssh_stderr)


print(requests.get(sync_url, auth=(url_user, url_pass)).content)
