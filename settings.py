import json
import os

slots = {}
options = {}
gui = {}


def GetSlotsFilePath():
	local_dir = os.path.dirname(os.path.abspath(__file__))
	settings_file_path = os.path.join(os.path.normpath(local_dir), "exporter_slots.json")

	if (os.path.exists(settings_file_path)):
		return settings_file_path

	return None


def GetConfFilePath():
	local_dir = os.path.dirname(os.path.abspath(__file__))
	settings_file_path = os.path.join(os.path.normpath(local_dir), "exporter_conf.json")

	if (os.path.exists(settings_file_path)):
		return settings_file_path

	return None


def LoadSettings():
	# Parse slots file.
	path = GetSlotsFilePath()
	if (path == None):
		import errno
		raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

	# print("Path: " + str(path))
	with open(path, "r") as slots_file:
		global slots
		slots = json.load(slots_file)
		# slots_file.read().encode('ascii', errors='ignore')
		# print(json.dumps(slots, sort_keys=False, indent=2))

		for key, value in slots.items():
			# print(key, ":", value)
			# print(key)
			# print(value["selected"])
			pass

	# Parse conf file.
	path = GetConfFilePath()
	if (path == None):
		import errno
		raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

	with open(path, "r") as conf_file:
		conf = json.load(conf_file)

		global options
		options = conf["options"]

		global gui
		gui = conf["gui"]
		# print(options["compactslotsize"])
		# print(options["lastprojectpath"])

	pass


def SaveSettings():
	# Save slots file.
	path = GetSlotsFilePath()
	with open(path, "w") as write_file:

		json.dump(slots, indent=4, fp=write_file)

	# Save conf file.
	path = GetConfFilePath()
	with open(path, "w") as write_file:
		settings = {}
		settings["options"] = options
		settings["gui"] = gui

		json.dump(settings, indent=4, fp=write_file)

	pass
