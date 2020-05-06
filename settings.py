import json
import os

slots = {}
options = {}
gui = {}


# ---------------------------------------------------------------------------------------------------------------------
# Paths.
# ---------------------------------------------------------------------------------------------------------------------
def GetSlotsFilePath():
	local_dir = os.path.dirname(os.path.abspath(__file__))
	settings_file_path = os.path.join(os.path.normpath(local_dir), "exporter_slots.json")

	return settings_file_path


def GetConfFilePath():
	local_dir = os.path.dirname(os.path.abspath(__file__))
	settings_file_path = os.path.join(os.path.normpath(local_dir), "exporter_conf.json")

	return settings_file_path


# ---------------------------------------------------------------------------------------------------------------------
# Load.
# ---------------------------------------------------------------------------------------------------------------------
def LoadSettings():
	# Parse slots file.
	path = GetSlotsFilePath()
	if (os.path.exists(path)):
		ParseSlotsJson(path)
	else:
		# import errno
		# raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		pass

	# Parse conf file.
	path = GetConfFilePath()
	if (os.path.exists(path)):
		ParseSettingsJson(path)
	else:
		# import errno
		# raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		pass

	# Check and load default settings.
	if (len(slots.keys()) == 0 or len(options.keys()) == 0 or len(gui.keys()) == 0): DefaultSettings()

	pass

def ParseSlotsJson(path):
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

def ParseSettingsJson(path):
	with open(path, "r") as conf_file:
		conf = json.load(conf_file)

		global options
		options = conf["options"]

		global gui
		gui = conf["gui"]
		# print(options["compactslotsize"])
		# print(options["lastprojectpath"])

# ---------------------------------------------------------------------------------------------------------------------
# Save.
# ---------------------------------------------------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------------------------------------------------
# Create default settings and save.
# ---------------------------------------------------------------------------------------------------------------------
def DefaultSettings():
	global slots
	slots = {
	    "diffuse": {
	        "selected": True,
	        "suffix": "_df",
	        "fill": [
	            128,
	            128,
	            128
	        ],
	        "allowSharpen": True,
	        "downscale": 1,
	        "channels": [
	            {
	                "channel": "a",
	                "source": "alpha",
	                "fill": [
	                    128,
	                    128,
	                    128
	                ]
	            }
	        ]
	    },
	    "normal": {
	        "selected": True,
	        "suffix": "_nm",
	        "fill": [
	            128,
	            128,
	            255
	        ],
	        "allowSharpen": False,
	        "downscale": 2,
	        "channels": [
	            {
	                "channel": "a",
	                "source": "glossiness",
	                "fill": [
	                    255,
	                    255,
	                    255
	                ]
	            }
	        ]
	    },
	    "alpha": {
	        "selected": False,
	        "suffix": "_alpha",
	        "fill": [
	            255,
	            255,
	            255
	        ],
	        "allowSharpen": False,
	        "downscale": 1,
	        "channels": []
	    },
	    "mask_RGB": {
	        "selected": False,
	        "suffix": "_mask",
	        "fill": [
	            128,
	            128,
	            128
	        ],
	        "allowSharpen": True,
	        "downscale": 1,
	        "channels": [
	            {
	                "channel": "r",
	                "source": "R",
	                "fill": [
	                    255,
	                    255,
	                    255
	                ]
	            },
	            {
	                "channel": "g",
	                "source": "G",
	                "fill": [
	                    255,
	                    255,
	                    255
	                ]
	            },
	            {
	                "channel": "b",
	                "source": "B",
	                "fill": [
	                    255,
	                    255,
	                    255
	                ]
	            }
	        ]
	    }
	}

	global options
	options = {
        "outputtype": "tga",
        "nonpow2": True,
        "sharpencontrast": False,
        "copytoexportpath": True,
        "copytolocalpath": True
    }

	global gui
	gui = {
        "compactslotsize": True,
        "lastprojectpath": None
    }

	# Save.
	SaveSettings()
