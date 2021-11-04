import subprocess

completed = subprocess.run(["/bin/journalctl --since='1 hour ago'"], shell=True)
print(completed.stdout)