from setuptools import setup, find_packages

setup(
	name='bguploaderlocal',
	version='0.0.1',
	packages=find_packages(),
	install_requires=['requests','urllib3<2'],
	entry_points={
		'console_scripts': [
			'bguploaderlocal=bguploaderlocal.cli:run',
		],
	},
	author='Your Name',
	description='CLI to upload JUnit .xml files.',
	python_requires='>=3.6',
)