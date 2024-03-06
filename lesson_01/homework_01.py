import  subprocess

def sub(directory: str, name: str) -> bool:
    res = subprocess.run(directory, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = res.stdout
    lst = out.split("\n")
    if not res.returncode and name in lst:
        return True
    return False


print(sub('cat /etc/os-release', 'VERSION="22.04.4 LTS (Jammy Jellyfish)"'))
