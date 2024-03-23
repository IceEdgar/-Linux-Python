import pytest
from sshcheckers import ssh_checkout, ssh_getout
import random
import string
import yaml
from datetime import datetime


with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True)
def make_folders():
    return ssh_checkout(f'{data["IP"]}', f'{data["USER"]}', f'{data["PASSWD"]}',
                        f"mkdir -p {data['FOLDER_TST']} {data['FOLDER_OUT']} {data['FOLDER_1']} {data['FOLDER_2']}", "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout('0.0.0.0', 'user2', '111',
                        f"rm -rf {data['FOLDER_TST']}/* {data['FOLDER_OUT']}/* {data['FOLDER_1']}/* {data['FOLDER_2']}/*", "")


@pytest.fixture(autouse=True)
def make_files():
    list_off_files = []
    for i in range(5):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                        f"cd {data['FOLDER_TST']}; dd if=/dev/urandom of={filename} bs={data['BS']} count=1 iflag=fullblock", ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data["IP"], data["USER"], data["PASSWD"], f"cd {data['FOLDER_TST']}; mkdir {subfoldername}", ""):
        return None, None
    if not ssh_checkout(data["IP"], data["USER"], data["PASSWD"], f"cd {data['FOLDER_TST']}/{subfoldername}; "
                                        f"dd if=/dev/urandom of={testfilename} bs=1M count=1 iflag=fullblock", ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def make_bad_arx():
    ssh_checkout(f'{data["IP"]}', f'{data["USER"]}', f'{data["PASSWD"]}', f"cd {data['FOLDER_TST']}; 7z a {data['FOLDER_OUT']}/arxbad -t{data['TYPE']}", "Everything is Ok")
    ssh_checkout(f'{data["IP"]}', f'{data["USER"]}', f'{data["PASSWD"]}', f"truncate -s 1 {data['FOLDER_OUT']}/arxbad.{data['TYPE']}", "Everything is Ok")
    yield "arxbad"
    ssh_checkout(f'{data["IP"]}', f'{data["USER"]}', f'{data["PASSWD"]}', f"rm -f {data['FOLDER_OUT']}/arxbad.{data['TYPE']}", "")


@pytest.fixture(autouse=True)
def status():
    yield
    stat = ssh_getout(f'{data["IP"]}', f'{data["USER"]}', f'{data["PASSWD"]}', "cat /proc/loadavg")
    ssh_checkout(f'{data["IP"]}', f'{data["USER"]}', f'{data["PASSWD"]}',f"echo 'time: {datetime.now().strftime('%H:%M:%S.%f')} count:{data['COUNT']} size: {data['BS']} load: {stat}'>> status.txt", "")


@pytest.fixture(autouse=True)
def print_time():
    print(f"Start: {datetime.now().strftime('%H:%M:%S.%f')}")
    yield print(f"Stop: {datetime.now().strftime('%H:%M:%S.%f')}")


@pytest.fixture()
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


