import pathlib
from os import path

def get_settings():
	''' ---------------
	Global values:
	    --------------- '''
	settings_dict = {}
	file_name = "Settings\\settings.txt"

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
	file1.writelines("TSO_dimmension: 460, 150, 1000, 600\n")
	file1.writelines("CICS_dimmension: 350, 200, 900, 550\n")
	file1.writelines("TSO_option: CICS\n")
	file1.writelines("checkbox_options: 0, 0, 0, 0\n")
	file1.writelines("screen_list: CONT, SAVE, TREC, TBLT, TREV\n")
	file1.writelines("form_dimensions: 400, 250\n")
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