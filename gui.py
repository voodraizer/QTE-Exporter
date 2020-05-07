import nanogui

from nanogui import Color, Screen, Window, GroupLayout, BoxLayout, \
	ToolButton, Label, Button, Widget, \
	Popup, PopupButton, CheckBox, MessageDialog, VScrollPanel, \
	ImagePanel, ImageView, ComboBox, ProgressBar, Slider, \
	TextBox, ColorWheel, Graph, GridLayout, \
	Alignment, Orientation, TabWidget, IntBox, GLShader

from nanogui import gl, glfw, entypo

import photoshop_actions as ps_act

# Colors.
backgr_color = Color(0.5, 0.5, 0.5, 0.5)

class Slot(Widget):

	is_selected = False

	# def __init__(self, parent, image):
	# 	b = Button(parent, "")#, "Styled", entypo.ICON_ROCKET)
	# 	b.setBackgroundColor(Color(0, 0, 1.0, 0.1))
	# 	b.setFixedSize((400, 50))
	#
	# 	# imgPanel = ImagePanel(self)
	# 	# imgPanel.setFixedSize((300, 50))
	# 	# imgPanel.setImages([image])
	#
	# 	Label(b, "Slot", "sans-bold")
	#
	# 	pass

	def __init__(self, parent, image):
		super(Slot, self).__init__(parent)

		b = Button(parent, "")  # , "Styled", entypo.ICON_ROCKET)
		b.setBackgroundColor(Color(0, 0, 1.0, 0.1))
		b.setFixedSize((400, 50))
		# self.addChild(b)


		# imgPanel = ImagePanel(self)
		# imgPanel.setFixedSize((300, 50))
		# imgPanel.setImages([image])

		# l = Label(self, "Slot ====== ", "sans-bold")
		# self.addChild(l)

		pass


class QTE_Gui:
	# Main screen.
	screen = None

	# Main window.
	main_wnd = None
	# Settings window.
	settings_wnd = None

	# Window size.
	main_width = 280
	main_height = 420

	# Images.
	icons = None

	def __init__(self, screen):
		self.screen = screen


	def MainWindow(self, show=True):
		'''
		Main window.
		'''
		self.icons = nanogui.loadImageDirectory(self.screen.nvgContext(), "icons")

		self.main_wnd = Widget(self.screen)
		layout = GroupLayout()
		layout.setMargin(3)
		self.main_wnd.setLayout(layout)
		self.main_wnd.setFixedSize((self.main_width, self.main_height))

		b = Button(self.main_wnd, "Export")
		b.setFixedHeight(25)
		b.setCallback(ps_act.ExportFiles)

		# Slots.
		slots = Widget(self.main_wnd)
		slots.setPosition((20, 60))
		slots.setFixedHeight(345)

		self.DrawSlots(slots)


		# Tools.
		self.Tools(self.main_wnd)

		# Final draw.
		self.screen.setBackground(backgr_color)
		self.screen.drawAll()
		self.screen.drawContents()
		self.screen.performLayout()

	def SettingsWindow(self, show=True):

		self.screen.setBackground(backgr_color)
		self.screen.drawAll()
		self.screen.drawContents()
		self.screen.performLayout()

	def Tools(self, parent):
		'''
		Draw tools widget.
		'''
		tools = Widget(parent)
		tools.setPosition((20, 420))
		layout = BoxLayout(Orientation.Horizontal, Alignment.Middle, 0, 2)
		tools.setLayout(layout)

		tools2 = Widget(tools)
		tools2.setFixedWidth(150)

		b_size = (28, 28)
		b = Button(tools, "", entypo.ICON_ADD_TO_LIST)
		b.setFixedSize(b_size)

		def add(): print("Add")
		b.setCallback(add)

		# Settings.
		b = Button(tools, "", entypo.ICON_ADJUST)
		b.setFixedSize(b_size)

		def settings():
			print("Add")
			self.main_wnd.setVisible(False)

		b.setCallback(settings)

		#
		b = Button(tools, "", entypo.ICON_ALIGN_BOTTOM)
		b.setFixedSize(b_size)

		# Save.
		b = Button(tools, "", entypo.ICON_INSTALL)
		b.setFixedSize(b_size)

	def GetImage(self, name):
		for img in self.icons:
			if (img[1] == name): return img

		return None

	def DrawSlots(self, parent):
		images = Widget(parent)
		images.setLayout(GroupLayout())

		vscroll = VScrollPanel(images)
		vscroll.setFixedHeight(300)
		vscroll.setFixedWidth(240)
		vscroll.setLayout(GroupLayout())

		self.DrawAllSlots(vscroll)

	def DrawAllSlots(self, parent):
		images = Widget(parent)
		images.setLayout(BoxLayout(Orientation.Vertical, Alignment.Middle, 0, 1))

		for i in range(10):
			slot = Slot(images, self.GetImage("icons/slot_bg"))
		slot = Slot(images, self.GetImage("icons/slot_bg"))
		slot = Slot(images, self.GetImage("icons/slot_bg"))

if __name__ == "__main__":
	import sys

	if (len(sys.argv) > 1 and sys.argv[1] == "GUI"):
		import gc
		import qte_exporter
		nanogui.init()

		qte_app = qte_exporter.QTE_App()
		qte_app.Show()

		nanogui.mainloop()

		del qte_app
		gc.collect()
		nanogui.shutdown()

		pass
