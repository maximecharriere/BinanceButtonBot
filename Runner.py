import subprocess
import os

root = os.path.dirname(os.path.realpath(__file__))
filename = 'BinanceButtonBot.py'
while True:
    p = subprocess.run('python '+filename, shell=True, cwd=root)
    if p.returncode == 13:
        continue
    else:
        break

exit(p)