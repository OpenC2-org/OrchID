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
# Name: 
#	
#	example_response.py
#
# Descriptions: 
#	
#	This profile is a basic response receiver, it just reveives and logs responses
#
#
# Sample Files
#	
#	- ./samples/response_message.json

from orchid.decorators import openc2_action
from django.conf import settings

# Logging
import logging
logger = logging.getLogger("console")

@openc2_action(target_list=[{"type":"openc2:Data"}])
def response(target, actuator, modifier):

	if "command-ref" in modifier and "type" in modifier:

		if "value" in modifier:
		
			logger.info("Response message received: command:%s type:%s value:%s" % (modifier["command-ref"],modifier["type"],modifier["value"]))
		
		else:

			logger.info("Response message received: command:%s type:%s " % (modifier["command-ref"],modifier["type"]))
	else:

		logger.warning("RESPONSE Message received that was missing the correct command-ref / type feilds")
