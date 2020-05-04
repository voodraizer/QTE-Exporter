import photoshop as ps
from photoshop import Session


def GetPhotoshop():
	ps_app = ps.Application()
	return ps_app

def GetActiveDocument(ps_app = None):
	docRef = None

	if (ps_app and len(ps_app.documents) > 0):
		docRef = ps_app.activeDocument

	if (docRef): print(docRef.name)

	return docRef

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