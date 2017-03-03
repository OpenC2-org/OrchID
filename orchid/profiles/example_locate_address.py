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
#	example_address_lookup.py
#
# Descriptions: 
#	
#	This profile carries out a GeoIP lookup of a Cybox addresses in OpenC2 messages using a third party service
#
#
# Sample Files
#	
#	- ./samples/geoip_address_connection.json

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

@openc2_action(actuator_list=[{"type":"process-location-service"}], target_list=[{"type":"cybox:AddressObjectType"}])
def locate(target, actuator, modifier):

	cybox_address_obs = Observable.from_json(json.dumps(target["specifiers"]))

	address = str(cybox_address_obs.object_.properties.address_value)

	if is_public(address):

		country = geo_lookup(address)
		print country
		# Handle response
		if country and "respond-to" in modifier:

			if "command-ref" in modifier:
				ref = modifier["command-ref"]
			else:
				ref = None

			respond_message(make_response_message(ref, "simple", {"country":country}),modifier["respond-to"])

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

def geo_lookup(address):

	# Using Free GeoIP Net
	url="http://freegeoip.net/json/%s" % address

	try:

		return json.loads(requests.get(url).text)

	except:

		print "ERROR: freegeoip.net"
		return False