####################################################
#________				.__	.___________	   #
#\_____  \_______   ____ |  |__ |   \______ \	  #
# /   |   \_  __ \_/ ___\|  |  \|   ||	|  \	 #
#/	|	\  | \/\  \___|   Y  \   ||	`   \	#
#\_______  /__|	\___  >___|  /___/_______  /	#
#		\/			\/	 \/			\/	 #
#												   #
#  Orchestrator for Intelligence Defence - OpenC2  #
####################################################
import collections
import imp
import os
from django.http import Http404
from django.http import HttpResponse
from django.conf import settings
from ..models import OpenC2Action
import json
# Logging
import logging
logger = logging.getLogger("console")

class Dispatcher(object):


	def __init__(self):

		logger.info("Initialising dispatcher")
		
		self.profiles = collections.deque()

		for module in settings.OPENC2_PROFILES:

			logger.info("Loading profile %s" % module)
			self.profiles.appendleft(imp.load_source(module.split(".")[0], "./orchid/profiles/"+module))

	def capabilities(self):


		# Hacky - returns a list of signatures
		info = []
		for module in self.profiles:
			for var in dir(module):
				obj = getattr(module, var)
				if isinstance(obj, OpenC2Action):
					for sig in obj.function_signatures:
						info.append(sig["sig"])
						
		return json.dumps(info)


	def dispatch(self,message):

		logger.debug("Dispatcher called")
		capable_handlers = []

		# Check action / target type
		if message["action"] == 'query' and message["target"]["type"] == 'openc2:openc2':
			return HttpResponse(self.capabilities(),status=200)

		for profile in self.profiles:

			if hasattr(profile, message['action']):

				f = getattr(profile, message['action'])

				if f.identify(message):

					capable_handlers.append(f)

		if len(capable_handlers) > 0:

			for f in capable_handlers:

				# Handle responses here
				# TODO - Threading here
				status = f(message["target"], message.get("actuator"), message.get("modifiers"))

			return HttpResponse(status=200)

		else:

			return HttpResponse(status=501)



				

