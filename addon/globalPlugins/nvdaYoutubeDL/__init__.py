# -*- coding: utf-8 -*-

"""
Youtube Add-on for NVDA
@author: Hrvoje Katich <info@hrvojekatic.com>
@license: GNU General Public License version 2.0
"""

from __future__ import unicode_literals
import globalPluginHandler
import gettext
import languageHandler
import scriptHandler
import ui
import tones
import config
import addonConfig
import interface
import gui
import os
import sys
import wx
import re
import api
import textInfos
from logHandler import log
import addonHandler
addonConfig.load()
addonHandler.initTranslation()

PLUGIN_DIR = os.path.dirname(__file__)
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'Downloads')
sys.path.append(os.path.join(PLUGIN_DIR, "lib"))
import xml 
xml.__path__.append(os.path.join(PLUGIN_DIR, "lib", "xml"))
import youtube_dl
del sys.path[-1]
if not os.path.exists(DOWNLOAD_DIR): os.mkdir(DOWNLOAD_DIR)

class speakingLogger(object):

	def debug(self, msg):
		log.debug(msg)

	def warning(self, msg):
		log.warning(msg)

	def error(self, msg):
		log.error(msg)

def speakingHook(d):
	if d['status'] == 'downloading':
			tones.beep(500, 50)
	elif d['status'] == 'finished':
		ui.message(_("Download complete. Converting video."))
	elif d['status'] == 'error':
		ui.message(_("Download error."))

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self.menu=gui.mainFrame.sysTrayIcon.menu
		self.youtubeDownloaderSubmenu=wx.Menu()
		self.audioConverterOptionsMenuItem=self.youtubeDownloaderSubmenu.Append(wx.ID_ANY,
		# Translators: the name for an item of addon submenu.
		_("Audio &converter options..."),
		# Translators: the tooltip text for an item of addon submenu.
		_("Displays a dialog box for audio converter setup"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onAudioConverterOptionsClicked, self.audioConverterOptionsMenuItem)
		self.downloadsFolderMenuItem=self.youtubeDownloaderSubmenu.Append(wx.ID_ANY,
		# Translators: the name for an item of addon submenu.
		_("View &downloaded videos"),
		# Translators: the tooltip text for an item of addon submenu.
		_("Opens a folder with downloaded videos"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onDownloadsFolderClicked, self.downloadsFolderMenuItem)
		self.youtubeDownloaderMenuItem=self.menu.InsertMenu(2, wx.ID_ANY,
		# Translators: the name of addon submenu.
		_("&Youtube downloader"), self.youtubeDownloaderSubmenu)

	def onAudioConverterOptionsClicked(self, evt):
		gui.mainFrame._popupSettingsDialog(interface.audioConverterOptionsDialog)

	def onDownloadsFolderClicked(self, evt):
		try:
			os.startfile(DOWNLOAD_DIR)
		except WindowsError:
			pass

	def terminate(self):
		try:
			self.menu.RemoveItem(self.youtubeDownloaderMenuItem)
		except wx.PyDeadObjectError:
			pass

	def script_downloadVideo(self, gesture):
		currentDirectory=os.getcwdu()
		ydl_opts={
			'logger':speakingLogger(),
			'progress_hooks':[speakingHook],
			'format':'bestaudio/best',
			'postprocessors':[{
				'key':'FFmpegExtractAudio',
				'preferredcodec':addonConfig.conf['converter']['format'],
				'preferredquality':addonConfig.conf['converter']['quality'],
				}],
		}
		obj=api.getFocusObject()
		treeInterceptor=obj.treeInterceptor
		if hasattr(treeInterceptor,'TextInfo') and not treeInterceptor.passThrough:
			obj=treeInterceptor
		try:
			info=obj.makeTextInfo(textInfos.POSITION_SELECTION)
		except (RuntimeError, NotImplementedError):
			info=None
		if not info or info.isCollapsed:
			# Translators: This message is spoken if there's no selection.
			ui.message(_("Nothing selected."))
		else:
			urlPattern=re.compile(r"(^|[ \t\r\n])((http|https|www\.):?(([A-Za-z0-9$_.+!*(),;/?:@&~=-])|%[A-Fa-f0-9]{2}){2,}(#([a-zA-Z0-9][a-zA-Z0-9$_.+!*(),;/?:@&~=%-]*))?([A-Za-z0-9$_+!*();/?:~-]))")
			address=urlPattern.search(info.text)
			if address:
				os.chdir(DOWNLOAD_DIR)
				ui.message(_("Starting download."))
				with youtube_dl.YoutubeDL(ydl_opts) as ydl:
					ydl.download([unicode(address.group().strip())])
				ui.message(_("Done."))
				os.chdir(currentDirectory)
			else:
				# Translators: This message is spoken if selection doesn't contain any URL address.
				ui.message(_("Invalid URL address."))

	__gestures={
		"kb:NVDA+F8":"downloadVideo"
	}
