# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import qrcode
import os


log_file_name = 'log_python.txt'
# 清空文件内容
def clearFile():
    f = open(log_file_name, 'w+')
    f.truncate()
    f.close()

# 输出内容到文件
def dumpToFile(content):
    f = open(log_file_name, 'a')
    f.write(content + '\n')
    f.close()


# 编译类型（debug还是release）
build_type = sys.argv[1]
# 获得编译时间
build_time = sys.argv[2]
# 二维码存储的地址
or_code_path = sys.argv[3] + '/' + build_type + '/' + build_time
# apk名称
apkName = sys.argv[4]

apk_path = 'http://10.41.12.20:8080/jenkinsApk/testJenkins'+ '/' + build_type + '/' + build_time + '/' + apkName

if not os.path.exists(or_code_path):
    os.makedirs(or_code_path)

or_code_file_path = or_code_path + '/' + build_time + '.png'
if os.path.exists(or_code_file_path):
    os.remove(or_code_file_path)
clearFile()
dumpToFile(apk_path)
dumpToFile(or_code_file_path)

# 生成二维码
img = qrcode.make(apk_path)
img.save(or_code_file_path)