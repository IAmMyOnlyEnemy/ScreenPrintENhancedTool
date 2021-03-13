import pathlib
from os import path

def get_settings():
	''' ---------------
	Global values:
	    --------------- '''
	settings_dict = {}
	file_name = "settings.txt"

	''' ---------------
	Fill the input file if there is none:
	    --------------- '''
	if not path.exists(file_name):
		fill_file(file_name)

	''' ---------------
	Filling the dictionary values from input file:
	    --------------- '''
	fill_dict(file_name,settings_dict)

	''' ---------------
	Return the setting dictionary:
	    --------------- '''
	return settings_dict

def fill_dict(file_name,settings_dict):
	'''
	Read the settings file and fill the dictionary with global settings
	'''
	file1 = open(file_name,'r')
	lines = file1.read().splitlines()
	for line in lines:
		dict_key = line.split(": ")[0]
		dict_value = line.split(": ")[1].split(", ")

		for idx, val in enumerate(dict_value):
			try:
				int(val)
				dict_value[idx] = int(val)
			except ValueError:
				try:
					float(val)
					dict_value[idx] = float(val)
				except:
					pass

		settings_dict.update({dict_key : dict_value})
	file1.close()

def fill_file(file_name):
	file1 = open(file_name,'w')
	file1.writelines("opt1_dimmension: 350, 200, 900, 550\n")
	file1.writelines("opt2_dimmension: 460, 150, 1000, 600\n")
	file1.writelines("opt3_dimmension: 100, 50, 1200, 800\n")
	file1.writelines("screen_option: opt1\n")
	file1.writelines("checkbox_options: 0, 0, 0, 0\n")
	file1.writelines("screen_list: Print1, Print2, Print3, Print4, Print5\n")
	file1.writelines("my_screens: CONT, SAVE, ZAVE, TREC, ZREC, TREG, TRGU, TBLT, TREV, TBER, ZBER\n")
	file1.writelines("active_window: 198392, Google\n")
	file1.writelines("app_colour: LightCyan2\n")
	file1.writelines("save_path: {0}".format(pathlib.Path().absolute()))
	file1.close()

def fill_file_from_dict(file_name,settings_dict):
	file1 = open(file_name,'w')
	for item in settings_dict:
		newline1 = item + ": "
		for subitem in settings_dict[item]:
			newline1 += str(subitem) + ", "
		newline1 = newline1[:-2]
		file1.writelines(newline1 + "\n")
	file1.close()

if __name__== "__main__":
	get_settings()