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
#	responder.py
#
# Descriptions: 
#	
#	Holds all logic for handling responses - WORK IN PROGRESS - THIS IS JUST AN EXAMPLE
#
# Sample Files:
#	
#	- ./samples/response_message.json
# 	- ./samples/command_with_request_response_ack.json

from django.conf import settings
import requests
import json

# Logging
import logging
logger = logging.getLogger("console")

# These will change at somepoint, so putting them in variables for now
command_respond_to_identifier = "respond_to"


def make_response_message(command_ref, com_type, value):

	msg = {}

	msg["action"] = "response"

	msg["target"] = {}
	msg["target"]["type"] = "openc2:Data"

	msg["modifiers"] = {}

	msg["modifiers"]["command-ref"] = command_ref
	msg["modifiers"]["type"] = com_type
	msg["modifiers"]["value"] = value


	return json.dumps(msg)

def respond_ack(modifiers):

	if "id" in modifiers and command_respond_to_identifier in modifiers and "response" in modifiers:

		logger.info("Responding to message ref:%s to %s [ACK]" % (modifiers["id"],modifiers["respond_to"]))

		message_to_send = make_response_message(modifiers["id"],"ack","ack")

		r = requests.post(modifiers["respond_to"], message_to_send)

		if r.status_code == 200:

			logger.info("Successful ACK sent to %s command ref: %s." % (modifiers["respond_to"],modifiers["id"]))

		else:

			logger.error("Failed to send ACK to %s command ref: %s." % (modifiers["respond_to"],modifiers["id"]))

	else:

		logger.error("A response was requested, but didnt have the required fields to facilate response.")

