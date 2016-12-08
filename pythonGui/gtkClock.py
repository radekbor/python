import gtk
import math
import datetime
import math


class PyApp():
	def __init__(self):
		self.minutesOffset = 0;
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("Zegar")
		self.window.resize(230, 250)
		self.window.set_resizable(False);

		self.window.show()

		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.connect("destroy", gtk.main_quit)
		self.r = 100
		self.darea = gtk.DrawingArea()
		self.my_timer()
		self.darea.show()
		self.darea.set_size_request(300, 300)

		self.darea.connect("expose-event", self.expose)
		self.darea.connect("configure_event", self.configure_event)
		self.darea.queue_draw()
		gtk.timeout_add(1000, self.my_timer)

		self.box = gtk.VBox()
		self.box.pack_start(self.darea, False, False, 0)
		menu_bar = gtk.MenuBar()
		self.box.pack_end(menu_bar, False, False, 2)

		menu = gtk.Menu()

		menu_bar.show()
		root_menu = gtk.MenuItem("Menu")
		root_menu.set_submenu(menu)

		forward = gtk.MenuItem('Przestaw do przodu')
		forward.connect("activate", self.forward_actions, "Do przodu")
		forward.show()
		menu.append(forward)

		accel_group1 = gtk.AccelGroup()
		self.window.add_accel_group(accel_group1)
		forward.add_accelerator("activate", accel_group1, ord('J'), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)

		back = gtk.MenuItem('Przestaw do tylu')
		back.connect("activate", self.back_actions, "Do tylu")
		back.show()
		menu.append(back)

		accel_group2 = gtk.AccelGroup()
		self.window.add_accel_group(accel_group2)
		back.add_accelerator("activate", accel_group2, ord('U'), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)

		help = gtk.MenuItem('Pomoc')
		help.connect("activate", self.on_info_clicked, "Pomoc")
		help.show()
		menu.append(help)

		root_menu.show()
		menu_bar.append(root_menu)

		self.window.add(self.box)
		self.box.show()
		self.window.show_all()


	def on_info_clicked(self, widget, event):
		dialog = gtk.MessageDialog(self.window, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, "Pomoc aplikacji zegar")
		dialog.format_secondary_text("Zegar posiada funckje przewijania w przod oraz w tyl. Aby tego dokonac nalezy klinac w 'Przestaw do tyl' lub 'Przestaw do przodu'.\nAlternatywnie mozna tego dokonc przy pomocy skrotow klawiszowych")
		dialog.run()

	def forward_actions(self, widget, event):
		self.minutesOffset = self.minutesOffset + 1

	def back_actions(self, widget, event):
		self.minutesOffset = self.minutesOffset - 1

	def my_timer(self):
		now = datetime.datetime.now()
		self.hour = now.hour % 12
		self.minutes = now.minute + self.minutesOffset
		self.seconds = now.second
		self.darea.queue_draw()
		return True

	def getSecondsPoints(self):
		angle = math.radians(self.seconds * 6 - 90)
		X = self.r * math.cos(angle)
		Y = self.r * math.sin(angle)
		return [X, Y]

	def getMinutesPoints(self):
		angle = math.radians(self.minutes * 6 - 90)
		X = self.r * 0.75 * math.cos(angle)
		Y = self.r * 0.75 * math.sin(angle)
		return [X, Y]

	def getHoursPoints(self):
		angle = math.radians(self.hour * 30 - 90 + self.minutes / 2)
		X = self.r * 0.5 * math.cos(angle)
		Y = self.r * 0.5 * math.sin(angle)
		return [X, Y]

	def configure_event(self, widget, event):
		x, y, width, height = widget.get_allocation()
		return True

	def expose(self, widget, event):
		cr = widget.window.cairo_create()
		cr.set_line_width(2)
		cr.set_source_rgb(0.7, 0.2, 0.0)

		w = self.window.allocation.width
		h = self.window.allocation.height
		cr.translate(w / 2, h / 2)
		cr.arc(0, 0, 100, 0, 2 * math.pi)
		cr.stroke_preserve()

		cr.set_source_rgb(0.0, 0.0, 0.8)

		cr.move_to(0, 0)
		seconds = self.getSecondsPoints()
		cr.set_line_width(1)
		cr.rel_line_to(seconds[0], seconds[1])
		cr.stroke()

		cr.move_to(0, 0)
		minutes = self.getMinutesPoints()
		cr.set_line_width(4)
		cr.rel_line_to(minutes[0], minutes[1])
		cr.stroke()

		cr.move_to(0, 0)
		hours = self.getHoursPoints()
		cr.set_line_width(7)
		cr.rel_line_to(hours[0], hours[1])
		cr.stroke()


PyApp()
gtk.main()

