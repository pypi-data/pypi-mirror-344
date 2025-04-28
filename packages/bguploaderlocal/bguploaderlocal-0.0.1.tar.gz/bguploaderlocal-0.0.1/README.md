# BGS CLI File Uploader

A Python CLI tool to upload a single `.xml` file or all `.xml` files in a folder to an API endpoint.

---

## 📦 Installation

Install locally from source:

```
bash
pip install bguploaderlocal
```

## 🚀 Usage

Upload a single .xml file:

bguploaderlocal ./path/to/file.xml --api_key [Your API Key] --team_id [Bugasura Team Id] --project_id [Bugasura Project Id] --report_id [Bugasura Testrun Id (optional)] --server [Server Name (optional)]

Upload all .xml files from a folder:

bguploaderlocal ./path/to/folder --api_key [Your API Key] --team_id [Bugasura Team Id] --project_id [Bugasura Project Id] --report_id [Bugasura Testrun Id (optional)] --server [Server Name (optional)]


## ⚠️ Rules

	Only .xml files are allowed.

	Invalid paths or non-XML files will raise errors.

	For folders, only .xml files will be uploaded.


## 📂 Project Structure


	bguploaderlocal/
	├── bguploaderlocal/
	│	├── uploader.py
	│	├── cli.py
	│	└── __init__.py
	│	└── config.py
	├── setup.py
	├── bguploaderlocal.toml
	└── README.md


## ✅ License