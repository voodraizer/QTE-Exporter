import photoshop as ps
from photoshop import Session


# ---------------------------------------------------------------------------------------------------------------------
# JavaScript calls.
# ---------------------------------------------------------------------------------------------------------------------
def JS_RemoveAlphaChannel():
	jsx = r"""
	var doc = app.activeDocument;
	var channels = doc.channels;
	var channelCount = channels.length - 1;
	while ( channels[channelCount].kind != ChannelType.COMPONENT ) 
	{
		channels[channelCount].remove();
		channelCount--;
	}
	"""
	app = GetPhotoshop()
	app.doJavaScript(jsx)

def JS_ShowLayerSet(doc, layer):
	if (not layer): return

	indx = -1
	for i in range(len(doc.layerSets)):
		if (doc.layerSets[i].name == layer.name):
			indx = i

	if (indx != -1 or indx < 1): return

	indx -= 1 # convert to photoshop index

	jsx = f"""
	var doc = app.activeDocument;
	var layerFrom = doc.layerSets[{indx}];
	layerFrom.allLocked = false;
	layerFrom.visible = true;
	"""
	app = GetPhotoshop()
	app.doJavaScript(jsx)


def JS_HideLayerSets(indx):
	jsx = f"""
	var doc = app.activeDocument;
	doc.layerSets[{indx}].visible = false;
	"""
	app = GetPhotoshop()
	app.doJavaScript(jsx)


def JS_CollapseLayerSet():
	jsx = r"""
	var doc = app.activeDocument;
	executeAction(stringIDToTypeID("newPlacedLayer"), new ActionDescriptor(), DialogModes.NO);
	doc.activeLayer.rasterize(RasterizeType.ENTIRELAYER);
	"""
	app = GetPhotoshop()
	app.doJavaScript(jsx)


def JS_HasBackgroundLayer():
	jsx = r"""
	var doc = app.activeDocument;
	if (doc.artLayers.length == 0) return "false";
	return doc.artLayers[doc.artLayers.length - 1].isBackgroundLayer ? "true": "false";
	"""
	app = GetPhotoshop()
	has_back = app.doJavaScript(jsx)
	print("JS has back: " + str(has_back))
	return has_back

def JS_RemoveActiveLayer():
	jsx = r"""
	var doc = app.activeDocument;
	doc.activeLayer.remove()
	"""
	app = GetPhotoshop()
	app.doJavaScript(jsx)

def JS_SaveTgaTexture(path):
	jsx = r"""
	var doc = app.activeDocument;
	var saveOptions = new TargaSaveOptions();
	var hasAlpha = (doc.channels.length == 4) ? true : false;
	if (hasAlpha == true)
	{
		saveOptions.resolution = TargaBitsPerPixels.THIRTYTWO;
		saveOptions.alphaChannels = true;
	}
	else
	{
		saveOptions.resolution = TargaBitsPerPixels.TWENTYFOUR;
		saveOptions.alphaChannels = false;
	}
	saveOptions.rleCompression = false;
	"""
	jsx += f"""
	doc.saveAs(new File("{path}"), saveOptions, true, Extension.LOWERCASE);
	"""
	app = GetPhotoshop()
	app.doJavaScript(jsx)

def JS_CloseDocument():
	jsx = r"""
	var doc = app.activeDocument;
	doc.close(SaveOptions.DONOTSAVECHANGES);
	"""
	app = GetPhotoshop()
	app.doJavaScript(jsx)

# ---------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------
def GetPhotoshop():
	ps_app = ps.Application()
	return ps_app

# ---------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------
def GetActiveDocument(ps_app = None):
	docRef = None

	if (ps_app and len(ps_app.documents) > 0):
		docRef = ps_app.activeDocument

	# if (docRef): print(docRef.name)

	return docRef

# ---------------------------------------------------------------------------------------------------------------------
# Return an item called 'name' from the specified container.
# This works for the "magic" on PS containers like Documents.getByName(),
# for instance. However this returns null if an index is not found instead
# of throwing an exception
# The 'all' arg is optional and defaults to 'false'
# ---------------------------------------------------------------------------------------------------------------------
def getByName(container, name, all):
	# check for a bad index
	# if (!name) throw "'undefined' is an invalid name/index"

	# matchFtn = None
	#
	# if (name instanceof RegExp):
	# 	matchFtn = function(s1, re) { return s1.match(re) != null }
	# else:
	# 	matchFtn = function(s1, s2) { return s1 == s2  }
	#
	# var obj = []
	#
	# for (var i = 0; i < container.length; i++):
	# 	if (matchFtn(container[i].name, name)):
	# 		if (!all):
	# 			return container[i]     # there can be only one
	#
	# 		obj.push(container[i])    # add it to the list
	#
	# return all ? obj : undefined

	for l in container:
		if (l.name == name): return l

	return None

def getAllByName(container, name):
	return getByName(container, name, True)

# ---------------------------------------------------------------------------------------------------------------------
# Create artLayer and fill.
# Param color is array like[255, 0, 0] or null(layer not fill).
# ---------------------------------------------------------------------------------------------------------------------
def CreateLayer(doc, color=None):
	doc.artLayers.add()
	doc.selection.selectAll()

	if (color != None):
		# fill.
		fillColor = ps.SolidColor()
		fillColor.rgb.red = color[0]
		fillColor.rgb.green = color[1]
		fillColor.rgb.blue = color[2]
		doc.selection.fill(fillColor)

	doc.selection.deselect()

# ---------------------------------------------------------------------------------------------------------------------
# Copy layer to background.
# Сreate it if necessary.
# ---------------------------------------------------------------------------------------------------------------------
def CopyLayerToBackground(doc, layerFrom):
	'''
	Copy layer to background. Сreate it if necessary.
	:param doc: current document
	:param layerFrom:
	:return:
	'''
	# layerFrom.allLocked = False
	# layerFrom.visible = True
	JS_ShowLayerSet(doc, layerFrom)
	# print("Has back: " + str(HasBackgroundLayer(doc)))
	if (HasBackgroundLayer(doc)):
		# remove background.
		layerTo = doc.backgroundLayer
		layerTo.isBackgroundLayer = False
		doc.activeLayer = layerTo
		# doc.activeLayer.remove()
		JS_RemoveActiveLayer()

	doc.activeLayer = layerFrom
	doc.selection.selectAll()
	doc.selection.copy()
	doc.paste()
	doc.selection.deselect()

	doc.activeLayer.isBackgroundLayer = True

# ---------------------------------------------------------------------------------------------------------------------
#	Remove alpha channel from active document.
# ---------------------------------------------------------------------------------------------------------------------
def RemoveAlphaChannels(doc):
	channels = doc.channels
	# print(channels[0].kind)
	# channelCount = len(channels)
	# while (channels[channelCount].kind != ChannelType.COMPONENT):
	# 	channels[channelCount].remove()
	# 	channelCount --

	# for (c in channels):
	# 	print(c)
	# while (channels[channelCount].kind != ChannelType.COMPONENT):
	# 	channels[channelCount].remove()
	# 	channelCount --

# ---------------------------------------------------------------------------------------------------------------------
#  Check if background layer exists.
# ---------------------------------------------------------------------------------------------------------------------
def HasBackgroundLayer(doc):
	# return JS_HasBackgroundLayer()

	# doc.hasOwnProperty("backgroundLayer")
	if (len(doc.artLayers) == 0):
		return False

	if (doc.artLayers[len(doc.artLayers)].isBackgroundLayer):
		return True

	return False

# ---------------------------------------------------------------------------------------------------------------------
#  Get background layer.
#  Сreate it if necessary.
# ---------------------------------------------------------------------------------------------------------------------
def GetOrCreateBackgroundLayer(doc):
	backgroundLayer = None

	if (HasBackgroundLayer(doc)):
		backgroundLayer = doc.backgroundLayer
	else:
		CreateLayer(doc, [0, 0, 0])
		doc.activeLayer.isBackgroundLayer = True
		# backgroundLayer = doc.activeLayer

	return backgroundLayer

# ---------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------
def GetLayerByNameOrCollapseSet(doc, name):
	layer = getByName(doc.layerSets, name, False)

	if (layer != None):
		# get LayerSet.
		print(" === Get " + name + " as layer set")
		layer.allLocked = False
		layer.visible = True

		# Flatten layer set.
		doc.activeLayer = layer
		# executeAction(stringIDToTypeID("newPlacedLayer"), new ActionDescriptor(), DialogModes.NO)
		# doc.activeLayer.rasterize(RasterizeType.ENTIRELAYER)
		JS_CollapseLayerSet()

		# doc.activeLayer.move(LocationOptions.AT_BEGINNING)
		# doc.activeLayer.move(doc.layers.index(0), ElementPlacement.PLACEAFTER)
		# originalLayer.zOrder(ZOrderMethod.SENDTOBACK)

		layer = doc.activeLayer
		layer.allLocked = False
		layer.visible = True
	else:
		layer = getByName(doc.artLayers, name, False)

		if (layer != None):
			# get ArtLayer.
			print(" === Get " + name + " as art layer")
			doc.activeLayer = layer
			layer.allLocked = False
			layer.visible = True

	return layer

# ---------------------------------------------------------------------------------------------------------------------
# Create channel from layerGroup and delete layerGroup after that.
# channel - must be 0, 1, 2 or 3.
# Document must contain backgroundLayer.
# ---------------------------------------------------------------------------------------------------------------------
def SetChannelFromLayerGroup(doc, layer, channel):
	if (channel != 0 and channel != 1 and channel != 2 and channel != 3):
		return

	# find background layer.
	background = doc.backgroundLayer

	layer.allLocked = False
	layer.visible = True

	doc.activeLayer = layer
	doc.selection.selectAll()
	doc.selection.copy()
	layer.visible = False

	doc.activeLayer = background

	if (channel == 3 and len(doc.channels) == 3):
		# add alpha channel if needed.
		doc.channels.add()

	doc.activeChannels = [doc.channels[channel]]

	doc.paste()
	doc.selection.deselect()

	# restore channel selection.
	doc.channels[0].visible = True
	doc.channels[1].visible = True
	doc.channels[2].visible = True
	if (len(doc.channels) > 3): doc.channels[3].visible = False

	doc.activeChannels = [doc.channels[0], doc.channels[1], doc.channels[2]]

# ---------------------------------------------------------------------------------------------------------------------
# Hide all group and art layers in document root.
# ---------------------------------------------------------------------------------------------------------------------
def HideAllInRoot(doc):
	for i in range(len(doc.layerSets)):
		doc.layerSets[i].allLocked = False
		JS_HideLayerSets(i) # doc.layerSets[i].visible = False

	for i in range(len(doc.artLayers)):
		doc.artLayers[i].allLocked = False
		doc.artLayers[i].visible = False

# ---------------------------------------------------------------------------------------------------------------------
# Save options.
# ---------------------------------------------------------------------------------------------------------------------
def CreateTgaSaveOptions(hasAlpha):
	saveOptions = ps.TargaSaveOptions()
	if (hasAlpha):
	# 	saveOptions.resolution = TargaBitsPerPixels.THIRTYTWO
		saveOptions.alphaChannels = True
	else:
	# 	saveOptions.resolution = TargaBitsPerPixels.TWENTYFOUR
		saveOptions.alphaChannels = False

	saveOptions.rleCompression = False

	return saveOptions

def CreatePngSaveOptions(hasAlpha):
	# var pngOpts = ExportOptionsSaveForWeb()
	# pngOpts.format = SaveDocumentType.PNG
	# pngOpts.PNG8 = False
	# pngOpts.transparency = True
	# pngOpts.interlaced = False
	# pngOpts.quality = 100
	# activeDocument.exportDocument(new File(saveFile),ExportType.SAVEFORWEB,pngOpts)

	saveOptions = ps.PNGSaveOptions()
	saveOptions.interlaced = False
	return saveOptions

def CreateTiffSaveOptions(hasAlpha):
	saveOptions = ps.TiffSaveOptions()
	if (hasAlpha):
		saveOptions.alphaChannels = True
	else:
		saveOptions.alphaChannels = False

	# if (TIFFEncoding.JPEG == exportInfo.tiffCompression)
	# saveOptions.jpegQuality = exportInfo.tiffJpegQuality
	# saveOptions.embedColorProfile = exportInfo.icc
	# saveOptions.imageCompression = exportInfo.tiffCompression
	saveOptions.layers = False
	# saveOptions.transparency =

	return saveOptions

def CreateBmpSaveOptions(hasAlpha):
	saveOptions = ps.BMPSaveOptions()
	if (hasAlpha):
		saveOptions.alphaChannels = True
		# saveOptions.depth = BMPDepthType.THIRTYTWO
	else:
		saveOptions.alphaChannels = False
		# saveOptions.depth = BMPDepthType.TWENTYFOUR

	# saveOptions.flipRowOrder = False
	# saveOptions.osType = OperatingSystem.WINDOWS # OS2
	# saveOptions.rleCompression = False

	return saveOptions

# ---------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------
def SaveTexture(doc, saveFile, outputtype):
	# save new document
	saveOptions = None
	print("Ch num: " + str(doc.channels))
	hasAlpha = True if (len(doc.channels) == 4) else False

	if (outputtype == "tga"):
		saveOptions = CreateTgaSaveOptions(hasAlpha)
	if (outputtype == "png"):
		saveOptions = CreatePngSaveOptions(hasAlpha)
		# apply alpha. TODO
		# select from alpha channel, inverted, delete, delete alpha channel.
	if (outputtype == "tiff"):
		saveOptions = CreateTiffSaveOptions(hasAlpha)
	if (outputtype == "bmp"):
		saveOptions = CreateBmpSaveOptions(hasAlpha)

	if (saveOptions == None):
		# print("Not created save options")
		# doc.close(SaveOptions.DONOTSAVECHANGES)
		return

	# print(" >Save as: " + saveFile + "." + outputtype)
	# doc.saveAs(new File(saveFile + "." + outputtype), saveOptions, true, Extension.LOWERCASE)

	# copy duplicate to symmetry path if one exist.
	# var pathToExport = data.symmetrypath
	# if (data.copytosymmetrypath == true && Folder(pathToExport).exists == true)
		# symmetrypath = GetSymmetryPath(pathToExport)
		# if (symmetrypath != null)
		# 	symmetrypath = symmetrypath + "/" + exportName + suffix + "." + data.outputtype
		# 	newDoc.saveAs(new File(symmetrypath), saveOptions, false, Extension.LOWERCASE)
	# else if (data.copytosymmetrypath == true)
		# print("Path to symmetry export not exist." + " Path = " + pathToExport)

	pass

# ---------------------------------------------------------------------------------------------------------------------
# Save file by texture type.
# ---------------------------------------------------------------------------------------------------------------------
def ExportTexture(doc, slot_name, slot, exportPath, exportName):
	import settings

	# diffuse -- {'selected': True, 'suffix': '_df', 'fill': [128, 128, 128], 'allowSharpen': True, 'downscale': 1,
	# 'channels': [{'channel': 'a', 'source': 'alpha', 'fill': [255, 255, 255]}]}

	# print("Export texture: " + str(exportPath) + " -- " + str(exportName) + " -- " + outputtype)

	# Hide all.
	HideAllInRoot(doc)

	# RemoveAlphaChannels(doc)
	JS_RemoveAlphaChannel()

	# construct document.
	layer = GetLayerByNameOrCollapseSet(doc, slot_name)
	if (layer != None):
		# print(" <<=============>> Layer: " + layer.name)
		doc.activeLayer = layer

	CopyLayerToBackground(doc, layer)

	layer.visible = False

	for ch in range(len(slot["channels"])):
		print("Channel: " + str(ch))
		# channel_layer = GetLayerByNameOrCollapseSet(doc, slot.channels[ch].source)
		# if (channel_layer != None):
		# 	channel_layer.visible = True
		# 	doc.activeLayer = channel_layer
		#
		# 	backgroundLayer = GetOrCreateBackgroundLayer(doc)
		# 	if (backgroundLayer != None): doc.activeLayer = backgroundLayer
		#
		# 	# Create from channels.
		# 	# if (slot.channels[ch].type == "r"): SetChannelFromLayerGroup(doc, channel_layer, 0)
		# 	# if (slot.channels[ch].type == "g"): SetChannelFromLayerGroup(doc, channel_layer, 1)
		# 	# if (slot.channels[ch].type == "b"): SetChannelFromLayerGroup(doc, channel_layer, 2)
		# 	# if (slot.channels[ch].type == "a"): SetChannelFromLayerGroup(doc, channel_layer, 3)
		#
		# 	channel_layer.visible = False

	# downscale if needed.
	# TODO: если нужно даунскейлить, то создаём новый файл.
	# DownscaleSize(doc, slot)

	# sharpen.
	# TODO: проходится по настройкам слота и шарпить бэкграунд и(или) каналы.
	# if (data.sharpencontrast == true & & slotTemplate.allowSharpen == true)
	#   SharpenInkjetOutput()
	#   doc.flatten()
	#   # sharpen and contrast.
	#   SharpenLocalContrast()
	#   doc.flatten()

	import os
	# print(settings.options["copytolocalpath"])
	if (settings.options["copytolocalpath"] == True):
		outputtype = settings.options["outputtype"]
		# outputtype = "bmp"
		# full path with name.
		print("============================ COPY ============================")
		saveFile = os.path.join(os.path.normpath(exportPath), exportName + slot["suffix"])
		print("Export file: " + saveFile + "." + outputtype)
		# SaveTexture(doc, saveFile, outputtype)
		JS_SaveTgaTexture(saveFile + ".tga")

	# if (settings.options.copytoexportpath == True):
	# 	saveFile = ""

	# 	# check path from XMP PSD.
	# 	if (xmpSettings.ExportPath != ""):
	# 		# if (Folder(xmpSettings.ExportPath).exists == false)
	# 		# xmpPathFolder = Folder(xmpSettings.ExportPath) //.fsName.toLowerCase())
	# 		# if (!xmpPathFolder.exists):
	# 			# xmpPathFolder.create()
	#
	# 	# full path with name.
	# 	# outputtype = xmpSettings.OutputType
	# 	# saveFile = xmpSettings.ExportPath + "/" + exportName + suffix
	# 	# SaveTexture(doc, saveFile, outputtype)

# ---------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------
def ExportFiles():
	print("===== START EXPORT")

	ps_app = GetPhotoshop()
	docRef = GetActiveDocument(ps_app)

	docName = docRef.name
	docWidth = docRef.width
	docHeight = docRef.height

	# Check for errors.
	# if (CheckForErrors(data.nonpow2)) return

	# Delete alpha	channels from original psd	file.
	# RemoveAlphaChannels(docRef)
	JS_RemoveAlphaChannel()

	# delete file extension and suffix.
	import os
	exportPath = docRef.path
	exportName = os.path.splitext(docRef.name)[0]
	# tempStr = decodeURI(exportName.substring(0, exportName.lastIndexOf(fileNameDelimiter)))
	# if (tempStr != ""): exportName = tempStr

	# print(" ===> " + str(exportPath) + " --- " + str(exportName))

	# create new document.
	exportedDoc = docRef.duplicate(exportName + "_export", False)
	ps_app.activeDocument = exportedDoc

	# Create background layer.
	backgroundLayer = GetOrCreateBackgroundLayer(exportedDoc)

	import settings
	for name, slot in settings.slots.items():
		if (not slot["selected"]): continue
		# if (not getByName(name)): continue
		print("Slot:  " + str(name) + " -- " + str(slot))

		# update progress bar.

		# export.
		ExportTexture(exportedDoc, name, settings.slots[name], exportPath, exportName)
		pass

	# close.
	# exportedDoc.close(SaveOptions.DONOTSAVECHANGES)
	# JS_CloseDocument()

	# make original	document active
	# ps_app.activeDocument = docRef

	# ps_app.doJavaScript(f'alert("Example")')
	# ps.echo(ps_app.active_document.name)

	print("===== END EXPORT")
	pass

# ---------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------
def KillConsoleWindow():
	import ctypes
	import os
	# import win32process

	hwnd = ctypes.windll.kernel32.GetConsoleWindow()
	if hwnd != 0:
		ctypes.windll.user32.ShowWindow(hwnd, 0)
		ctypes.windll.kernel32.CloseHandle(hwnd)
		# _, pid = win32process.GetWindowThreadProcessId(hwnd)
		# os.system('taskkill /PID ' + str(pid) + ' /f')

	pass

# ---------------------------------------------------------------------------------------------------------------------
# Test.
# ---------------------------------------------------------------------------------------------------------------------
def Actions_1():
	with Session() as ps:
		if len(ps.app.documents) < 1:
			docRef = ps.app.documents.add()
		else:
			docRef = ps.app.activeDocument

		if len(docRef.layers) < 2:
			docRef.artLayers.add()

		ps.echo(docRef.activeLayer.name)
		ps.echo(docRef.layers.item(len(docRef.layers)))
		new_layer = docRef.artLayers.add()
		ps.echo(new_layer.name)
		new_layer.name = "test"


def Actions_2():
	app = ps.Application()
	doc = app.documents.add()
	new_doc = doc.artLayers.add()
	text_color = ps.SolidColor()
	text_color.rgb.green = 255
	new_text_layer = new_doc
	new_text_layer.kind = ps.LayerKind.TextLayer
	new_text_layer.textItem.contents = 'Hello, World!'
	new_text_layer.textItem.position = [160, 167]
	new_text_layer.textItem.size = 40
	new_text_layer.textItem.color = text_color

def Test_1():
	ps_app = GetPhotoshop()
	doc = GetActiveDocument(ps_app)

	# print(str(HasBackgroundLayer_2(doc)))

	backgroundLayer = GetOrCreateBackgroundLayer(doc)
	layerFrom = GetLayerByNameOrCollapseSet(doc, "diffuse")
	# print(type(layerFrom))
	CopyLayerToBackground(doc, layerFrom)

	pass

def Test_2():
	app = ps.Application()
	# print(app.doJavaScript("app.activeDocument.name"))
	JS_SaveTgaTexture("D:/ttttt.tga")
	pass


def HasBackgroundLayer_2(doc):
	# has_back = JS_HasBackgroundLayer()
	# print("Has back: " + str(has_back))
	# return has_back

	# doc.hasOwnProperty("backgroundLayer")
	if (len(doc.artLayers) == 0):
		return False
	print("-----")
	for l in range(len(doc.artLayers) + 1):
		print("N: " + str(l) + " Name: " + doc.artLayers[l].name + " Is_bak: " + str(doc.artLayers[l].isBackgroundLayer))
	print("-----")
	# print("Has back: " + str(doc.artLayers[len(doc.artLayers)].isBackgroundLayer))
	# print("Has back: " + str(doc.artLayers[0].isBackgroundLayer))
	if (doc.artLayers[len(doc.artLayers)].isBackgroundLayer):
		return True

	return False

# ---------------------------------------------------------------------------------------------------------------------
# Main.
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
	import sys

	# if (len(sys.argv) > 1 and sys.argv[1] == "GUI"):
	# 	print("RUN GUI")
	# 	pass
	# if (len(sys.argv) > 1 and sys.argv[1] == "NOGUI"):
	# 	print("RUN NOGUI")
	# 	pass
	# if (len(sys.argv) > 1 and sys.argv[1] == "TEST"):
	# 	print("RUN TEST")
	# 	# ps_app = GetPhotoshop()
	# 	# ps_app.doJavaScript(f'alert("MAIN");')
	# 	# ExportFiles()
	# 	pass

	import settings
	settings.LoadSettings()
	# Test_2()
	ExportFiles()