import photoshop as ps
from photoshop import Session


# ---------------------------------------------------------------------------------------------------------------------
# JavaScript calls.
# ---------------------------------------------------------------------------------------------------------------------
def JS_CollapseLayerSet():
	'''
	Замена
	executeAction(stringIDToTypeID("newPlacedLayer"), new ActionDescriptor(), DialogModes.NO)
	doc.activeLayer.rasterize(RasterizeType.ENTIRELAYER)
	'''

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
	'''
	Замена SaveTexture(doc, saveFile, xmp_output_type)
	'''

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
	'''
	Замена exportedDoc.close(SaveOptions.DONOTSAVECHANGES)
	'''

	jsx = r"""
	var doc = app.activeDocument;
	doc.close(SaveOptions.DONOTSAVECHANGES);
	"""
	app = GetPhotoshop()
	app.doJavaScript(jsx)

def JS_GetExporterXMPPreset():
	# XMP meta
	jsx = r"""
	var qteXMPNamespace = "http://qte.exporter/1.0/";
	var qteXMPPrefix = "qtesets:";

	if (ExternalObject.AdobeXMPScript == undefined)  ExternalObject.AdobeXMPScript = new ExternalObject("lib:AdobeXMPScript");
	XMPMeta.registerNamespace(qteXMPNamespace, qteXMPPrefix);
	
	//  Read xmp configs.
	var doc = app.activeDocument;
	
	var xmp = new XMPMeta( doc.xmpMetadata.rawData );
	
	//$.writeln("Path: " + xmp.getProperty(qteXMPNamespace, "ExportPath", XMPConst.STRING));
	//$.writeln("Type: " + xmp.getProperty(qteXMPNamespace, "OutputType", XMPConst.STRING));
	//$.writeln("DownScale: " + xmp.getProperty(qteXMPNamespace, "DownScale", XMPConst.NUMBER));
	
	var ExportPath = xmp.getProperty(qteXMPNamespace, "ExportPath", XMPConst.STRING);
	var OutputType = xmp.getProperty(qteXMPNamespace, "OutputType", XMPConst.STRING)
	var DownScale = xmp.getProperty(qteXMPNamespace, "DownScale", XMPConst.NUMBER);
	
	var output = "'" + ExportPath + "|" + OutputType + "|" + DownScale + "'";
	output; 
	"""
	app = GetPhotoshop()
	return app.doJavaScript(jsx)

def JS_SetExporterXMPPreset(ExportPath = "", OutputType = "", DownScale = 1):
	jsx = f"""
	var qteXMPNamespace = "http://qte.exporter/1.0/";
	var qteXMPPrefix = "qtesets:";

	if (ExternalObject.AdobeXMPScript == undefined)  ExternalObject.AdobeXMPScript = new ExternalObject("lib:AdobeXMPScript");
	XMPMeta.registerNamespace(qteXMPNamespace, qteXMPPrefix);

	var doc = app.activeDocument;
	var xmp = new XMPMeta( doc.xmpMetadata.rawData );
	
	//xmp.deleteProperty(qteXMPNamespace, "ExportPath");
	xmp.setProperty(qteXMPNamespace, "ExportPath", "{ExportPath}" , 0, XMPConst.STRING);
	
	//xmp.deleteProperty(qteXMPNamespace, "OutputType");
	xmp.setProperty(qteXMPNamespace, "OutputType", "{OutputType}" , 0, XMPConst.STRING);
	
	//xmp.deleteProperty(qteXMPNamespace, "DownScale");
	xmp.setProperty(qteXMPNamespace, "DownScale", {DownScale} , 0, XMPConst.NUMBER);
	
	doc.xmpMetadata.rawData = xmp.serialize();
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

	return doc.artLayers[0] # doc.activeLayer

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
	layerFrom.allLocked = False
	layerFrom.visible = True

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

	for c in channels:
		# if ("alpha" in c.name.lower()):
		if (c.kind == 2): # == ChannelType.COMPONENT
			alpha_channel = doc.channels.getByName(c.name)
			alpha_channel.remove()

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
		layer.allLocked = False
		layer.visible = True

		# Flatten layer set.
		doc.activeLayer = layer
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
			doc.activeLayer = layer
			layer.allLocked = False
			layer.visible = True

	return layer

# ---------------------------------------------------------------------------------------------------------------------
# Create channel from layerGroup and delete layerGroup after that.
# channel - must be 1 (r), 2 (g), 3 (b) or 4 (alpha).
# Document must contain backgroundLayer.
# ---------------------------------------------------------------------------------------------------------------------
def SetChannelFromLayerGroup(doc, layer, channel):
	if (channel != 1 and channel != 2 and channel != 3 and channel != 4):
		return

	if (not HasBackgroundLayer(doc)): raise Exception('\n\nDocument must contain background layer !')

	layer.allLocked = False
	layer.visible = True

	doc.activeLayer = layer
	doc.selection.selectAll()
	doc.selection.copy()
	layer.visible = False

	doc.activeLayer = doc.backgroundLayer

	if (channel == 4 and len(doc.channels) == 3):
		# add alpha channel if needed.
		doc.channels.add()

	doc.activeChannels = [doc.channels[channel]]

	doc.paste()
	doc.selection.deselect()

	# restore channel selection.
	doc.channels[1].visible = True
	doc.channels[2].visible = True
	doc.channels[3].visible = True
	if (len(doc.channels) > 3): doc.channels[4].visible = False

	doc.activeChannels = [doc.channels[1], doc.channels[2], doc.channels[3]]

# ---------------------------------------------------------------------------------------------------------------------
# Hide all group and art layers in document root.
# ---------------------------------------------------------------------------------------------------------------------
def HideAllInRoot(doc):
	for i in range(len(doc.layerSets)):
		doc.layerSets[i].allLocked = False
		doc.layerSets[i].visible = False

	for i in range(len(doc.artLayers)):
		doc.artLayers[i].allLocked = False
		doc.artLayers[i].visible = False

# ---------------------------------------------------------------------------------------------------------------------
# Save options.
# ---------------------------------------------------------------------------------------------------------------------
def CreateTgaSaveOptions(hasAlpha):
	from photoshop.enumerations import TargaBitsPerPixels

	saveOptions = ps.TargaSaveOptions()
	if (hasAlpha):
		saveOptions.resolution = TargaBitsPerPixels.THIRTYTWO
		saveOptions.alphaChannels = True
	else:
		saveOptions.resolution = TargaBitsPerPixels.TWENTYFOUR
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
	saveOptions = None

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

	# save new document
	doc.saveAs(saveFile + "." + outputtype, saveOptions, asCopy=True)

	pass

# ---------------------------------------------------------------------------------------------------------------------
# Export by texture type.
# ---------------------------------------------------------------------------------------------------------------------
def ExportTexture(doc, slot_name, slot, exportPath, exportName):

	# get XMP from PSD [ExportPath | OutputType | DownScale].
	xmp_output = JS_GetExporterXMPPreset()
	xmp_output = xmp_output.replace("'", "").split("|")
	xmp_export_path = xmp_output[0]
	xmp_output_type = xmp_output[1]
	xmp_downscale = xmp_output[2]
	# print(xmp_export_path + " --- " + xmp_output_type + " --- " + xmp_downscale)

	# Hide all.
	HideAllInRoot(doc)

	RemoveAlphaChannels()

	# construct document.
	layer = GetLayerByNameOrCollapseSet(doc, slot_name)
	if (layer is None): raise Exception("Not found layer: " + slot_name)

	doc.activeLayer = layer

	CopyLayerToBackground(doc, layer)

	layer.visible = False

	for n_ch in range(len(slot["channels"])):
		channel = slot["channels"][n_ch]

		channel_layer = GetLayerByNameOrCollapseSet(doc, channel["source"])
		if (channel_layer is None):
			if (channel["channel"] == "a"): continue

			# create default layer if not alpha.
			channel_layer = CreateLayer(doc, channel["fill"])

		channel_layer.visible = True
		doc.activeLayer = channel_layer

		backgroundLayer = GetOrCreateBackgroundLayer(doc)
		if (backgroundLayer is None): raise Exception("Not found background layer !")

		doc.activeLayer = backgroundLayer

		# Create from channels.
		if (channel["channel"] == "r"): SetChannelFromLayerGroup(doc, channel_layer, 1)
		if (channel["channel"] == "g"): SetChannelFromLayerGroup(doc, channel_layer, 2)
		if (channel["channel"] == "b"): SetChannelFromLayerGroup(doc, channel_layer, 3)
		if (channel["channel"] == "a"): SetChannelFromLayerGroup(doc, channel_layer, 4)

		channel_layer.visible = False

	HideAllInRoot(doc) # TODO: раньше без этого работало. Посмотреть !!!

	# downscale if needed.
	# TODO: если нужно даунскейлить, то создаём новый файл.
	# if (slot["downscale"] != 1): DownscaleSize(doc, slot)

	# sharpen.
	# TODO: проходится по настройкам слота и шарпить бэкграунд и(или) каналы.
	# if (slot["allowSharpen"] == True): # and slotTemplate.allowSharpen == True)
	#   SharpenInkjetOutput()
	#   doc.flatten()
	#   # sharpen and contrast.
	#   SharpenLocalContrast()
	#   doc.flatten()

	import os
	import settings
	if (settings.options["copytolocalpath"] == True):
		outputtype = settings.options["outputtype"]
		# full path with name.
		saveFile = os.path.join(os.path.normpath(exportPath), exportName + slot["suffix"])
		print("Export file: " + saveFile + "." + outputtype)
		JS_SaveTgaTexture(saveFile + ".tga")
		# SaveTexture(doc, saveFile, outputtype)

	if (settings.options["copytoexportpath"] == True):
		# check path from XMP PSD.
		if (xmp_export_path != ""):
			if (not os.path.exists(xmp_export_path)): os.makedirs(xmp_export_path)

		# full path with name.
		saveFile = xmp_export_path + "/" + exportName + slot["suffix"]
		JS_SaveTgaTexture(saveFile + ".tga")
		# SaveTexture(doc, saveFile, outputtype)

# ---------------------------------------------------------------------------------------------------------------------
# Export all textures.
# ---------------------------------------------------------------------------------------------------------------------
def ExportFiles():
	import os

	print("===== START EXPORT")

	ps_app = GetPhotoshop()
	docRef = GetActiveDocument(ps_app)

	if (docRef is None): raise Exception("Not found open document.")

	docName = docRef.name
	docWidth = docRef.width
	docHeight = docRef.height
	exportPath = docRef.path
	if (exportPath is None) or (not os.path.exists((exportPath))): raise Exception("Document must be saved.")

	# Check for errors.
	# if (CheckForErrors(data.nonpow2)) return

	# Delete alpha	channels from original psd	file.
	RemoveAlphaChannels()

	# create new document.
	exportName = os.path.splitext(docRef.name)[0]
	exportedDoc = docRef.duplicate(exportName + "_export", False)
	ps_app.activeDocument = exportedDoc

	# Create background layer.
	backgroundLayer = GetOrCreateBackgroundLayer(exportedDoc)

	import settings
	for name, slot in settings.slots.items():
		if (not slot["selected"]): continue

		# update progress bar.

		# export.
		ExportTexture(exportedDoc, name, settings.slots[name], exportPath, exportName)
		pass

	# close.
	JS_CloseDocument()

	# make original	document active
	ps_app.activeDocument = docRef

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
# Tests.
# ---------------------------------------------------------------------------------------------------------------------

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
	ps_app = GetPhotoshop()
	doc = GetActiveDocument(ps_app)

	HideAllInRoot(doc)
	SetChannelFromLayerGroup(doc, doc.artLayers[0], 4)
	SetChannelFromLayerGroup(doc, doc.artLayers[3], 1)

def Test_3():
	JS_SetExporterXMPPreset(ExportPath="D:/__QteExport", OutputType="tga", DownScale=2)
	output = JS_GetExporterXMPPreset()
	output = output.replace("'", "").split("|")
	print(output[0] + " --- " + output[1] + " --- " + output[2])

def Test_4():
	ps_app = GetPhotoshop()
	doc = GetActiveDocument(ps_app)
	RemoveAlphaChannels(doc)


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
	if (len(sys.argv) > 1 and sys.argv[1] == "TEST"):
		import settings

		print("================= RUN TEST =================")
		settings.LoadSettings()
		# ps_app.doJavaScript(f'alert("MAIN");')
		# Test_4()
		ExportFiles()
		pass