from cStringIO import StringIO
import os.path
import configobj
from validate import Validator
import globalVars
from logHandler import log

confFile="nvdaYoutubeDL.ini"
conf=None

_confSpec="""
[converter]
format=string(default=mp3)
quality=string(default=192)
"""

def load():
	global conf
	if conf is None:
		path=os.path.join(globalVars.appArgs.configPath, confFile)
		conf=configobj.ConfigObj(path, configspec=StringIO(_confSpec), encoding="utf-8")
		conf.newlines = "\r\n"
		conf.stringify=True
		val=Validator()
		ret=conf.validate(val, preserve_errors=True, copy=True)
		if ret != True:
			log.warning("Invalid configuration file for nvdaYoutubeDL: %s", ret)

def save():
	global conf
	if conf is None:
		raise RuntimeError("Configuration for nvdaYoutubeDL not loaded.")
	val=Validator()
	conf.validate(val, copy=True)
	conf.write()
