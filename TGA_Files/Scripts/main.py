#### Script for file format conversion for TGA (machine 1) ####

import glob, os
import xlrd
from collections import OrderedDict
import simplejson as json 
import pprint
import tkFileDialog
import tkSimpleDialog
from Tkinter import *	
import dicttoxml
import lxml.etree as etree

class TGApp:
	def __init__(self):
		self.sh = None
		self.root = Tk()
		self.label = Label(self.root, text = "Enter Sheet Number")
		self.label.pack()

		self.entry = Entry(self.root)
		self.entry.pack()

		self.button = Button(self.root, text = "Load", command = self.load_sheet)
		self.button.pack()

	def load_sheet(self):
		self.sheet = self.entry.get()
		print "Sheet No: %s"%self.sheet
		if self.sheet.__class__ == type(""):
			
			self.sh = self.wb.sheet_by_index(int(self.sheet) - 1)
			self.button2 = Button(self.root, text = "Init JSON Transfer", command = self.runJSON)
			self.button2.pack()
			
		else:
			print 'Eee Roar!'

	def run(self):
		print "Please select a file"
		self.file_path = tkFileDialog.askopenfilename()
		self.wb = xlrd.open_workbook(filename = self.file_path)
		print self.file_path
		self.root.mainloop()


	def runJSON(self):

		os.chdir(os.path.dirname(os.getcwd()))
		for file in glob.glob("Data_Files/Excel/*.xlsx"):

			self.file_path = file
			sequence = file.split("/")[-1].split("_")[0]

			TGA_Data = {"dataset":self.file_path.split("/")[-1]}

			TGA_Header = {}
			TGA_Content = []

			#FileName
			TGA_Header["filename"] = self.sh.cell_value(0, 2)

			#Experiment
			TGA_Header["experiment"] = {}
			TGA_Header["experiment"]["name"]= self.sh.cell_value(1, 2)
			TGA_Header["experiment"]["id"]= self.sh.cell_value(3, 2)
			TGA_Header["experiment"]["started"]= self.sh.cell_value(18, 2)

			#Operator
			TGA_Header["operator"] = self.sh.cell_value(2, 2)

			#Sample Name
			TGA_Header["sample"] = {}
			TGA_Header["sample"]["name"] = self.sh.cell_value(4, 2)
			TGA_Header["sample"]["lot"] = self.sh.cell_value(5, 2)

			#Notes
			TGA_Header["notes"] = self.sh.cell_value(6, 2)

			#Pump
			TGA_Header["pump"] = self.sh.cell_value(7, 3)

			#Absorbate
			TGA_Header["absorbate"] = self.sh.cell_value(8, 2)

			#Temp
			TGA_Header["temperature"] = {}
			TGA_Header["temperature"]["drying"] = self.sh.cell_value(9, 2)
			TGA_Header["temperature"]["run"] = {}
			TGA_Header["temperature"]["run"]["value"] = self.sh.cell_value(13, 2)
			TGA_Header["temperature"]["run"]["unit"] = self.sh.cell_value(13, 3)

			#Heating Rate
			TGA_Header["heating_rate"] = {}
			TGA_Header["heating_rate"]["value"] = self.sh.cell_value(10, 2)
			TGA_Header["heating_rate"]["unit"] = self.sh.cell_value(10, 3)

			#Max Time
			TGA_Header["max_time"] = {}
			TGA_Header["max_time"]["drying"] = {}
			TGA_Header["max_time"]["drying"]["value"] = self.sh.cell_value(11, 2)
			TGA_Header["max_time"]["drying"]["unit"] = self.sh.cell_value(11, 3)
			TGA_Header["max_time"]["equil"] = {}
			TGA_Header["max_time"]["equil"]["value"] = self.sh.cell_value(14, 2)
			TGA_Header["max_time"]["equil"]["unit"] = self.sh.cell_value(14, 3)

			#Equal Crit
			TGA_Header["equil_crit"] = []

			equil_1 = {}
			equil_1["value1"] = self.sh.cell_value(12, 2)
			equil_1["unit1"] = self.sh.cell_value(12, 3)
			equil_1["value2"] = self.sh.cell_value(12, 4)
			equil_1["unit2"] = self.sh.cell_value(12, 5)

			equil_2 = {}
			equil_2["value1"] = self.sh.cell_value(15, 2)
			equil_2["unit1"] = self.sh.cell_value(15, 3)
			equil_2["value2"] = self.sh.cell_value(15, 4)
			equil_2["unit2"] = self.sh.cell_value(15, 5)

			TGA_Header["equil_crit"].append(equil_1)
			TGA_Header["equil_crit"].append(equil_2)


			#Pres Steps
			steps = self.sh.cell_value(16, 2)[1:len(self.sh.cell_value(16, 2))-1]
			TGA_Header["pressure_steps"] = steps.split(",")

			#Data Logging Interval
			TGA_Header["data_logging_interval"] = {}
			TGA_Header["data_logging_interval"]["value1"] = self.sh.cell_value(17, 2)
			TGA_Header["data_logging_interval"]["unit1"] = self.sh.cell_value(17, 3)
			TGA_Header["data_logging_interval"]["value2"] = self.sh.cell_value(17, 4)
			TGA_Header["data_logging_interval"]["unit2"] = self.sh.cell_value(17, 5)

			#Run Started
			TGA_Header["run_started"] = self.sh.cell_value(19, 2)

			TGA_Data["header"] = TGA_Header


			#Content

			begin = 23

			# print str(begin)
			# print self.sh.cell_value(23, 0)

			while 1:
				try:
					row = {}

					row["index"] = begin -22
					row["elap_time"] = {}
					row["elap_time"]["unit"] = self.sh.cell_value(22, 0)
					row["elap_time"]["value"] = self.sh.cell_value(begin, 0)

					row["weights"] = []
					weight1 = {}
					weight1["prefix"] = ""
					weight1["unit"] = self.sh.cell_value(22, 1)
					weight1["value"] = self.sh.cell_value(begin, 1)
					row["weights"].append(weight1)

					weight2 = {}
					weight2["prefix"] = ""
					weight2["unit"] = self.sh.cell_value(22, 2)
					weight2["value"] = self.sh.cell_value(begin, 2)
					row["weights"].append(weight2)

					weight3 = {}
					weight3["prefix"] = "Corr."
					weight3["unit"] = self.sh.cell_value(22, 7)
					weight3["value"] = self.sh.cell_value(begin, 7)
					row["weights"].append(weight3)

					weight4 = {}
					weight4["prefix"] = "Corr."
					weight4["unit"] = self.sh.cell_value(22, 8)
					weight4["value"] = self.sh.cell_value(begin, 8)
					row["weights"].append(weight4)

					row["pressure"] = {}
					row["pressure"]["unit"] = self.sh.cell_value(22, 3)
					row["pressure"]["value"] = self.sh.cell_value(begin, 3)

					row["sample_temp"] = {}
					row["sample_temp"]["unit"] = self.sh.cell_value(22, 4)
					row["sample_temp"]["value"] = self.sh.cell_value(begin, 4)

					row["Z"] = {}
					row["Z"]["unit"] = self.sh.cell_value(22, 6)
					row["Z"]["value"] = self.sh.cell_value(begin, 6)

					TGA_Content.append(row)
					begin += 1
				except:
					break


			#End content
			TGA_Data["content"] = TGA_Content

			with open('Data_Files/JSON/%s_DataSet_TGA.json'%sequence, 'w') as f:
				f.write(json.dumps(TGA_Data, sort_keys=True, indent=4, separators=(',', ': ')))

			with open('Data_Files/XML/%s_DataSet_TGA.xml'%sequence, 'w') as f:
				f.write(dicttoxml.dicttoxml(TGA_Data))

			x = etree.parse("Data_Files/XML/%s_DataSet_TGA.xml"%sequence)

			with open('Data_Files/XML/%s_DataSet_TGA.xml'%sequence, 'w') as f:
				f.write(etree.tostring(x, pretty_print = True))				


if __name__ == '__main__':

	TGInstance = TGApp()
	TGInstance.run()




			