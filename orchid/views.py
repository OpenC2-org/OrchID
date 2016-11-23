####################################################
#________                .__    .___________       #
#\_____  \_______   ____ |  |__ |   \______ \      #
# /   |   \_  __ \_/ ___\|  |  \|   ||    |  \     #
#/    |    \  | \/\  \___|   Y  \   ||    `   \    #
#\_______  /__|    \___  >___|  /___/_______  /    #
#        \/            \/     \/            \/     #
#												   #
#  Orchestrator for Intelligence Defence - OpenC2  #
####################################################
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse

from validators import openc2_validatior

from profiles import Dispatcher
import json

# Logging
import logging
logger = logging.getLogger("console")

# Response
import response

# Create a single dispatcher on load
dispatcher = Dispatcher()

@csrf_exempt
def service_router(request):

	if request.method != 'POST':
		
		logger.error("None POST request received.")

		return HttpResponse(status=400)

	else:

		try:

			# Parse To JSON			
			openc2_command = json.loads(request.body)
			
		except ValueError:

			# Not a valid JSON
			logger.error("Invalid JSON received from client %s" % request.META.get('REMOTE_ADDR'))
			return HttpResponse(status=400)

		if openc2_validatior(openc2_command):


			# Log the message
			logger.info("Inbound message received from %s" % request.META.get('REMOTE_ADDR'))
			logger.info("______________________")
			logger.info(request.body)
			logger.info("______________________")

			# If the user wants an out of band ack
			if "modifiers" in openc2_command:

				if "response" in openc2_command["modifiers"]:

					if openc2_command["modifiers"]["response"] == "ack":

						response.respond_ack(openc2_command["modifiers"])

			# Dispatch
			return dispatcher.dispatch(openc2_command)

		else:

			return HttpResponse(status=400)

		# TODO: Response
		return HttpResponse(status=200)
