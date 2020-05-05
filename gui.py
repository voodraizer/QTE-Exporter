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
	main_width = 200
	main_height = 400

	def __init__(self, screen):
		self.screen = screen

	def MainWindow(self, show=True):
		label = Label(self.screen, "Actions", "sans-bold")
		label.setPosition((20, 20))

		b = Button(self.screen, "Execute !")
		b.setPosition((20, 40))
		b.setCallback(ps_act.ExportFiles)

		self.screen.setBackground(Color(0, 0, 0, 0.5))

		self.screen.drawAll()
		self.screen.drawContents()

		self.screen.performLayout()
