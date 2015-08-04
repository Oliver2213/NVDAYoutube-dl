# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Full getext (please don't change)
_ = lambda x : x

# Add-on information variables
addon_info = {
	# for previously unpublished addons, please follow the community guidelines at:
	# https://bitbucket.org/nvdaaddonteam/todo/raw/master/guideLines.txt
	# add-on Name, internal for nvda
	"addon_name" : "nvdaYoutubeDL",
	# Add-on summary, usually the user visible name of the addon.
	# Translators: Summary for this add-on to be shown on installation and add-on information.
	"addon_summary" : _("NVDA Youtube-DL"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon_description" : _("""
***notice***
This is *not* the original addon, it has threading modifications by blake oliver.
To view all my modifications to this add-on, visit https://github.com/oliver2213/NVDAYoutube-DL, and look at the branches.
This addon integrates your NVDA screen reader with Youtube-DL. Youtube-DL is a small program to download videos from YouTube.com and many, many, many more sites.
To use this addon, you just select a URL address of the video by using standard Windows text selection commands, and then press NVDA+F8. The selected URL will be detected, and your video will be downloaded and converted automatically.
Go to NVDA menu, Youtube Downloader submenu to configure download formats and other options.
"""),
	# version
	"addon_version" : "1.1dev",
	# Author(s)
	"addon_author" : u"Hrvoje Katić <info@hrvojekatic.com>, Blake Oliver <oliver2213@me.com>",
	# URL for the add-on documentation support
	"addon_url" : "www.hrvojekatic.com",
	# Documentation file name
	"addon_docFileName" : "readme.html",
}


import os.path

# Define the python files that are the sources of your add-on.
# You can use glob expressions here, they will be expanded.
pythonSources = [os.path.join("addon", "globalPlugins", "nvdaYoutubeDL", "*.py"), os.path.join("addon", "*.py")]

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []
