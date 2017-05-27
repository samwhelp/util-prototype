#!/usr/bin/env python3

## http://python-gtk-3-tutorial.readthedocs.io/en/latest/introduction.html
## https://lazka.github.io/pgi-docs/index.html#Gtk-3.0
## https://lazka.github.io/pgi-docs/index.html#Keybinder-3.0
## https://lazka.github.io/pgi-docs/index.html#AppIndicator3-0.1
## https://lazka.github.io/pgi-docs/index.html#WebKit2-4.0

## install debian package
## $ sudo apt-get install gir1.2-gtk-3.0 gir1.2-keybinder-3.0 gir1.2-appindicator3-0.1 gir1.2-webkit2-4.0

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

gi.require_version('Keybinder', '3.0')
from gi.repository import Keybinder

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as AppIndicator

gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2 as WebKit


import signal
import subprocess


class App:
	app = None
	box = None
	webview = None

	app_name = 'hiply'
	app_title = 'Hiply'

	win_width = 600
	win_height = 800

	state_fullscreen = False
	state_activate = True

	uri_default = 'http://hichannel.hinet.net/radio/index.do'

	icon_name_app = 'video'
	icon_name_on_win_activate = 'video'
	icon_name_on_win_deactivate = 'video-display'
	icon_name_btn_app_quit = 'application-exit'

	keybind_accelerator_name_activate = '<Super>a'
	keybind_accelerator_name_fullscreen = 'F11'
	keybind_accelerator_name_play_icrt = 'F5'

	#def __init__ (self):
	#	pass

	def init (self):
		self.init_signal()
		self.init_keybind()
		self.init_menu()
		self.init_win()


	def init_signal (self):
		## https://docs.python.org/3/library/signal.html
		signal.signal(signal.SIGINT, signal.SIG_DFL)

	def init_keybind (self):
		Keybinder.init()
		Keybinder.bind(self.keybind_accelerator_name_activate, self.on_key_activate_win)

	def init_menu (self):

		self.menu = menu = Gtk.Menu()

		item = Gtk.MenuItem.new_with_label('開啟應用視窗 (%s)' % self.keybind_accelerator_name_activate)
		item.connect('activate', self.on_activate_win)
		menu.append(item)

		item = Gtk.MenuItem.new_with_label('全螢幕 (%s)' % self.keybind_accelerator_name_fullscreen)
		item.connect('activate', self.on_fullscreen_win)
		menu.append(item)

		item = Gtk.MenuItem.new_with_label('播放ICRT (%s)' % self.keybind_accelerator_name_play_icrt)
		item.connect('activate', self.on_play_icrt)
		menu.append(item)

		item = Gtk.MenuItem.new_with_label('目前頁面網址')
		item.connect('activate', self.on_get_uri)
		menu.append(item)

		item = Gtk.MenuItem.new_with_label('關於 %s' % self.app_title)
		item.connect('activate', self.on_show_about)
		menu.append(item)

		img = Gtk.Image.new_from_icon_name(self.icon_name_btn_app_quit, 16)
		item = Gtk.ImageMenuItem.new_with_label('離開')
		item.connect('activate', self.on_quit_app)
		item.set_image(img)
		menu.append(item)


		menu.show_all()

		self.indicator = indicator = AppIndicator.Indicator.new(
			self.app_name,
			self.icon_name_on_win_activate,
			AppIndicator.IndicatorCategory.APPLICATION_STATUS
		)

		indicator.set_menu(menu)

		indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)


	def init_win (self):
		self.win = win = Gtk.Window()

		win.set_title(self.app_title)
		win.set_icon_name(self.icon_name_app)

		win.connect('delete-event', self.on_close_win)

		win.connect('key-press-event', self.on_key_press)
		#win.connect('key-release-event', self.on_key_release)

		self.box = box = Gtk.Box(spacing=6)
		win.add(box)

		self.init_webview()
		box.pack_start(self.webview, True, True, 0)

		win.resize(self.win_width, self.win_height)
		win.show_all()

	def init_webview (self):
		self.webview = webview = WebKit.WebView()
		self.go_load_default()

		webview.connect('button-press-event', self.on_button_press)
		#webview.connect('button-release-event', self.on_button_release)

	def on_button_press (self, win, evt):
		## on mouse left button double click
		if evt.type == Gdk.EventType.DOUBLE_BUTTON_PRESS:
			self.go_switch_fullscreen()
			return True

		return False

	def on_button_release (self, win, evt):

		return False

	def on_key_press (self, win, evt):
		accelerator_name = Gtk.accelerator_name(evt.keyval, evt.state)
		## accelerator_label = Gtk.accelerator_get_label(evt.keyval, evt.state)

		if accelerator_name == self.keybind_accelerator_name_fullscreen:
			self.go_switch_fullscreen()
			return True

		elif accelerator_name == self.keybind_accelerator_name_play_icrt:
			self.go_play_icrt()
			return True

		return False

	def on_key_release (self, win, evt):
		accelerator_name = Gtk.accelerator_name(evt.keyval, evt.state)
		## accelerator_label = Gtk.accelerator_get_label(evt.keyval, evt.state)

		return False

	def on_show_about (self, menu_item):
		self.go_show_about()

	def on_quit_app (self, menu_item):
		self.go_quit()

	def on_activate_win (self, menu_item):
		self.go_activate()

	def on_fullscreen_win (self, menu_item):
		self.go_fullscreen()

	def on_get_uri (self, menu_item):
		print('current_uri:', self.go_get_uri())

	def on_play_icrt (self, menu_item):
		self.go_play_icrt()

	def on_key_activate_win (self, accelerator_name):
		self.go_switch_activate()

	def on_close_win (self, win, evt):
		self.go_deactivate()

		return True

	def go_load_default (self):
		self.webview.load_uri(self.uri_default)

	def go_get_uri (self):
		return self.webview.get_uri()

	def go_play_icrt (self):
		js = ''
		js += "var proxy=document.getElementById('proxy');\n"
		js += "proxy.init('MTU0MDE3NzAzMjI')\n"
		self.webview.run_javascript(js);

	## fullscreen
	def is_fullscreen (self):
		return self.state_fullscreen

	def set_state_fullscreen (self, val):
		self.state_fullscreen = val

	def go_switch_fullscreen (self):
		if self.is_fullscreen():
			self.go_unfullscreen()
		else:
			self.go_fullscreen()

	def go_fullscreen (self):
		self.set_state_fullscreen(True)
		self.win.fullscreen()
		self.go_activate()

	def go_unfullscreen (self):
		self.set_state_fullscreen(False)
		self.win.unfullscreen()

	## activate
	def is_activate (self):
		return self.state_activate

	def set_state_activate (self, val):
		self.state_activate = val

	def go_switch_activate (self):
		if self.is_activate():
			self.go_deactivate()
		else:
			self.go_activate()

	def go_activate (self):
		self.set_state_activate(True)
		self.win.present()
		self.go_switch_icon_on_win_activate()

	def go_deactivate (self):
		self.set_state_activate(False)
		self.win.hide()
		self.go_switch_icon_on_win_deactivate()

	def go_switch_icon_on_win_activate (self):
		self.indicator.set_icon(self.icon_name_on_win_activate)

	def go_switch_icon_on_win_deactivate (self):
		self.indicator.set_icon(self.icon_name_on_win_deactivate)

	def go_show_about (self):
		print('hiply:')

	def go_quit (self):
		Gtk.main_quit()

	def run (self):
		Gtk.main()

def main ():
	app = App()
	app.init()
	app.run()


if __name__ == '__main__':
	main()
