import nanogui

from nanogui import Color, Screen, Window, GroupLayout, BoxLayout, \
	ToolButton, Label, Button, Widget, \
	Popup, PopupButton, CheckBox, MessageDialog, VScrollPanel, \
	ImagePanel, ImageView, ComboBox, ProgressBar, Slider, \
	TextBox, ColorWheel, Graph, GridLayout, \
	Alignment, Orientation, TabWidget, IntBox, GLShader

from nanogui import gl, glfw, entypo

import photoshop_actions as ps_act


class QTE_Gui:
	# Main screen.
	screen = None

	# Window size.
	main_width = 280
	main_height = 450

	# Colors.
	backgr_color = Color(0.5, 0.5, 0.5, 0.5)

	def __init__(self, screen):
		self.screen = screen

	def MainWindow(self, show=True):
		# label = Label(self.screen, "Actions", "sans-bold")
		# label.setPosition((20, 20))

		b = Button(self.screen, "Export")
		b.setPosition((10, 5))
		b.setFixedHeight(25)
		b.setFixedWidth(self.main_width - 20)
		b.setTooltip("Export")
		b.setCallback(ps_act.ExportFiles)

		icons = nanogui.loadImageDirectory(self.screen.nvgContext(), "c:/Program Files/Adobe/Adobe Photoshop 2020/Presets/Scripts/QTE_Exporter/icons/")

		# Slots.
		images = Widget(self.screen)
		images.setPosition((20, 80))
		images.setFixedWidth(self.main_width - 10)
		images.setLayout(BoxLayout(Orientation.Horizontal, Alignment.Fill, 0, 1))

		vscroll = VScrollPanel(images)
		vscroll.setFixedWidth(images.width())
		vscroll.setFixedHeight(250)
		imgPanel = ImagePanel(vscroll)
		imgPanel.setFixedWidth(images.width())
		imgPanel.setImages(icons)

		# Tools.
		tools = Widget(self.screen)
		tools.setPosition((20, 420))
		tools.setFixedWidth(self.main_width - 10)
		tools.setLayout(BoxLayout(Orientation.Horizontal, Alignment.Fill, 0, 2))

		b = ToolButton(tools, entypo.ICON_ADD_TO_LIST)
		def cb2(): print("Add")
		b.setCallback(cb2)
		ToolButton(tools, entypo.ICON_ADJUST)
		ToolButton(tools, entypo.ICON_ALIGN_BOTTOM)
		ToolButton(tools, entypo.ICON_INSTALL)


		self.screen.setBackground(self.backgr_color)
		self.screen.drawAll()
		self.screen.drawContents()
		self.screen.performLayout()

	def SettingsWindow(self, show=True):

		self.screen.setBackground(self.backgr_color)
		self.screen.drawAll()
		self.screen.drawContents()
		self.screen.performLayout()


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
