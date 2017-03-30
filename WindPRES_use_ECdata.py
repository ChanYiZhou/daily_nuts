#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- version: python2.7 -*-


import os
import time
import shapefile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np 
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter,LatitudeFormatter
from mpl_toolkits.basemap import Basemap
from datetime import datetime,timedelta


# 导入自定义模块
from ECMWF_PRES import *

# 设置全局变量
# 地表等压面位势高度，levnum = 11; 850hPa, levnum = 18; 500hPa, levnum = 17;
LevNum = 17
ECres = 0.25 # unit is deg, 数据空间分辨率
SLON, ELON = 104.25, 112.25
SLAT, ELAT = 20.5, 27.0
NLONS = (ELON - SLON)/ECres + 1
NLATS = (ELAT - SLAT)/ECres + 1
NLONS, NLATS = int(NLONS), int(NLATS)
srcDir = os.path.join(r'/Users/chan/Desktop','ECdata_Plot','src')
shpDir = os.path.join(r'/Users/chan/Desktop','ECdata_Plot','src','shp')  # shapefile的路径
OutFigDir = os.path.join(r'/Users/chan/Desktop','ECdata_Plot','figs','pres') # 输出图片的路径
Atime = range(0,242,12) # 风场的预报时效
Atime = [str(_).zfill(3) for _ in Atime]
Map = Basemap(projection='cyl', resolution='c', llcrnrlat=SLAT,
            urcrnrlat=ELAT, llcrnrlon=SLON, urcrnrlon=ELON)

# 风速等级分类
grade_label = ['0', '1', '2', '3-4', '5-6', '7-8', '9-10', '11-12', 
    '13-14', '15-16', '17-18', '>=19', '21-22', '23-24', 
    '25-26', '27-28']

# 配置汉字字体，根据中文字体文件位置来配置，须自行设定
MYFONTFILE = srcDir+'/msyh.ttc'
FONTWeight = ['ultralight','extra bold']
FONTSize = [9, 12]
MYFONT,MYFONT_TITLE = [
    matplotlib.font_manager.FontProperties(fname=MYFONTFILE, size=FONTSize[i], weight=FONTWeight[i])
    for i in range(len(FONTSize))]

def plt_WndBarb(XIn, YIn, U, V, timestr):
	fig = plt.figure()
	ax = fig.add_axes([0.1, 0.1, 0.70, 0.75],projection=ccrs.PlateCarree())

	Map.readshapefile(os.path.join(shpDir,'bou2_4p'), name='whatever', drawbounds=True,
	                linewidth=0.5, color='black')

	ax.barbs(XIn, YIn, U, V, length=5, pivot='tip', flagcolor='r',
              barbcolor=['b', 'b'], barb_increments=dict(half=1, full=2, flag=10))

	# 标注经纬度坐标轴
	ax.set_xticks([106, 108, 110, 112], crs=ccrs.PlateCarree())
	ax.set_yticks([21, 23, 25, 27], crs=ccrs.PlateCarree())
	# zero_direction_label用来设置经度的0度加不加E和W
	lon_formatter = LongitudeFormatter(zero_direction_label=False)
	lat_formatter = LatitudeFormatter()
	ax.xaxis.set_major_formatter(lon_formatter)
	ax.yaxis.set_major_formatter(lat_formatter)

	axm = plt.gca()
	xlim, ylim = axm.get_xlim(), axm.get_ylim()
	fcstdates = timestr[:8]+'_'+timestr[8:10]
	hours = timestr[-2:]
	plt.text(xlim[0]+(xlim[1]-xlim[0])*0.25, ylim[1]+(ylim[1]-ylim[0])*0.08,
	    u'广 西 全 区 未 来 '+hours+u' 小 时 500hPa 风 场 预 报', fontproperties=MYFONT_TITLE)
	plt.text(xlim[0]+(xlim[1]-xlim[0])*0.02, ylim[1]+(ylim[1]-ylim[0])*0.02,
	    u'起 报 时 间 ：'+fcstdates, fontproperties=MYFONT)

    # 添加风羽图例
	naxes = len(grade_label)
	fig.subplots_adjust(top=0.75, bottom=0.15, left=0.78, right=0.95)
	for iplt in range(naxes):
	  axn = fig.add_subplot(naxes, 1, iplt+1)
	  axn.set_xlim(0.0,1.0)
	  axn.set_ylim(0.0,1.0)
	  if iplt == 0:
	    axn.barbs(0.5,0.5,0.0,0.0, flagcolor='r',
	       barbcolor=['b', 'b'], barb_increments=dict(half=1, full=2, flag=10)) # 绘制0级风，散点图
	    tm = plt.gca()
	    xlim, ylim = tm.get_xlim(), tm.get_ylim()
	    plt.text((xlim[1]-xlim[0])*0.20, ylim[1]+(ylim[1]-ylim[0])*0.15,u'风 速 : 米每秒',fontproperties=MYFONT)
	  elif iplt == 1:
	    line, = axn.plot([0.26,0.5], [0.5,0.5], '-', color='b')          # 绘制1级风，直线图
	  else:
	    x = (iplt-1)* 1.0
	    axn.barbs(0.5,0.5,x,0.0, flagcolor='r',
	       barbcolor=['b', 'b'], barb_increments=dict(half=1, full=2, flag=10))

	  axn.text(0.60,0.36,grade_label[iplt])
	  axn.xaxis.set_visible(False)
	  axn.yaxis.set_visible(False)
	  axn.set_frame_on(False)

        # plt.show()
	flename = timestr + '_' + '500Windbarb.png'
	OutFigPath = os.path.join(OutFigDir,fcstdates)
	if not os.path.exists(OutFigPath): os.makedirs(OutFigPath)
	plt.savefig(OutFigPath+'/'+flename, bbox_inches='tight', pad_inches=0.3, dpi=300)
	plt.clf()
	plt.close(fig)
	


def plt_WndVector(X,Y,U,V,timestr):
	fig = plt.figure()
	ax = plt.subplot(1,1,1,projection=ccrs.PlateCarree())

	Map.readshapefile(os.path.join(shpDir,'bou2_4p'), name='whatever', drawbounds=True,
	                linewidth=0.5, color='black')
	M = np.hypot(U,V)
	#ax.quiver(X, Y, U, V, M, transform=vector_crs, regrid_shape=30)
	Q = ax.quiver(X, Y, U, V, M, units='x', pivot='tip', width=0.012,
	    scale=4 / 0.15)
	qk = ax.quiverkey(Q, 0.86, 0.92, 2.5, r'$10 \frac{m}{s}$', labelpos='E',
	    coordinates='figure')

	# 标注坐标轴
	ax.set_xticks([106, 108, 110, 112], crs=ccrs.PlateCarree())
	ax.set_yticks([21, 23, 25, 27], crs=ccrs.PlateCarree())
	# zero_direction_label用来设置经度的0度加不加E和W
	lon_formatter = LongitudeFormatter(zero_direction_label=False)
	lat_formatter = LatitudeFormatter()
	ax.xaxis.set_major_formatter(lon_formatter)
	ax.yaxis.set_major_formatter(lat_formatter)

	axm = plt.gca()
	xlim, ylim = axm.get_xlim(), axm.get_ylim()
	fcstdates = timestr[:8]+'_'+timestr[8:10]
	hours = timestr[-2:]
	plt.text(xlim[0]+(xlim[1]-xlim[0])*0.25, ylim[1]+(ylim[1]-ylim[0])*0.08,
	    u'广 西 全 区 未 来 '+hours+u' 小 时 500hPa 风 场 预 报 图', fontproperties=MYFONT_TITLE)
	plt.text(xlim[0]+(xlim[1]-xlim[0])*0.02, ylim[1]+(ylim[1]-ylim[0])*0.02,
	    u'起 报 时 间 ：'+fcstdates, fontproperties=MYFONT)

	# plt.show()
	flename = timestr + '_' + '500WindVector.png'
	OutFigPath = os.path.join(OutFigDir,fcstdates)
	plt.savefig(OutFigPath+'/'+flename, bbox_inches='tight', pad_inches=0.3, dpi=300)
	plt.clf()
	plt.close(fig)
	


def main():
	# 1. set time
	#CurrTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	# year, month = int(CurrTime[:4]), int(CurrTime[5:7])
	# day, hour = int(CurrTime[8:10]), CurrTime[11:13]

	year, month, day, prehour = 2017, 3, 6, '00'
	for hours in Atime[2:3]:
	    # 2. read ecmwf data
		# hours, year, month, day, prehour = '24', 2017, 3, 6, '00'
		try:
			output = readECMWF_inbox(hours, year, month, day, prehour, LevNum)
		except Exception as e:
			raise e
			continue
		UIn = np.array(output['uwind'])
		VIn = np.array(output['vwind'])
		lons = output['lons']
		lats = output['lats'][::-1]

		latsize = len(list(set(lats)))
		lonsize = len(list(set(lons)))
		SLAT_ID, SLON_ID = lats.index(SLAT)/lonsize, lons.index(SLON)
		ELAT_ID, ELON_ID = lats.index(ELAT)/lonsize, lons.index(ELON)

		XIn = np.arange(SLON,ELON+0.5*ECres,ECres)
		YIn = np.arange(SLAT,ELAT+0.5*ECres,ECres)
		XIn, YIn = np.meshgrid(XIn, YIn)

		uwnd = UIn.reshape((latsize,lonsize))[::-1,:][SLAT_ID:ELAT_ID+1,SLON_ID:ELON_ID+1]
		vwnd = VIn.reshape((latsize,lonsize))[::-1,:][SLAT_ID:ELAT_ID+1,SLON_ID:ELON_ID+1]

		# 3. plot uv wind at 10m level
		fcstdates = datetime(year,month,day,int(prehour)).strftime('%Y%m%d%H')
		timestr = fcstdates+'_'+ hours.zfill(3)
		plt_WndBarb(XIn[::3,::3],YIn[::3,::3],uwnd[::3,::3],vwnd[::3,::3],timestr)
		# plt_WndVector(XIn[::4,::4],YIn[::4,::4],uwnd[::4,::4],vwnd[::4,::4],timestr)

if __name__ == '__main__':
    main()
