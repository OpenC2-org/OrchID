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

from orchid.models import OpenC2Action

# Logging
import logging
logger = logging.getLogger("console")

def openc2_action(target_list, actuator_list=None):
	"""
	Decorator for OpenC2 target and actuator types.
	"""
	def register(function):

		name = function.__name__
		
		current_def = function.__globals__.get(name)
		
		if current_def is None:

			current_def = OpenC2Action(name)
		
			# Generate all signatures
			for target in target_list:

				if actuator_list:

					for actuator in actuator_list:
				
						sig = {"action":name,"target":target,"actuator":actuator}
						logger.info("Registered %s name with signature %s" % (name,sig))
						current_def.register(sig, function)

				else:

					sig =  {"action":name,"target":target}

					logger.info("Registered %s name with signature %s" % (name,sig))
					current_def.register(sig, function)

		return current_def

	return register