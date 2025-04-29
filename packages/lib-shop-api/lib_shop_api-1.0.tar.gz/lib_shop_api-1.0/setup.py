from setuptools import setup, find_packages

setup(
	name='lib_shop_api',
	version='1.0',
	packages=find_packages(),
	install_requires=[
		'requests',
		'beautifulsoup4',
		'fake_useragent',
	],
	description='Library-api for web-shop',
	author='Yurij',
	author_email='yuran.ignatenko@yanderx.ru',
	url='https://github.com/YuranIgnatenko/lib_shop_api',
)