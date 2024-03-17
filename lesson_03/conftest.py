import pytest
from checkers import checkout, getout
import random, string
import yaml
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checkout(f"mkdir {data['FOLDER_TST']} {data['FOLDER_TST']} {data['FOLDER_1']} {data['FOLDER_2']}", "")


@pytest.fixture()
def clear_folders():
    return checkout(f"rm -rf {data['FOLDER_TST']}/* {data['FOLDER_TST']}/* {data['FOLDER_1']}/* {data['FOLDER_2']}/*", "")


@pytest.fixture()
def make_files():
    list_off_files = [ ]
    for i in range(data["COUNT"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout(f"cd {data['FOLDER_TST']}; dd if=/dev/urandom of={filename} bs={data['BS']} count=1 iflag=fullblock", ""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout(f"cd {data['FOLDER_TST']}; mkdir {subfoldername}", ""):
        return None, None
    if not checkout(f"cd {data['FOLDER_TST']}/{subfoldername}; dd if=/dev/urandom of={testfilename} bs=1M count=1 iflag=fullblock",""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print(f"Start: {datetime.now().strftime('%H:%M:%S.%f')}")
    yield
    print(f"Finish: {datetime.now().strftime('%H:%M:%S.%f')}")


@pytest.fixture()
def make_bad_arx():
    checkout(f"cd {data['FOLDER_TST']}; 7z a {data['FOLDER_OUT']}/arxbad -t{data['TYPE']}", "Everything is Ok")
    checkout(f"truncate -s 1 {data['FOLDER_OUT']}/arxbad.{data['TYPE']}", "Everything is Ok")
    yield "arxbad"
    checkout(f"rm -f {data['FOLDER_OUT']}/arxbad.{data['TYPE']}", "")


@pytest.fixture(autouse=True)
def status():
    yield
    stat = getout("cat /proc/loadavg")
    checkout(f"echo 'time: {datetime.now().strftime('%H:%M:%S.%f')} count:{data['COUNT']} size: {data['BS']} load: {stat}'>> status.txt", "")