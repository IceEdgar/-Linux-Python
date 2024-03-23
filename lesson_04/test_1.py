import yaml
from checkers import getout
from sshcheckers import ssh_checkout, ssh_getout, upload_files


with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def save_log(self, start_time, name):
        with open(name, 'w') as f:
            f.write(getout(f"journalctl --since '{start_time}'"))

    def test_step0(self, start_time):
        res = []
        upload_files(data["IP"], data["USER"], data["PASSWD"], "/home/edgar/tests/p7zip-full.deb",
                     "/home/user2/p7zip-full.deb")
        res.append(ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                                "echo '111' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                                "Настраивается пакет"))
        res.append(ssh_checkout(data["IP"], data["USER"], data["PASSWD"], "echo '111' | sudo -S dpkg -s p7zip-full",
                                "Status: install ok installed"))
        self.save_log(start_time, "log.txt")
        assert all(res), "test0 FAIL"

    def test_step1(self, make_folders,clear_folders, make_files, start_time):
        # test1
        res1 = ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                            f"cd {data['FOLDER_TST']}; 7z a {data['FOLDER_OUT']}/arx2", "Everything is Ok")
        res2 = ssh_checkout(data["IP"], data["USER"], data["PASSWD"], f"ls {data['FOLDER_OUT']}", "arx2.7z")
        print(res1, res1)
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, make_folders,clear_folders, make_files, start_time):
        # test2
        res = []
        res1 = ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                                f"{data['FOLDER_TST']}; 7z a {data['FOLDER_OUT']}/arx2 -t{data['TYPE']}",
                                "Everything is Ok")
        res2 = ssh_checkout(data["IP"], data["USER"], data["PASSWD"],f"{data['FOLDER_OUT']}; 7z e arx2.{data['TYPE']} -o{data['FOLDER_1']} -y","Everything is Ok")
        for item in make_files:
            res.append(ssh_checkout(data["IP"], data["USER"], data["PASSWD"],f"ls {data['FOLDER_1']}", ""))
        assert res1 and res2 and all(res), "test2 FAIL"

    def test_step3(self, clear_folders, make_files, start_time):
        # test3
        res = []
        res1 = ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                                f"{data['FOLDER_TST']}; 7z a {data['FOLDER_OUT']}/arx2 -t{data['TYPE']}",
                                "Everything is Ok")
        for i in make_files:
            res.append(ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                                    f"{data['FOLDER_OUT']}; 7z l arx2.{data['TYPE']}", i))
        assert res1 and all(res), "test3 FAIL"

    def test_step4(self, clear_folders, make_files, start_time):
        # test4
        res = []
        res1 = ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                                f"cd {data['FOLDER_TST']}; 7z a {data['FOLDER_OUT']}/arx2.7z",
                                "Everything is Ok")
        res2 = ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                                f"{data['FOLDER_OUT']}; 7z x arx2.7z -o{data['FOLDER_2']} -y",
                                "Everything is Ok")
        for i in make_files:
            res.append(ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                                    f"ls {data['FOLDER_1']}", i))
        assert res1 and res2 and all(res), "test4 FAIL"

    def test_step5(self, clear_folders, make_files, start_time):
        # test5
        res = []
        for i in make_files:
            res.append(ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                                    f"cd {data['FOLDER_TST']}; 7z h {i}", "Everything is Ok"))
            hash = ssh_getout(data["IP"], data["USER"], data["PASSWD"],
                              f"cd {data['FOLDER_TST']}; crc32 {i}").upper()
            res.append(ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                                    f"cd {data['FOLDER_TST']}; 7z h {i}", hash))
        assert all(res), "test5 FAIL"

    def test_step6(self, start_time):
        # test6
        assert ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                            f"{data['FOLDER_OUT']}; 7z t arx2.7z", "Everything is Ok"), "test6 FAIL"

    def test_step7(self, start_time):
        # test7
        assert ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                            f"{data['FOLDER_TST']}; 7z u arx2.7z", "Everything is Ok"), "test7 FAIL"

    def test_step8(self, start_time):
        # test8
        assert ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                            f"{data['FOLDER_OUT']}; 7z d arx2.7z", "Everything is Ok"), "test8 FAIL"

    def test_step99(self, start_time):
        res1 = ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                            "echo '111' | sudo -S dpkg -r p7zip-full","Удаляется")
        res2 = ssh_checkout(data["IP"], data["USER"], data["PASSWD"],
                            "echo '111' | sudo -S dpkg -s p7zip-full","Status: deinstall ok")
        self.save_log(start_time, "log99.txt")
        assert res1 and res2, "test99 FAIL"


