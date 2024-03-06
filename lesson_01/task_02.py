import subprocess

res = subprocess.run("cat /etc/os-release", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
out = res.stdout
if not res.returncode:
    lst = out.split("\n")
    if 'VERSION="22.04.4 LTS (Jammy Jellyfish)"' in lst and 'VERSION_CODENAME=jammy' in lst:
        print("SUCCESS")
else:
    print("FAIL")