import gc
import sys
import os
import nanogui

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import photoshop_actions as ps_act
import gui
import settings


class QTE_App(nanogui.Screen):
	# Photoshop app.
	ps_app = None

	# Active document.
	docRef = None

	# Gui.
	app_gui = None

	def __init__(self):

		self.app_gui = gui.QTE_Gui(self)

		super(QTE_App, self).__init__((self.app_gui.main_width, self.app_gui.main_height), "QTE Exporter")

		# self.setScrPos(800, 40)
		self.setScrPosCenter()

		settings.LoadSettings()

		self.ps_app = ps_act.GetPhotoshop()
		self.docRef = ps_act.GetActiveDocument(self.ps_app)

	def draw(self, ctx):
		super(QTE_App, self).draw(ctx)

	def Show(self):
		self.app_gui.MainWindow()

		self.drawAll()
		self.setVisible(True)

	def keyboardEvent(self, key, scancode, action, modifiers):
		from nanogui import glfw

		if super(QTE_App, self).keyboardEvent(key, scancode, action, modifiers):
			return True
		if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
			self.setVisible(False)
			return True

		return False


if __name__ == "__main__":
	import sys

	if (sys.argv[1] == "GUI"):
		nanogui.init()

		qte_app = QTE_App()
		qte_app.Show()

		nanogui.mainloop()

		del qte_app
		gc.collect()
		nanogui.shutdown()
		
		pass
	if (sys.argv[1] == "NOGUI"):
		import photoshop_actions

		photoshop_actions.ExportFiles()
		pass
	if (sys.argv[1] == "TEST"):
		import photoshop_actions

		photoshop_actions.ExportFiles()
		pass

	nanogui.init()

	qte_app = QTE_App()
	qte_app.Show()

	nanogui.mainloop()

	del qte_app
	gc.collect()
	nanogui.shutdown()
