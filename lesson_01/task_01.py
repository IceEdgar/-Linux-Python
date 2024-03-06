import subprocess

res = subprocess.run("cat /etc/os-release", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
out = res.stdout
if "22.04.4" in out and "jammy" in out and not res.returncode:
    print("SUCCESS")
else:
    print("FAIL")