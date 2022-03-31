import subprocess

filename = 'BinanceButtonBot.py'
while True:
    p = subprocess.Popen('python '+filename, shell=True).wait()

    if p == 2:
        continue
    else:
        break