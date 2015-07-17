#### Script for plotting machine produced data ####

#### TGA (machine 1) ####

import glob, os
from collections import OrderedDict, Counter
import simplejson as json 	
import matplotlib
import matplotlib.markers as mark
from matplotlib.markers import MarkerStyle
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import show, plot, ion
import pylab
import numpy as np


class createSimplePlot: 
	
	def __init__(self, congo, horn):
		continue

	def adsPlotVals(self):
		for i in range(len(adsMainList)):
			self.adsPresList_x = tuple(adsMainList[i])
			self.adsPresVals_x = adsPresList_x[0]

			self.adsConcList_y = tuple(adsMainList[i])
			self.adsConcVals_y = adsConcList_y[1]

	
	def desPlotVals(self):
		for j in range(len(desMainList)):
			self.desPresList_x = tuple(desMainList[i])
			self.desPresVals_x = desPresList_x[0]

			self.desConcList_y = tuple(desMainList[i])
			self.desConcVals_y = desConcList_y[1]





	def simplePlot(presList, concList):





	os.chdir(os.path.dirname(os.getcwd()))
	print os.getcwd()

	for file in glob.glob("TGA/Data_Files/JSON/json_aliq/*.json"):
		json_file_pathTGA = file
		sequence1 = file.split("/")[-1].split("_")[0]
		sequence2 = file.split("/")[-1].split("_")[1]

		fileList = []
		fileList.append(file)

		with open('%s'%json_file_pathTGA) as json_data_fileTGA:    
			json_dictTGA = json.load(json_data_fileTGA)


		begin3 = 1

		pressure_listTGA = []
		conc_listTGA = []


		while True: 
			try:
				content_dictTGA = json_dictTGA["content"][begin3 - 1]

				conc_dictTGA = content_dictTGA.get('weights')[3]
				conc_valTGA = conc_dictTGA.get('value')

				pressure_dictTGA = content_dictTGA.get('pressure')
				pressure_valTGA = pressure_dictTGA.get('value')

				pressure_listTGA.append(pressure_valTGA)
				conc_listTGA.append(conc_valTGA)
					
				begin3 +=1

			except:
				break


		total = len(pressure_listTGA)

		pressure_listTGA1 = []
		conc_listTGA1 = []

		pressure_listTGA2 = []
		conc_listTGA2 = []
		
		boundary = -1
		for t in range(total):
			if t == total - 1:
				break
			elif t > 0:
				if pressure_listTGA[t] >= pressure_listTGA[t + 1] and pressure_listTGA[t] >= pressure_listTGA[t - 1]:
					boundary = t
					break
				if pressure_listTGA[t] <= pressure_listTGA[t + 1] and pressure_listTGA[t] <= pressure_listTGA[t - 1]:
					boundary = t
					break

		pressure_listTGA1 = list(pressure_listTGA[0:boundary])
		pressure_listTGA2 = list(pressure_listTGA[boundary + 1:len(pressure_listTGA) - 1])

		conc_listTGA1 = list(conc_listTGA[0:boundary])
		conc_listTGA2 = list(conc_listTGA[boundary + 1:len(conc_listTGA) - 1])

		for p in range(len(fileList)):
			plt.figure(p)
			plt.plot(pressure_listTGA1, conc_listTGA1, '^g', mfc = 'g', mec = 'k', mew = .25)
			plt.plot(pressure_listTGA2, conc_listTGA2, '^g', mfc = 'none', mec = 'g', mew = 1)


		plot_pathTGA_raw = '%s/TGA/TGA_plots/Aliq_plots/Aliq_plots-original/%s_%s_originalPlot.png'\
							%(os.getcwd(), sequence1, sequence2)

		plt.axis([0, 50, 0, 3.75])
		plt.savefig('%s'%plot_pathTGA_raw)


	print "done"

if __name__ == '__main__':

