# 首先我们要用到Python的PIL库的Image模块，PIL(Python Imaging Library)库是Python的一个图像处理库。想了解PIL的详细功能介绍，可参考PIL的官方文档（虽然我也没看过，不过还是贴上来）：http://effbot.org/imagingbook/

# 图片转字符画的关键思想是将图片的灰度值与你自己设定的字符集之间建立映射关系，不同区间的灰度值对应不同的字符，之后将图片每一个像素对应的字符打印出来就是我们要的字符画啦~

# 这里提供两种方法：

# 先将彩色图片转换为黑白图片，然后直接将每个像素点的灰度值与字符集建立映射。

# 获取图片的RGB值，利用公式：

# Gray = R*0.299 + G*0.587 + B*0.114 

# 计算可得每个像素点的灰度值，之后再建立映射即可。

# -*- coding: utf-8 -*-
from PIL import Image

codeLib = '''@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. '''#生成字符画所需的字符集
count = len(codeLib)

def transform1(image_file):
  image_file = image_file.convert("L")#转换为黑白图片，参数"L"表示黑白模式
  codePic = ''
  for h in range(0,image_file.size[1]): #size属性表示图片的分辨率，'0'为横向大小，'1'为纵向
    for w in range(0,image_file.size[0]):
      gray = image_file.getpixel((w,h)) #返回指定位置的像素，如果所打开的图像是多层次的图片，那这个方法就返回一个元组
      codePic = codePic + codeLib[int(((count-1)*gray)/256)]#建立灰度与字符集的映射
    codePic = codePic+'\r\n'
  return codePic

def transform2(image_file):
  codePic = ''
  for h in range(0,image_file.size[1]):
    for w in range(0,image_file.size[0]):
      g,r,b = image_file.getpixel((w,h))
      gray = int(r* 0.299+g* 0.587+b* 0.114)
      codePic = codePic + codeLib[int(((count-1)*gray)/256)]
    codePic = codePic+'\r\n'
  return codePic


fp = open(u'暴走.jpg','rb')
image_file = Image.open(fp)
image_file=image_file.resize((int(image_file.size[0]*0.75), int(image_file.size[1]*0.5)))#调整图片大小
print u'Info:',image_file.size[0],' ',image_file.size[1],' ',count

tmp = open('tmp.txt','w')
tmp.write(transform1(image_file))
tmp.close()

