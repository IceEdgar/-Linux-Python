from checkers import checkout, getout, checkout_negative
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, make_folders, clear_folders, make_files, print_time):
        # test1
        res1 = checkout(f"cd {data['FOLDER_TST']}; 7z a {data['FOLDER_OUT']}/arx2", "Everything is Ok")
        res2 = checkout(f"ls {data['FOLDER_OUT']}", "arx2.7z")
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(checkout(f"cd {data['FOLDER_TST']}; 7z a {data['FOLDER_OUT']}/arx -t{data['TYPE']}", "Everything is Ok"))
        res.append(checkout(f"cd {data['FOLDER_OUT']}; 7z e arx.{data['TYPE']} -o{data['FOLDER_1']} -y", "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f"ls {data['FOLDER_1']}", item))
        assert all(res)

    def test_step3(self, clear_folders, make_files):
        # test3
        res = []
        res.append(checkout(f"cd {data['FOLDER_TST']}; 7z a {data['FOLDER_OUT']}/arx -t{data['TYPE']}", "Everything is Ok"))
        for i in make_files:
            res.append(checkout(f"cd {data['FOLDER_OUT']}; 7z l arx.{data['TYPE']}", i))
        assert all(res), "test3 FAIL"

    def test_step4(self, clear_folders, make_files, make_subfolder):
        # test4
        res = []
        res.append(checkout(f"cd {data['FOLDER_TST']}; 7z a {data['FOLDER_OUT']}/arx -t{data['TYPE']}", "Everything is Ok"))
        res.append(checkout(f"cd {data['FOLDER_OUT']}; 7z x arx.{data['TYPE']} -o{data['FOLDER_2']} -y", "Everything is Ok"))
        for i in make_files:
            res.append(checkout(f"ls {data['FOLDER_2']}", i))
        res.append(checkout(f"ls {data['FOLDER_2']}", make_subfolder[0]))
        res.append(checkout(f"ls {data['FOLDER_2']}/{make_subfolder[0]}", make_subfolder[1]))
        assert all(res), "test4 FAIL"

    def test_step5(self, clear_folders, make_files):
        # test5
        res = []
        for i in make_files:
            res.append(checkout(f"cd {data['FOLDER_TST']}; 7z h {i}", "Everything is Ok"))
            hash = getout(f"cd {data['FOLDER_TST']}; crc32 {i}").upper()
            res.append(checkout(f"cd {data['FOLDER_TST']}; 7z h {i}", hash))
        assert all(res), "test5 FAIL"

    def test_step6(self):
        # test6
        assert checkout(f"cd {data['FOLDER_OUT']}; 7z t arx2.7z", "Everything is Ok"), "test6 FAIL"

    def test_step7(self):
        # test7
        assert checkout(f"cd {data['FOLDER_TST']}; 7z u arx2.7z", "Everything is Ok"), "test7 FAIL"

    def test_step8(self):
        # test8
        assert checkout(f"cd {data['FOLDER_OUT']}; 7z d arx2.7z", "Everything is Ok"), "test8 FAIL"


class TestNegative:
    def test_neg1(self):
        # test1
        assert checkout_negative(f"{data['FOLDER_OUT']}; 7z e arx2bad.7z -o{data['FOLDER_1']} -y", "ERROR"), "test1 FAIL"

    def test_neg2(self):
        # test2
        assert checkout_negative(f"{data['FOLDER_OUT']}; 7z t arx2bad.7z", "ERROR"), "test2 FAIL"