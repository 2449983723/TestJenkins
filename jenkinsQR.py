# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import qrcode
import os
from PIL import Image
import traceback

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

try:
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
    dumpToFile('-----------------generate start--------------------')
    dumpToFile(apk_path)
    dumpToFile(or_code_file_path)

    # 生成二维码
    # img = qrcode.make(apk_path)
    # img.save(or_code_file_path)

    qr = qrcode.QRCode(version=5,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=8,border=4)
    qr.add_data(apk_path)
    qr.make(fit=True)

    # 获得Image实例并把颜色模式转换为RGBA
    img = qr.make_image()
    img = img.convert("RGBA")

    # 打开logo文件
    icon = Image.open("ic_launcher.png")

    # 计算logo的尺寸
    img_w,img_h = img.size
    factor = 4
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)

    # 比较并重新设置logo文件的尺寸
    icon_w,icon_h = icon.size
    if icon_w >size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    icon = icon.resize((icon_w,icon_h),Image.ANTIALIAS)

    # 计算logo的位置，并复制到二维码图像中
    w = int((img_w - icon_w)/2)
    h = int((img_h - icon_h)/2)
    icon = icon.convert("RGBA")
    img.paste(icon,(w,h),icon)

    # 保存二维码
    img.save(or_code_file_path)

    dumpToFile('-----------------generate end--------------------')
except Exception, e:
    dumpToFile('traceback.format_exc():\n%s' % traceback.format_exc())