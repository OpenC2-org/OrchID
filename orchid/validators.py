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
from jsonschema import validate

def openc2_validatior(openc2_message):

	schema = {
		"type" : "object",
		"properties" : {
			"action": {"type":"string"},
			"target":{
					"type" : "object",
					"properties":{
						"type":{"type":"string"},
						"specifiers":{
								"type":"object",
								"properties":{},
								"additionalProperties": True,
								}
					},
					"required": ["type"],
			},
			"actuator":{
					"type" : "object",
					"properties":{
						"type":{"type":"string"},
						"specifiers":{
								"type":"object",
								"properties":{},
								"additionalProperties": True,
								}
					},
					"required": ["type"]
					
			},
			"modifiers":{
					"type":"object",
					"properties":{},
					"additionalProperties": True,
			}
		
		},
		"required": ["action","target"]
	}

	try:

		validate(openc2_message,schema)
		return True
	
	except Exception, e:

		return False
