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

	if args.server:
		api_urls = {
			'local': 'http://localhost/api.appachhi.com/',
			'stage': 'https://api.stage.bugasura.io/',
			'live': 'https://api.bugasura.io/',
			'facilio': 'https://api.facilio.bugasura.io/',
			'shoppersstop': 'https://api.shoppersstop.bugasura.io/',
			'frammer': 'https://api.frammer.bugasura.io/',
			'jupiter': 'https://api.jupiter.bugasura.io/',
			'trustrace': 'https://api.trustrace.bugasura.io/',
			'testpert': 'https://api.testpert.bugasura.io/'
		}
		Config().api_base_url = api_urls.get(args.server, 'http://localhost/api.appachhi.com/')

		match args.server:
			case 'local':
				Config().server = 'LOCAL'
			case 'stage':
				Config().server = 'STAGE'
			case 'live':
				Config().server = 'LIVE'
			case _:
				Config().server = 'CUSTOM'

	else:
		Config().server = "LOCAL"
		Config().api_base_url = "http://localhost/api.appachhi.com"

	if not args.testrun_id:
		args.testrun_id = ''

	try:
		if os.path.isfile(args.path):
			result = upload_file(args.path, args.api_key, args.team_id, args.project_id, args.testrun_id)
			print("Upload successful:", result)
		elif os.path.isdir(args.path):
			results = upload_xml_files_from_folder(args.path, args.api_key, args.team_id, args.project_id, args.testrun_id)
			print(f"Uploaded {len(results)} file(s) successfully:", results)
		else:
			raise ValueError(f"Invalid path: {args.path}")
	except Exception as e:
		print("Upload failed:", str(e))