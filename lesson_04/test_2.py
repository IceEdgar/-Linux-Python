import yaml
from sshcheckers import ssh_checkout, ssh_checkout_negative


with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_neg1(self):
        # test1
        assert ssh_checkout_negative(data["IP"], data["USER"], data["PASSWD"],
                                     f"{data['FOLDER_OUT']}; 7z e arx2bad.7z -o{data['FOLDER_1']} -y",
                                     "ERROR"), "test1 FAIL"

    def test_neg2(self):
        # test2
        assert ssh_checkout_negative(data["IP"], data["USER"], data["PASSWD"],
                                     f"{data['FOLDER_OUT']}; 7z t arx2bad.7z", "ERROR"), "test2 FAIL"

    def test_neg3(self):
        # test3
        res = []
        res.append(ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                                f"echo '{data['PASSWD']}' | sudo -S dpkg -r {data['PKGNAME']}",
                                "Удаляется"))
        res.append(ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                                f"echo '{data['PASSWD']}' | sudo -S dpkg -s {data['PKGNAME']}",
                                "Status: deinstall ok"))
        assert all(res), "test3 FAIL"


