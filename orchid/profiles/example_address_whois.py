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
#	example_address_whois.py
#
# Descriptions: 
#	
#	This profile carries out a Whois lookup of a Cybox addresses in OpenC2 messages using ARIN or RIPE
#
#
# Sample Files
#	
#	- ./samples/whois_address_connection.json

from orchid.decorators import openc2_action
from django.conf import settings
from orchid.profiles import Dispatcher
from orchid.response import make_response_message,respond_message

# General
import requests
import json

# Cybox/STIX/TAXII Stuff
from cybox.core import Observable 
from cybox.objects.address_object import Address


# Logging
import logging
logger = logging.getLogger("console")

@openc2_action(actuator_list=[{"type":"process-directory-service"}], target_list=[{"type":"cybox:AddressObjectType"}])
def report(target, actuator, modifier):

	cybox_address_obs = Observable.from_json(json.dumps(target["specifiers"]))

	address = str(cybox_address_obs.object_.properties.address_value)

	if is_public(address):

		whois = whois_lookup(address)
		
		# Handle response
		if whois and "respond-to" in modifier:

			if "command-ref" in modifier:
				ref = modifier["command-ref"]
			else:
				ref = None

			respond_message(make_response_message(ref, "simple", {"whois":whois}),modifier["respond-to"])

	return True

def is_public(address):

	# I could use NetAddr here but I am trying to keep the import footprint light
	addr = address.split(".")
	#Private A Class
	if addr[0] == '10':
		return False
	#Private B Class
	elif addr[0] == '172' and int(addr[1]) >= 16 and int(addr[1]) < 32:
		return False
	#Private C Class
	elif addr[0] == '192' and addr[1] == '168':
		return False
	else:
		return True

def whois_lookup(address):

	# ARIN the RIPE if needed
	try:
		url = 'http://whois.arin.net/rest/ip/'+address
		headers = {'Accept': 'application/json'}

		response = requests.get(url, headers=headers).text

		if "RIPE" in response:

			url = 'https://stat.ripe.net/data/whois/data.json?resource='+address
			return json.loads(requests.get(url, headers=headers).text)

		else:

			return json.loads(response)
	except:

		return False

