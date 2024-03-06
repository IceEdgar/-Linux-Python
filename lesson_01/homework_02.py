import  subprocess
import string
def sub(directory: str, name: str, word = 'Yes'):
    res = subprocess.run(directory, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = res.stdout
    lst = out.split("\n")
    if not res.returncode and name in lst:
        for x in name:
            if x in string.punctuation:
                name = name.replace(x, ' ')
        if word in name:
            print('Find')
        else:
            print('No find')
        return True
    return False


print(sub('cat /etc/os-release', 'VERSION="22.04.4 LTS (Jammy Jellyfish)"', '22'))
