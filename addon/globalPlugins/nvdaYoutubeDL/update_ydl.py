# -*- coding: utf-8 -*-
"""
Author of this file: Blake Oliver <oliver22213@me.com>
File that contains a class and it's methods for updating YDL

This class doesn't update YDL, it only phasilitates an easy way to do so.
First, it calls a function to determine the latest YDL available and makes that accessible from whatever classname it's enstantiated with. E.G:
updater = update_ydl.YDLUpdate(pluginpath, False, CurrentVersion)
After that, you can access the latest version like
updater.latest_version

"""


class YDLUpdate(object):
	def __init__(self, pluginpath, silent=False, version):
		self.pluginpath = pluginpath
		self.silent = silent
		self.YDLVersion = version
		self.updateURL = "https://rg3.github.io/youtube-dl/update/"
		self.latestURL=updateURL+'LATEST_VERSION'
		# Get the latest YDL version from the github repo:
		self.latest_version = self.getLatest(self.latestURL)

	def getLatest(URL):
		