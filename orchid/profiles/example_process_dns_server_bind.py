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
#	example_process_dns_server_bind.py
#
# Descriptions: 
#	
#	This profile is a basic layout for sinkholeing a supplied Cybox domain name using bind DNS
#
# Prerequisite:
#
#	 - OPENC2_BIND_DNS_SERVERS must be defined in the config file
#
# Sample Files
#	
#	- ./samples/deny_domain_name_dns_server.json

from orchid.decorators import openc2_action
from django.conf import settings

# Logging
import logging
logger = logging.getLogger("console")

@openc2_action(target_list=[{"type":"cybox:Domain_Name"}],actuator_list=[{"type":"process-dns-server"}])
def deny(target, actuator, modifier):

	"""
	Deny a supplied Cybox Domain Name by sinkholing it on BIND DNS servers

	Accepted Actuator Specifiers:

		hostname = Hostname of the DNS Server
		ip = IP Address of the DNS Server

	"""
	if "specifiers" in actuator:

		# Execute on a specific DNS Server
		for dns_server in target_systems(actuator["specifiers"]):

			bind_dns_server_sinkhole(dns_server,target["specifiers"]["value"])

	else:

		# Execute on all DNS Servers
		for dns_server in settings.OPENC2_BIND_DNS_SERVERS:

			bind_dns_server_sinkhole(dns_server,target["specifiers"]["value"])

	return True

def target_systems(actuator_specifiers):
	"""
	Based on a set of specifiers taken from the OpenC2 message, decide
	which servers from OPENC2_BIND_DNS_SERVERS are applicable

	TODO: Add BIND Versions
	"""

	valid_servers = []

	for dns_server in settings.OPENC2_BIND_DNS_SERVERS:


		if "hostname" in actuator_specifiers:

			if actuator_specifiers["hostname"] != dns_server["hostname"]:

				continue

		if "ip" in actuator_specifiers:

			if actuator_specifiers["ip"] != dns_server["ip"]:

				continue

		# If you get to here, this server matches all accepted specifiers
		valid_servers.append(dns_server)		

	return valid_servers


def bind_dns_server_sinkhole(dns_server_object, target_domain_value):

	"""
	Function to contain logic for deploying changes to a remote BIND DNS Server
	
	TODO: SSH Logic here, append to zone file and live reload
	"""

	try:
		# Perform the Work Here
		logger.info("Sinkhole domain %s on DNS Server %s[%s] (BIND DNS Server)" % (target_domain_value,dns_server_object["hostname"],dns_server_object["ip"]))
		return True
	
	except Exception, e:

		# TODO: Raise Alert

		return False