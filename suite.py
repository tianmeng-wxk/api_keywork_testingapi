from HTMLTestRunner import HTMLTestRunner
import unittest,os,time
from testcase import Test_api
#curPath = os.path.abspath(os.path.dirname(__file__))

# path = curPath+"../../test_case"
# discover = unittest.defaultTestLoader.discover(start_dir=path, pattern="read_*.py")#在path目录下运行以read开头的文件,运行discover

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(Test_api))
    report_path = "../report/"
    report_file = report_path+"{}_html_report.html".format(time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime()))
    if not os.path.exists(report_path):
        os.mkdir(report_path)
    else:
        pass

    with open(report_file, 'wb')as file:
        runner = HTMLTestRunner(stream=file, title="特斯汀接口测试", description="特斯汀接口测试")
        runner.run(suite)
    return report_file
suite()