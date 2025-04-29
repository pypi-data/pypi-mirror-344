from setuptools import setup, find_packages

APP = ['ultipa']
DATA_FILES = []
OPTIONS = {}

def readMe():
    try:

        ret = open("""/Users/wangjinrong/PycharmProjects/MakeUltipaPackage/ReadMe.md""", encoding="utf-8").read()
    except Exception as e:
        return ""
    return ret

setup(
    app=APP,
    name="ultipa",
    metaversion="",
    version="5.0.6",
    python_requires='>=3.9,<3.13',
    packages=find_packages(),  # 常用,要熟悉 :会自动查找当前目录下的所有模块(.py文件) 和包(包含__init___.py文件的文件夹)
    # scripts = ['say_hello.py'],
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[
				'google>=2.0.3',
                'grpcio>=1.48.2',
                'grpcio-tools>=1.48.2',
                'prettytable>=2.5.0',
                'protobuf>=3.19.0',
                'python-dateutil~=2.8.2',
                'pytz==2022.7',
                'pytz-deprecation-shim==0.1.0.post0',
                'schedule==1.1.0',
                'treelib==1.7.0',
                'tzdata==2024.2',
                'tzlocal==4.2',
                'requests==2.32.3'
                ],  # 常用
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst',"printer"],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },
    # metadata for upload to PyPI
    author="Ultipa",
    author_email="support@ultipa.com",
    description="Pure Python Ultipa Driver",
    license="PSF",
    keywords="ultipa sdk,ultipa graph",
    url="https://www.ultipa.com/document/ultipa-drivers/python-installation",  # project home page, if any
    long_description=readMe(),
    long_description_content_type='text/markdown',
    # could also include long_description, download_url, classifiers, etc.
)