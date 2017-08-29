# coding:utf8

# 广东省的RH色标
# attention:
# 使用时调整boundaries参数

# 相对湿度的色标分级
StdRGB_RH = [
[255, 255, 255], # <70%
[0, 255, 175], # 70~75%
[0, 255, 58], # 75~80%
[0, 255, 23], # 80~85%
[168, 255, 0], # 85~90%
[255, 286, 0], # 90~95%
[255, 0, 0]  # 95~100%
[255, 0, 0]  # >100%
]



if __name__ == '__main__':
        import matplotlib.pyplot as plt
        import matplotlib as mpl
        import numpy as np

        fig = plt.figure(figsize=(8, 3))
        ax = fig.add_axes([0.05, 0.475, 0.9, 0.15])

        over_RGB = list(np.array(StdRGB_RH[-1])/255.0)