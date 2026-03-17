import subprocess
password = "hardcoded_secret_123"
user_input = input("cmd: ")
subprocess.call(user_input, shell=True)  # command injection
