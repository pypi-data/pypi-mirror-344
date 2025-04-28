import argparse
import os
from .uploader import upload_file, upload_xml_files_from_folder
from .config import Config

def run():
	parser = argparse.ArgumentParser(description="Upload a single .xml file or all .xml files in a folder to an API endpoint.")
	parser.add_argument('path', help='Path to .xml file or folder containing .xml files')
	parser.add_argument('--api_key', required=True, help='Bugasura API Key')
	parser.add_argument('--team_id', required=True, help='Bugasura Team Id')
	parser.add_argument('--project_id', required=True, help='Bugasura Project Id')
	parser.add_argument('--testrun_id', required=False, help='Bugasura Testrun Id. If not passed, new Testrun will be created in the Bugasura Project')
	parser.add_argument('--server', required=False, choices=['local', 'live', 'stage', 'facilio', 'shoppersstop', 'frammer', 'jupiter', 'trustrace', 'testpert'], help='Enterprise Server Names')
	args = parser.parse_args()
	api_base_url = "http://localhost/api.appachhi.com/"

	# if args.server:

	# 	if args.server.lower() == "local":
	# 		Config().server = 'LOCAL'
	# 		Config().api_base_url = "http://localhost/api.appachhi.com/"
	# 	elif args.server.lower() == "stage":
	# 		print("here")
	# 		Config().server = 'STAGE'
	# 		Config().api_base_url = "https://api.stage.bugasura.io/"
	# 	elif args.server.lower() == "live":
	# 		Config().server = 'LIVE'
	# 		Config().api_base_url = "https://api.bugasura.io/"
	# 	elif args.server.lower() == "facilio":
	# 		Config().server = 'CUSTOM'
	# 		Config().api_base_url = "https://api.facilio.bugasura.io/"
	# 	elif args.server.lower() == "shoppersstop":
	# 		Config().server = 'CUSTOM'
	# 		Config().api_base_url = "https://api.shoppersstop.bugasura.io/"
	# 	elif args.server.lower() == "frammer":
	# 		Config().server = 'CUSTOM'
	# 		Config().api_base_url = "https://api.frammer.bugasura.io/"
	# 	elif args.server.lower() == "jupiter":
	# 		Config().server = 'CUSTOM'
	# 		Config().api_base_url = "https://api.jupiter.bugasura.io/"
	# 	elif args.server.lower() == "trustrace":
	# 		Config().server = 'CUSTOM'
	# 		Config().api_base_url = "https://api.trustrace.bugasura.io/"
	# 	elif args.server.lower() == "testpert":
	# 		Config().server = 'CUSTOM'
	# 		Config().api_base_url = "https://api.testpert.bugasura.io/"
	# 	else:
	# 		raise ValueError(f"Unsupported enterprise server: {server}")

	# else:
	# 	Config().server = "LOCAL"
	# 	Config().api_base_url = "http://localhost/api.appachhi.com/"

	if args.server:
		if args.server.lower() == "local":
			api_base_url = "http://localhost/api.appachhi.com/"
		elif args.server.lower() == "stage":
			api_base_url = "https://api.stage.bugasura.io/"
		elif args.server.lower() == "live":
			api_base_url = "https://api.bugasura.io/"
		elif args.server.lower() == "facilio":
			api_base_url = "https://api.facilio.bugasura.io/"
		elif args.server.lower() == "shoppersstop":
			api_base_url = "https://api.shoppersstop.bugasura.io/"
		elif args.server.lower() == "frammer":
			api_base_url = "https://api.frammer.bugasura.io/"
		elif args.server.lower() == "jupiter":
			api_base_url = "https://api.jupiter.bugasura.io/"
		elif args.server.lower() == "trustrace":
			api_base_url = "https://api.trustrace.bugasura.io/"
		elif args.server.lower() == "testpert":
			api_base_url = "https://api.testpert.bugasura.io/"

	if not args.testrun_id:
		args.testrun_id = ''

	try:
		if os.path.isfile(args.path):
			result = upload_file(args.path, args.api_key, args.team_id, args.project_id, args.testrun_id, api_base_url)
			print("Upload successful:", result)
		elif os.path.isdir(args.path):
			results = upload_xml_files_from_folder(args.path, args.api_key, args.team_id, args.project_id, args.testrun_id, api_base_url)
			print(f"Uploaded {len(results)} file(s) successfully:", results)
		else:
			raise ValueError(f"Invalid path: {args.path}")
	except Exception as e:
		print("Upload failed:", str(e))