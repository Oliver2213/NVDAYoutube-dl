from collections import OrderedDict
import os.path
import wx
import gui
import globalVars
import config
import addonConfig
import addonHandler
addonConfig.load()
addonHandler.initTranslation()

availableConversionFormats=OrderedDict([
	("aac","AAC"),
	("mp3","MP3"),
	("m4a","M4A"),
	("opus","Opus"),
	("vorbis","Ogg Vorbis"),
	("wav","WAV")])

availableConversionQualities=OrderedDict([
	("128","128 kbps"),
	("160","160 kbps"),
	("192","192 kbps"),
	("224","224 kbps"),
	("256","256 kbps"),
	("320","320 kbps")])

class audioConverterOptionsDialog(gui.SettingsDialog):
	# Translators: name of the dialog.
	title=_("Audio Converter Options")

	def __init__(self, parent):
		super(audioConverterOptionsDialog, self).__init__(parent)

	def makeSettings(self, sizer):
		conversionFormatSizer=wx.BoxSizer(wx.HORIZONTAL)
		# Translators: This is the name of the option in Audio Converter Options dialog.
		conversionFormatLabel=wx.StaticText(self, label=_("Conversion &format:"))
		conversionFormatSizer.Add(conversionFormatLabel)
		self.conversionFormatChoice = wx.Choice(self, choices=availableConversionFormats.values())
		conversionFormatSizer.Add(self.conversionFormatChoice)
		for pos, val in enumerate(availableConversionFormats.keys()):
			if addonConfig.conf['converter']['format']==val:
				self.conversionFormatChoice.SetSelection(pos)
		conversionQualitySizer=wx.BoxSizer(wx.HORIZONTAL)
		# Translators: This is the name of the option in Audio Converter Options dialog.
		conversionQualityLabel=wx.StaticText(self, label=_("Conversion &quality:"))
		conversionQualitySizer.Add(conversionQualityLabel)
		self.conversionQualityChoice = wx.Choice(self, choices=availableConversionQualities.values())
		conversionQualitySizer.Add(self.conversionQualityChoice)
		for pos, val in enumerate(availableConversionQualities.keys()):
			if addonConfig.conf['converter']['quality']==val:
				self.conversionQualityChoice.SetSelection(pos)

	def postInit(self):
		self.conversionFormatChoice.SetFocus()

	def onOk(self, event):
		super(audioConverterOptionsDialog, self).onOk(event)
		for pos, val in enumerate(availableConversionFormats.keys()):
			if self.conversionFormatChoice.GetSelection()==pos:
				addonConfig.conf['converter']['format']=val
		for pos, val in enumerate(availableConversionQualities.keys()):
			if self.conversionQualityChoice.GetSelection()==pos:
				addonConfig.conf['converter']['quality']=val
		addonConfig.save()
