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
from __future__ import unicode_literals

from django.db import models
import json

# Logging
import logging
logger = logging.getLogger("console")

# Create your models here.
class OpenC2Action(object):

	def __init__(self,name):

		self.name = name
		self.function_signatures = []
		self.function = None


	def sig_match(self, message, function_signature):

		# Should work to the following logic:
		#							|    Specifier In Profile Signature	  |    Specifier Not In Profile Signature 
		# Specifier In message		|			  Match					  |				Match - Generic Profile - But use profile logic to check specifiers (saves writing a profile for every firewall etc)
		# Specifier Not In message	|			  No Match   			  |				Match
		

		# Check actions
		if function_signature["action"] != message["action"]:

			return False

		# Check Targets
		if function_signature["target"]["type"] != message["target"]["type"]:

			return False

		if "specifiers" in function_signature["target"]:

			for target_spec in function_signature["target"]["specifiers"]:

				if target_spec in message["target"]["specifiers"]:

					if function_signature["target"]["specifiers"][target_spec] != message["target"]["specifiers"][target_spec]:

						return False

				else:

					return False

		# Check Actuators
		if "actuator" in function_signature:

			if function_signature["actuator"]["type"] != message["actuator"]["type"]:

				return False

			if "specifiers" in function_signature["actuator"]:

				for actuator_spec in function_signature["actuator"]["specifiers"]:

					if actuator_spec in message["actuator"]["specifiers"]:

						if function_signature["actuator"]["specifiers"][actuator_spec] != message["actuator"]["specifiers"][actuator_spec]:

							return False

					else:

						return False
		return True

	def identify(self, message):

		# Identify functions capable of handling this message
		for func_sig in self.function_signatures:

			if self.sig_match(message,func_sig["sig"]):

				logger.info("A %s profile matched signature %s" % (self.name,json.dumps(func_sig["sig"])))

				return True

		return False


	def register(self, sig, function):

		self.function_signatures.append({"sig":sig,"function":function})
		self.function = function

	def __call__(self,target, actuator, modifier):

		return self.function(target, actuator, modifier)




