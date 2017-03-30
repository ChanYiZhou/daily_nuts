# coding:utf8

# attention:
# 使用时调整boundaries参数

# 降雨等级色标，适用24小时、12小时及6小时降雨量
StdRGB_aRain = [
[165, 243, 141], #  小雨
[61, 185, 63], # 中雨
[99, 184, 249], # 大雨
[0, 0, 254], # 暴雨
[243, 5, 238], # 大暴雨
[129, 0, 64] # 特大暴雨
]


if __name__ == '__main__':
	import matplotlib.pyplot as plt
	import matplotlib as mpl
	import numpy as np

	fig = plt.figure(figsize=(8, 3))
	ax = fig.add_axes([0.05, 0.475, 0.9, 0.15])

	over_RGB = list(np.array(StdRGB_aRain[-1])/255.0)
	under_RGB = list(np.array(StdRGB_aRain[0])/255.0)
	Bcmap_RGB = StdRGB_aRain[1:len(StdRGB_aRain)]
	Bcmap_RGB = np.array(Bcmap_RGB)/255.0
	Bcmap_RGB = [list(_) for _ in Bcmap_RGB]
	cmap = mpl.colors.ListedColormap(Bcmap_RGB)
	cmap.set_over(tuple(over_RGB))
	cmap.set_under(tuple(under_RGB))

	bounds = range(10,50,10) # 不同等级对应的降雨值
	norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
	cb = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
	                                norm=norm,
	                                boundaries=[-1] + bounds + [17],
	                                extend='both',
	                                extendfrac='auto',
	                                ticks=bounds,
	                                spacing='uniform',
	                                orientation='horizontal')
	cb.set_label('Standard Colorbars of Rain, from CMA')

	plt.show()