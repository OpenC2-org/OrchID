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
from django.test import TestCase

from orchid.validators import openc2_validatior
from orchid.profiles import Dispatcher
from django.http import HttpResponse
import os
import json

# Create your tests here.
class SampleJSONTests(TestCase):

	def test_all_sample_jsons_for_validity(self):
		"""Loops through all sample JSONs and ensures all result in a 200"""

		for filename in os.listdir("./samples"):
			if filename.endswith(".json"): 

				with open('./samples/'+filename, 'r') as content_file:
					
					json_raw = content_file.read()

					self.assertTrue(openc2_validatior(json.loads(json_raw)))
				
			else:
				
				continue

		
	def test_all_sample_jsons_in_dispatcher(self):
		"""Loops through all sample JSONs and ensures all result in a 200"""

		for filename in os.listdir("./samples"):
			if filename.endswith(".json"): 

				with open('./samples/'+filename, 'r') as content_file:
					
					json_raw = content_file.read()

					openc2_command = json.loads(json_raw)

					dispatcher = Dispatcher()				
					print "Testing %s" % (filename)
					self.assertEquals(200,dispatcher.dispatch(openc2_command).status_code)

			else:
				
				continue