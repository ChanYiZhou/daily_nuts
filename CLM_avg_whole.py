#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -*- version: python2.7 -*-

# ================================== #
# purpose:                           #
#	do annual and monthly mean  #
#	for PenLin                       #
# ================================== #

import os
import pandas as pd
import numpy as np
from datetime import datetime

# define global vars
datadir = os.path.join(r'/Users/chan','Desktop','Businee_doing',
	'Self_works','For_Peilin','Datasets')
Diamod = ['Sand', 'CLM']
Reg1 = ['GanSu','QingHai','XinJiang_XiZang'] # for Sand kind
COLS1 = ['station','date','dust','dust_storm']
Reg2 = ['GanSu_QingHai','XinJiang_XiZang'] # for CLM kind
COLS2 = ['station','date','temp','wind','prep']

def main():
	for ikid in Diamod[:1]:
		if ikid is 'Sand':
			flnames = [_+'_'+ikid+'.txt' for _ in Reg1]
			COLS = COLS1
		else:
			flnames = [_+'_'+ikid+'.txt' for _ in Reg2]
			COLS = COLS2

		for ifl in flnames:
			# 1. read data from files
			print "---"*20
			print "file to be read is: ",ifl
			ALLdata = pd.read_table(os.path.join(datadir,ifl),skiprows=1,
				header=None,delim_whitespace=True)
			# print ALLdata

			# 2. compute and output the monthly and annual mean value from daily data
			STD = pd.Series(ALLdata[0])
			AllSTD = list(set(list(STD)))
			# print AllSTD

			dataM, dataY = [], []
			for istd in AllSTD:
				print "站点名: ",istd
				Indata = ALLdata[ALLdata[0] == istd]
				YEAR = list(Indata[1])
				Month = list(Indata[2])
				Day = list(Indata[3])
				Indates = [datetime(YEAR[im],Month[im],Day[im]) for im in range(len(YEAR))]
				Indat0 = []				
				for irec in range(len(Indates)):
					therec = []
					therec.append(istd); therec.append(Indates[irec])
					for icol in range(2,len(COLS)):
						colData = list(Indata[icol+2])[irec]
						if colData >= 30000:
							if colData == 32766:
								colData = np.nan
							elif colData >= 32000: # 降水微量或者纯雾露霜
								colData = 0
							elif colData >= 31000: # 雨雪总量
								colData = colData - 31000
							else:
								colData = colData - 30000 # 雨夹雪或者雪暴
						therec.append(colData)
					Indat0.append(therec)

				Indat = pd.DataFrame(Indat0,columns=COLS,index=Indates)
				# print Indat.shape
				Indat1 = Indat.resample('D').mean()# 重采样补充缺失日值记录
				# print Indat1

				if ikid == 'CLM':
					# --- 计算月均值
					IndatM = Indat1[['station','temp','wind']].copy().resample('M').mean()
					IndatRM = Indat1[['prep']].copy().resample('M').sum()
					IndatM['prep'] = IndatRM['prep']*0.1
					# print IndatM
					# --- 计算年均值
					IndatY = Indat1[['station','temp','wind']].copy().resample('A').mean()
					IndatRY = Indat1[['prep']].copy().resample('A').sum()
					IndatY['prep'] = IndatRY['prep']*0.1
					# print IndatY
				else: # 针对沙尘和沙尘暴统计
					IndatM = Indat1.resample('M').sum()
					IndatY = Indat1.resample('A').sum()

				# merge the mean value and output it
				yearlst = list(IndatY.index.map(lambda x: x.strftime('%Y')))
				# print yearlst 

				for irec in range(IndatY.shape[0]):
					therec = []
					therec.append(istd)
					therec.append(yearlst[irec])
					for icol in range(2,len(COLS)):
						therec.append(list(IndatY[COLS[icol]])[irec])
					dataY.append(therec)

				yearmonlst = list(IndatM.index.map(lambda x: x.strftime('%Y-%m')))
				# print yearmonlst
				for irec in range(IndatM.shape[0]):
					therec = []
					therec.append(istd)
					therec.append(yearmonlst[irec])
					for icol in range(2,len(COLS)):
						therec.append(list(IndatM[COLS[icol]])[irec])
					dataM.append(therec)

			# output result
			dfY = pd.DataFrame(dataY,columns=COLS)
			dfY.to_csv(os.path.join(datadir,'annual_'+ifl[:-3]+'csv'))
			dfM = pd.DataFrame(dataM,columns=COLS)
			dfM.to_csv(os.path.join(datadir,'monthly_'+ifl[:-3]+'csv'))

			print "---"*20
			print " "

if __name__ == '__main__':
	main()
