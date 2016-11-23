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
#	example_process_firewall_juniper.py
#
# Descriptions: 
#	
#	This profile is a basic layout for blocking a Cybox Network connection on a Juniper firewall
#
# Prerequisite: 
#
#	 - OPENC2_BIND_JUNIPER_FIREWALLS must be defined in the config file
#
# Sample Files
#	
#	- ./samples/deny_connection_firewall.json
#	- ./samples/deny_ip_firewall.json

from orchid.decorators import openc2_action
from django.conf import settings

# Logging
import logging
logger = logging.getLogger("console")

@openc2_action(target_list=[{"type":"cybox:Network_Connection"},{"type":"cybox:Address"}],actuator_list=[{"type":"network-firewall"}])
def deny(target, actuator, modifier):
	
	"""
	Deny a supplied Cybox network connection by adding a firewall rule to Juniper firewalls

	Accepted Actuator Specifiers:

		hostname = Hostname of the firewall
		ip = IP Address of the firewalls managment interface
		version = Version of the firewall (SSG5 etc) to help with version specific command syntax

	"""
	if "specifiers" in actuator:

		# Execute on a specific DNS Server
		for firewall in target_systems(actuator["specifiers"]):

			if target["type"] == "cybox:Network_Connection":

				# The user wants to block a connection			
				if firewall["version"] == "SSG5":

					juniper_ssg_block_connection(target,firewall)

				elif firewall["version"] == "SRX":

					juniper_srx_block_connection(target,firewall)

				else:

					# Unsupported vendor version
					pass

			elif target["type"] == "cybox:Address":

				# The user wants to block an IP address
				if firewall["version"] == "SSG5":

					juniper_ssg_block_address(target,firewall)

				elif firewall["version"] == "SRX":

					juniper_srx_block_address(target,firewall)

				else:

					# Unsupported vendor version
					logger.error("Unsupported Juniper Version Requested (%s), this profile does not support that model" % (firewall["version"]))

	else:

		# Execute on all DNS Servers
		for firewall in settings.OPENC2_JUNIPER_FIREWALLS:

			if target["type"] == "cybox:Network_Connection":

				# The user wants to block a connection			
				if firewall["version"] == "SSG5":

					juniper_ssg_block_connection(target,firewall)

				elif firewall["version"] == "SRX":

					juniper_srx_block_connection(target,firewall)

				else:

					# Unsupported vendor version
					pass

			elif target["type"] == "cybox:Address":

				# The user wants to block a IP address
				if firewall["version"] == "SSG5":

					juniper_ssg_block_address(target,firewall)

				elif firewall["version"] == "SRX":

					juniper_srx_block_address(target,firewall)

				else:

					# Unsupported vendor version
					logger.error("Unsupported Juniper Version Requested (%s), this profile does not support that model" % (firewall["version"]))

	return True

def target_systems(actuator_specifiers):
	"""
	Based on a set of specifiers taken from the OpenC2 message, decide
	which firewalls from OPENC2_JUNIPER_FIREWALLS are applicable

	"""

	valid_firewalls = []

	for firewall in settings.OPENC2_JUNIPER_FIREWALLS:


		if "hostname" in actuator_specifiers:

			if actuator_specifiers["hostname"] != firewall["hostname"]:

				continue

		if "ip" in actuator_specifiers:

			if actuator_specifiers["ip"] != firewall["ip"]:

				continue

		if "version" in actuator_specifiers:

			if actuator_specifiers["version"] != firewall["version"]:

				continue

		# If you get to here, this server matches all accepted specifiers
		valid_firewalls.append(firewall)		

	return valid_firewalls


def juniper_ssg_block_connection(target,firewall):

	"""
	Function to contain logic for deploying changes to a remote Juniper SSG to block a Connection
	
	TODO: SSH Logic here
	"""

	try:

		# Perform the Work Here
		logger.info("Block Connection %s->%s (%s) on Juniper SSG Firewall %s[%s]" % (
																					target["specifiers"]["SourceSocketAddress"]["IP_Address"]["Address_Value"],
																					target["specifiers"]["DestinationSocketAddress"]["IP_Address"]["Address_Value"],
																					target["specifiers"]["Layer4Protocol"],
																					firewall["hostname"],
																					firewall["ip"]))
		return True
	
	except Exception, e:

		# TODO: Raise Alert

		return False

def juniper_srx_block_connection(target,firewall):

	"""
	Function to contain logic for deploying changes to a remote Juniper SRX to block a Connection
	
	TODO: SSH Logic here
	"""

	try:

		# Perform the Work Here
		logger.info("Block Connection %s->%s (%s) on Juniper SRX Firewall %s[%s]" % (
																					target["specifiers"]["SourceSocketAddress"]["IP_Address"]["Address_Value"],
																					target["specifiers"]["DestinationSocketAddress"]["IP_Address"]["Address_Value"],
																					target["specifiers"]["Layer4Protocol"],
																					firewall["hostname"],
																					firewall["ip"]))
		return True
	
	except Exception, e:

		# TODO: Raise Alert

		return False

def juniper_ssg_block_address(target,firewall):

	"""
	Function to contain logic for deploying changes to a remote Juniper SSG to block an address
	
	TODO: SSH Logic here
	"""


	try:

		# Perform the Work Here
		logger.info("Block Address %s on Juniper SSG Firewall %s[%s]" % (
																		target["specifiers"]["IP_Address"]["Address_Value"],
																		firewall["hostname"],
																		firewall["ip"]))
		return True
	
	except Exception, e:

		# TODO: Raise Alert

		return False

def juniper_srx_block_address(target,firewall):

	"""
	Function to contain logic for deploying changes to a remote Juniper SRX to block an address
	
	TODO: SSH Logic here
	"""

	try:

		# Perform the Work Here
		logger.info("Block Address %s on Juniper SRX Firewall %s[%s]" % (
																		target["specifiers"]["IP_Address"]["Address_Value"],
																		firewall["hostname"],
																		firewall["ip"]))
		return True
	
	except Exception, e:

		# TODO: Raise Alert

		return False